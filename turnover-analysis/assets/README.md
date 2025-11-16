# Assets Folder

Place your images here!

## Required Images for Website

### For Publications Page Preview (`/papers/index.html`)
- **sankey-preview.png** (250x250px recommended)
  - Sankey diagram showing employee flow between departments/cases
  - Used as thumbnail on publications page
  - Should show a representative visualization from the tool

### For Documentation/Tool Pages
- **cost-analysis.jpg** - Cost analysis visualization
- **employee-retention-curve.jpg** - Retention curve graph
- **manul-tophat.png** - Distinguished manul in top hat (help/branding image)

## Manul Image

Add your distinguished manul in a top hat image as:
- `manul_tophat.png` (or `.jpg`)

This image will appear on the "Read the Manul" help page and in documentation.

To use it in the app, update `show_manul_help()` function in `app.py`:

```python
# Replace this line:
st.info("🎩 **[Image placeholder: Distinguished manul in top hat goes here]**")

# With:
from PIL import Image
manul_img = Image.open('assets/manul_tophat.png')
st.image(manul_img, caption="A distinguished manul", use_column_width=True)
```

## How to Generate Images from Streamlit App

1. Run the app locally or use the web version
2. Upload sample data
3. Navigate to relevant tabs (Case Analysis for Sankey, Cost Analysis, etc.)
4. Take screenshots or use Plotly's download feature
5. Crop and resize as needed (250x250px for thumbnails)
6. Save to this folder

## Image Guidelines

- Use PNG for diagrams and charts (better for line art and transparency)
- Use JPG for photos
- Optimize file sizes (keep under 500KB for web performance)
- 250x250px works well for publication page thumbnails
