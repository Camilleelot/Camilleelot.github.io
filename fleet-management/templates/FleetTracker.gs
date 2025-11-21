// FleetTracker for NGOs - Google Apps Script
// Version 1.0
// License: MIT
// Repository: https://github.com/Camilleelot/FleetTracker-NGO

// =============================================================================
// --- CONFIGURATION ---
// Edit these values to match your organization's setup
// =============================================================================

// !!! PRODUCTION EMAIL RECIPIENTS !!!
// Comma-separated list of email addresses to notify when incidents are reported
const RECIPIENT_EMAILS = 'ops@example.org,fleet@example.org';

// Master List Spreadsheet Details
// This spreadsheet contains your fleet inventory (vehicle details, insurance info)
const MASTER_LIST_SPREADSHEET_ID = '1895NA95MNA054MA9590AJMT9401JM'; // Replace with your spreadsheet ID
const MASTER_LIST_SHEET_NAME = 'Master Sheet';
const MASTER_LIST_KEY_HEADER = 'License Plate';
const MASTER_LIST_SUMMARY_HEADER = 'Lease/Coverage Summary';
const MASTER_LIST_VEHICLE_HEADER = 'Make';

// Folder IDs for file organization
// NEW_VEHICLE_ARCHIVE_FOLDER_ID: Where to file incidents for vehicles not yet in the map
const NEW_VEHICLE_ARCHIVE_FOLDER_ID = '902jnfc901ndiweh840dnmqaH495NMFHJ'; // Replace with your folder ID
// UPLOAD_FOLDER_ID: Temporary storage for form file uploads (before moving to vehicle folders)
const UPLOAD_FOLDER_ID = '123412351231514asdab123tb78v9s093n690vbhw905n6t0'; // Replace with your folder ID

// Form Field Names (must EXACTLY match the column headers in your Google Form response sheet)
const DATE_FIELD_NAME = 'Date of Incident';
const TIME_FIELD_NAME = 'Time of Incident (if known)';
const HOME_FIELD_NAME = 'What home does the driver fall under?';
const DRIVER_NAME_FIELD_NAME = 'Full Legal Name of the Driver';
const UPLOAD_FIELD_NAME = 'Vehicle Damage/Photos & Scene Diagram';
const DESCRIPTION_FIELD_NAME = 'Brief Description of What Happened';
const FORM_VEHICLE_FIELD_NAME = 'Vehicle In Question (Year/Make/Model/License Plate)';

// Map of License Plate to permanent vehicle Folder ID
// Add one entry per vehicle in your fleet
// Format: "LICENSE-PLATE": "GOOGLE_DRIVE_FOLDER_ID",
const VEHICLE_FOLDER_MAP = {
  "ABC-1234": "1A2-42ydOzwGw4qasaPfjw4_jlUdNR2ld",  // Example: Honda Civic
  "XYZ-5678": "9B8-73xdPawHx5rbtBgkx5_kmVeOS3me",  // Example: Toyota Camry
  // Add more vehicles here...
};

// =============================================================================
// --- HELPER FUNCTIONS ---
// Do not edit below unless you're customizing the logic
// =============================================================================

/**
 * Looks up the most recent maintenance/service record for a given vehicle
 * Scans the vehicle's Drive folder for files with "service" in the name
 * Returns: { lastServiceDate, lastServiceLink, nextServiceDate }
 */
function lookupMaintenanceData(licensePlate) {
  const incidentFolderId = VEHICLE_FOLDER_MAP[licensePlate];

  const maintenanceData = {
    lastServiceDate: 'N/A (No service file found)',
    lastServiceLink: 'N/A',
    nextServiceDate: 'N/A'
  };

  if (!incidentFolderId) {
    maintenanceData.lastServiceDate = 'Error: Vehicle folder ID not configured in script.';
    return maintenanceData;
  }

  try {
    const folder = DriveApp.getFolderById(incidentFolderId);
    const files = folder.getFiles();

    let latestDate = null;
    let latestFileUrl = '';

    const serviceRegex = /service/i; // Case-insensitive match for "service"
    const yyyyDateRegex = /(\d{4}[-/_]\d{2}[-/_]\d{2})/; // YYYY-MM-DD (or / or _)

    while (files.hasNext()) {
      const file = files.next();
      const fileName = file.getName();

      if (serviceRegex.test(fileName)) {
        let currentDate = null;
        let dateMatch = fileName.match(yyyyDateRegex);

        if (dateMatch) {
          // Extract date from filename
          const dateString = dateMatch[1].replace(/[-/_]/g, '-');
          currentDate = new Date(dateString);
        } else {
          // FALLBACK: Use the file's creation date if no date in filename
          currentDate = file.getDateCreated();
        }

        if (currentDate && !isNaN(currentDate.getTime())) {
          if (!latestDate || currentDate.getTime() > latestDate.getTime()) {
            latestDate = currentDate;
            latestFileUrl = file.getUrl();
          }
        }
      }
    }

    if (latestDate) {
      // Format last service date as YYYY-MM-DD
      const yyyy = latestDate.getFullYear();
      const mm = String(latestDate.getMonth() + 1).padStart(2, '0');
      const dd = String(latestDate.getDate()).padStart(2, '0');
      const lastDateFormatted = `${yyyy}-${mm}-${dd}`;

      maintenanceData.lastServiceDate = lastDateFormatted;
      maintenanceData.lastServiceLink = latestFileUrl;

      // Calculate next service date (add 3 months - adjust as needed for your schedule)
      const nextService = new Date(latestDate);
      nextService.setMonth(nextService.getMonth() + 3);

      const nextYyyy = nextService.getFullYear();
      const nextMm = String(nextService.getMonth() + 1).padStart(2, '0');
      const nextDd = String(nextService.getDate()).padStart(2, '0');

      maintenanceData.nextServiceDate = `${nextMm}/${nextDd}/${nextYyyy}`;
    }

  } catch (err) {
    Logger.log(`Error accessing vehicle folder ${incidentFolderId} for maintenance data: ${err.toString()}`);
    maintenanceData.lastServiceDate = `CRITICAL ERROR retrieving service history. Check folder ID and permissions.`;
  }

  return maintenanceData;
}

/**
 * Looks up vehicle details from the Master List spreadsheet
 * Extracts the license plate from the form submission string (assumes last word)
 * Returns: { key: licensePlate, summary: coverageInfo, makeModel: displayName }
 */
function lookupVehicleData(fullVehicleString) {
  // Extract license plate (assumes format: "2020 Honda Civic ABC-1234")
  const parts = fullVehicleString.split(' ');
  const licensePlate = parts[parts.length - 1];

  // Default values if lookup fails
  let coverageSummary = `License Plate (${licensePlate}) not found in Master List.`;
  let vehicleMakeModel = licensePlate;

  try {
    const ss = SpreadsheetApp.openById(MASTER_LIST_SPREADSHEET_ID);
    const sheet = ss.getSheetByName(MASTER_LIST_SHEET_NAME);

    if (!sheet) {
      return { key: licensePlate, summary: `Error: Master List sheet '${MASTER_LIST_SHEET_NAME}' not found.`, makeModel: licensePlate };
    }

    const data = sheet.getDataRange().getValues();
    const headers = data[0];
    const dataRows = data.slice(1);

    // Find column indices dynamically (resilient to column reordering)
    const keyColIndex = headers.indexOf(MASTER_LIST_KEY_HEADER);
    const summaryColIndex = headers.indexOf(MASTER_LIST_SUMMARY_HEADER);
    const makeColIndex = headers.indexOf(MASTER_LIST_VEHICLE_HEADER);

    if (keyColIndex !== -1 && summaryColIndex !== -1) {
      for (const row of dataRows) {
        if (row[keyColIndex] === licensePlate) {
          coverageSummary = row[summaryColIndex] || 'No summary provided in Master List.';
          vehicleMakeModel = makeColIndex !== -1 ? `${row[makeColIndex]} (${licensePlate})` : licensePlate;
          break;
        }
      }
    }
  } catch (err) {
    Logger.log(`CRITICAL ERROR accessing Master List: ${err.toString()}`);
    coverageSummary = `CRITICAL ERROR accessing Master List: ${err.toString()}`;
  }

  return {
    key: licensePlate,
    summary: coverageSummary,
    makeModel: vehicleMakeModel
  };
}

// =============================================================================
// --- MAIN TRIGGER FUNCTION ---
// This function is automatically executed when the Google Form is submitted
// =============================================================================

/**
 * Main function triggered when the Google Form is submitted.
 * Handles lookups, file filing, Google Doc generation, and email notification.
 * @param {object} e The form submission event object.
 */
function onFormSubmit(e) {
  const responseData = e.namedValues;

  // 1. Extract form data
  const submissionDate = responseData['Timestamp'][0];
  const dateValue = responseData[DATE_FIELD_NAME] ? responseData[DATE_FIELD_NAME][0] : 'No Date';
  const driverName = responseData[DRIVER_NAME_FIELD_NAME] ? responseData[DRIVER_NAME_FIELD_NAME][0] : 'No Driver';
  const homeValue = responseData[HOME_FIELD_NAME] ? responseData[HOME_FIELD_NAME][0] : 'No Home';
  const timeValue = responseData[TIME_FIELD_NAME] ? responseData[TIME_FIELD_NAME][0] : 'No Time';
  const briefDescription = responseData[DESCRIPTION_FIELD_NAME] ? responseData[DESCRIPTION_FIELD_NAME][0] : 'N/A';
  const fullVehicleString = responseData[FORM_VEHICLE_FIELD_NAME] ? responseData[FORM_VEHICLE_FIELD_NAME][0] : 'No Vehicle Selected';

  // 2. Look up vehicle context from Master List and maintenance records
  const vehicleData = lookupVehicleData(fullVehicleString);
  const { key: licensePlate, summary: coverageSummary, makeModel } = vehicleData;
  const maintenanceData = lookupMaintenanceData(licensePlate);

  // 3. Determine the parent folder (vehicle-specific or archive for new vehicles)
  let parentFolderId = VEHICLE_FOLDER_MAP[licensePlate];
  if (!parentFolderId) {
    Logger.log(`Vehicle ${licensePlate} not in static map. Filing in new vehicle archive.`);
    parentFolderId = NEW_VEHICLE_ARCHIVE_FOLDER_ID;
  }
  const parentFolder = DriveApp.getFolderById(parentFolderId);

  // 4. Create incident folder with standardized name
  // Format: YYYY-MM-DD - Incident - [Driver Name] - [Vehicle Make/Model] (Plate)
  const incidentFolderName = `${Utilities.formatDate(new Date(submissionDate), Session.getScriptTimeZone(), 'yyyy-MM-dd')} - Incident - ${driverName} - ${makeModel}`;
  const incidentFolder = parentFolder.createFolder(incidentFolderName);
  const incidentFolderUrl = incidentFolder.getUrl();
  Logger.log(`Incident folder created: ${incidentFolderUrl}`);

  // 5. Move uploaded files from temporary upload folder to incident folder
  const fileUrlsString = responseData[UPLOAD_FIELD_NAME] ? responseData[UPLOAD_FIELD_NAME][0] : '';
  const fileIds = fileUrlsString.match(/id=([a-zA-Z0-9_-]+)/g);

  if (fileIds) {
    const uploadFolder = DriveApp.getFolderById(UPLOAD_FOLDER_ID);
    fileIds.forEach(idMatch => {
      const fileId = idMatch.replace('id=', '');
      try {
        const file = DriveApp.getFileById(fileId);
        file.makeCopy(incidentFolder); // Copy to incident folder
        uploadFolder.removeFile(file); // Remove from temporary upload folder
      } catch (e) {
        Logger.log(`Could not move file ${fileId}: ${e.toString()}`);
      }
    });
  }

  // 6. Create the Incident Summary Google Doc
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const lastRow = sheet.getLastRow();
  const values = sheet.getRange(lastRow, 1, 1, sheet.getLastColumn()).getDisplayValues()[0];
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getDisplayValues()[0];

  const docName = `${incidentFolderName} - Summary`;
  const doc = DocumentApp.create(docName);
  const body = doc.getBody();
  body.clear();

  // Document title and header
  body.appendParagraph('Vehicle Incident Report Summary')
      .setHeading(DocumentApp.ParagraphHeading.TITLE);
  body.appendParagraph(`Filed: ${Utilities.formatDate(new Date(submissionDate), Session.getScriptTimeZone(), 'MM/dd/yyyy HH:mm:ss')}`).setBold(false);
  body.appendParagraph(`Vehicle: ${makeModel}`).setBold(false);
  body.appendHorizontalRule();

  // Form data table
  body.appendParagraph('Form Data').setHeading(DocumentApp.ParagraphHeading.HEADING3);
  const dataTable = body.appendTable();

  headers.forEach((header, index) => {
    // Skip redundant fields
    if (header !== 'Timestamp' && header !== DESCRIPTION_FIELD_NAME && header !== FORM_VEHICLE_FIELD_NAME) {
      const row = dataTable.appendTableRow();
      row.appendTableCell(header + ':').setBold(true).setWidth(200);
      row.appendTableCell(values[index]).setWidth(400);
    }
  });

  // Lookup data table
  body.appendParagraph('').setSpacingBefore(12);
  body.appendParagraph('External Lookups').setHeading(DocumentApp.ParagraphHeading.HEADING3);
  const lookupTable = body.appendTable();

  lookupTable.appendTableRow().appendTableCell('Lease/Coverage Summary:').setBold(true).setWidth(200).getParent().appendTableCell(coverageSummary).setWidth(400);
  lookupTable.appendTableRow().appendTableCell('Last Uploaded Service Date:').setBold(true).setWidth(200).getParent().appendTableCell(maintenanceData.lastServiceDate).setWidth(400);
  lookupTable.appendTableRow().appendTableCell('Approximate Next Service Due:').setBold(true).setWidth(200).getParent().appendTableCell(maintenanceData.nextServiceDate + ' (Quarterly)').setBold(true).setWidth(400);

  // Description section
  body.appendParagraph('').setSpacingBefore(12);
  body.appendParagraph('Brief Description of What Happened').setHeading(DocumentApp.ParagraphHeading.HEADING3);
  body.appendParagraph(briefDescription).setBold(false);

  // Save and move the doc to the incident folder
  doc.saveAndClose();
  const docFile = DriveApp.getFileById(doc.getId());
  incidentFolder.addFile(docFile);
  DriveApp.getRootFolder().removeFile(docFile); // Remove from root

  // 7. Send Email Notification
  const emailSubject = `🚨 Vehicle Incident: ${driverName} - ${makeModel}`;

  const emailBody = `
    <p>A new <b>Vehicle Incident Report</b> has been filed.</p>
    <hr>

    <h3>Incident Details:</h3>
    <p><b>Driver:</b> ${driverName}</p>
    <p><b>Home/Program:</b> ${homeValue}</p>
    <p><b>Date/Time:</b> ${dateValue} at ${timeValue}</p>
    <p><b>Vehicle Involved:</b> ${makeModel}</p>

    <h3>Lease/Coverage Context (from Master List):</h3>
    <p>${coverageSummary}</p>

    <hr>

    <h3>Maintenance Context:</h3>
    <p><b>Last Uploaded Date of Service (Approximation based on Upload Date):</b>
      ${maintenanceData.lastServiceLink !== 'N/A' ? `<a href="${maintenanceData.lastServiceLink}">${maintenanceData.lastServiceDate}</a>` : maintenanceData.lastServiceLink}
    </p>
    <p><b>Approximate Next Service Due:</b>
      ${maintenanceData.nextServiceDate !== 'N/A' ? `<b>${maintenanceData.nextServiceDate}</b> (Quarterly)` : maintenanceData.nextServiceDate}
    </p>

    <hr>

    <h3>Brief Description:</h3>
    <p>${briefDescription}</p>

    <hr>

    <p>Click below to view the incident folder, uploaded photos, and Summary Document:</p>
    <p>👉 <a href="${incidentFolderUrl}">VIEW INCIDENT FOLDER: ${incidentFolderName}</a></p>
    <br>
    <p><i>This email was automatically generated by FleetTracker.</i></p>
  `;

  // Archive email content to the incident folder
  const emailFileName = `${incidentFolderName} - Email Notification Log.txt`;
  const emailFileContent = `Subject: ${emailSubject}\n\nRecipient List: ${RECIPIENT_EMAILS}\n\n---\n\nEmail Body:\n\n${emailBody.replace(/<[^>]*>/g, '').replace(/(\n\s*){3,}/g, '\n\n')}`;
  incidentFolder.createFile(emailFileName, emailFileContent, MimeType.PLAIN_TEXT);

  // Send the email
  try {
    MailApp.sendEmail({
      to: RECIPIENT_EMAILS,
      subject: emailSubject,
      htmlBody: emailBody
    });
    Logger.log('Email sent successfully to ' + RECIPIENT_EMAILS);
  } catch (error) {
    Logger.log('ERROR sending email: ' + error.toString());
  }
}
