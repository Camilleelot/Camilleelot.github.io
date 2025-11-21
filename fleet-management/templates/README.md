# FleetTracker Templates

This directory contains template files for deploying FleetTracker at your nonprofit organization.

## Files

### `FleetTracker.gs`
The main Google Apps Script code. Copy this into your Google Apps Script editor (Extensions → Apps Script from your form response spreadsheet).

**Configuration Required:**
- Update `RECIPIENT_EMAILS` with your notification email addresses
- Replace `MASTER_LIST_SPREADSHEET_ID` with your vehicle inventory spreadsheet ID
- Update folder IDs (`NEW_VEHICLE_ARCHIVE_FOLDER_ID`, `UPLOAD_FOLDER_ID`)
- Add your vehicles to `VEHICLE_FOLDER_MAP` (license plate → folder ID)

### `Master_Vehicle_List_Template.csv`
Template for your fleet inventory spreadsheet. Populate with your vehicle data.

**Required Columns:**
- **License Plate**: Unique identifier (MUST match form dropdown exactly)
- **Make**: Vehicle manufacturer and model
- **Year**: Model year
- **Lease/Coverage Summary**: Insurance details (e.g., "Owned / Full Coverage / State Farm #12345")
- **VIN**: Vehicle Identification Number (optional but recommended)

### `Form_Questions.txt`
Suggested Google Form questions and configurations.

**Critical Requirements:**
- Question titles MUST match the field name constants in the script
- Vehicle dropdown format: `Year Make Model PLATE` (e.g., "2020 Honda Civic ABC-1234")
- File upload field configured to upload to your "Form Upload Temp" folder

### `Drive_Structure.txt`
Recommended Google Drive folder organization.

**Key Folders:**
- One folder per vehicle (for permanent storage of incidents and maintenance records)
- "New Vehicle Archive" (for incidents involving unlisted vehicles)
- "Form Upload Temp" (temporary storage for form uploads before moving)

## Quick Start

1. **Download all template files** from this directory
2. **Follow the step-by-step guide**: [Deployment Guide](../deployment-guide.html)
3. **Test with a sample incident** before rolling out to your team

## Support

- **Full Documentation**: [FleetTracker Overview](../index.html)
- **Technical Details**: [Code Architecture Walkthrough](../technical-walkthrough.html)
- **GitHub Issues**: [Report bugs or request features](https://github.com/Camilleelot/FleetTracker-NGO/issues)

## License

MIT License - Free for nonprofit use. See the main repository for details.

---

**Questions?** Review the [deployment guide](../deployment-guide.html) or open an issue on GitHub.
