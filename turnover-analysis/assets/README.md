# Assets Folder

Place your images here!

## Manul Image

Add your distinguished manul in a top hat image as:
- `manul_tophat.png` (or `.jpg`)

This image will appear on the "Read the Manul" help page.

To use it in the app, update `show_manul_help()` function in `app.py`:

```python
# Replace this line:
st.info("🎩 **[Image placeholder: Distinguished manul in top hat goes here]**")

# With:
from PIL import Image
manul_img = Image.open('assets/manul_tophat.png')
st.image(manul_img, caption="A distinguished manul", use_column_width=True)
```

## Other Images

You can also add:
- Screenshots for the landing page
- Logo images
- Diagrams
- Whatever else you want!
