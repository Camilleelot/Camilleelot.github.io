# Deployment Guide

## Option 1: Streamlit Cloud (Recommended for Sharing)

Perfect for sharing with your team without technical setup.

### Steps:

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit of turnover analysis tool"
git remote add origin https://github.com/yourusername/turnover-analysis.git
git push -u origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file: `app.py`
   - Click "Deploy"

3. **Access**
   - Get a public URL like `yourapp.streamlit.app`
   - Share with team members
   - They can upload their own data files

**Pros:**
- Free for public repos
- Easy sharing via URL
- Auto-updates when you push to GitHub
- No server maintenance

**Cons:**
- Data uploaded by users goes through Streamlit's servers (not ideal for sensitive HR data)
- Limited to public repos (unless you have paid plan)

## Option 2: Internal Server (Best for Security)

For sensitive HR data, run on your organization's internal network.

### On Linux/Mac Server:

```bash
# Install dependencies
pip install -r requirements.txt

# Run with custom port
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# Or run in background
nohup streamlit run app.py --server.port 8501 &
```

### On Windows Server:

```cmd
# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py --server.port 8501
```

### Using Docker:

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t turnover-analysis .
docker run -p 8501:8501 turnover-analysis
```

**Pros:**
- Full control over data security
- Can integrate with internal databases
- No external dependencies

**Cons:**
- Requires IT support
- Server maintenance needed

## Option 3: Desktop Application (Single User)

For personal use by one HR manager.

### Using PyInstaller:

```bash
pip install pyinstaller

pyinstaller --onefile --add-data "src:src" --add-data "data:data" app.py
```

This creates a standalone `.exe` (Windows) or binary (Mac/Linux) that can be distributed.

**Pros:**
- No server needed
- Works offline
- Easy for non-technical users

**Cons:**
- Large file size
- Needs rebuilding for updates
- OS-specific

## Security Recommendations

### For Sensitive HR Data:

1. **Use Internal Deployment** (Option 2)
   - Keep data within your network
   - Set up authentication (basic auth, LDAP, SSO)
   - Use HTTPS with proper certificates

2. **Add Authentication**

Add to `app.py`:
```python
import streamlit as st

def check_password():
    """Returns `True` if user had correct password."""
    def password_entered():
        if st.session_state["password"] == "your_secure_password":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password",
                     on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password",
                     on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

# Add before main():
if not check_password():
    st.stop()
```

3. **Database Integration** (Advanced)

Instead of file uploads, pull data from your HRIS:

```python
# Example: Connect to PostgreSQL
import psycopg2

conn = psycopg2.connect(
    host="your-db-host",
    database="hr_database",
    user="readonly_user",
    password="secure_password"
)

df = pd.read_sql("""
    SELECT
        employee_id, name, hire_date, termination_date,
        department, role, salary
    FROM employees
""", conn)
```

## Performance Optimization

For large datasets (>10,000 employees):

1. **Enable Caching**
Already implemented via `@st.cache_data` decorators

2. **Use Parquet Instead of Excel**
```python
df = pd.read_parquet('employees.parquet')
```

3. **Limit Date Ranges**
Add filters to only load recent data

## Monitoring & Maintenance

### Log Usage:
```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

logging.info(f"Data loaded: {len(df)} employees")
```

### Schedule Updates:
Set up cron job (Linux) or Task Scheduler (Windows) to pull fresh data:

```bash
# Run daily at 6 AM
0 6 * * * /path/to/update_data.sh
```

## Support & Customization

### White Labeling:

Edit `app.py`:
```python
st.set_page_config(
    page_title="Your Org Name - HR Analytics",
    page_icon="🏢",
)
```

### Custom Branding:

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor="#your-color"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f0f2f6"
textColor="#262730"
font="sans serif"
```

### Adding Features:

All modules in `src/` are modular. Easy to extend:
- Add new calculations in `src/cohort_analysis.py`
- Add new charts in `src/visualizations.py`
- Add new metrics in `src/predictive.py`

## Questions?

- Check [Streamlit docs](https://docs.streamlit.io)
- Review `README.md` for architecture
- Open an issue on GitHub
