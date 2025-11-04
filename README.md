# XPRESS SGS Vendor Dashboard

A Python dashboard for viewing cafeteria vendor reports with automatic data refresh and WhatsApp integration.

## Features

- 📊 Real-time vendor report dashboard
- 🔄 Automatic data refresh (configurable interval)
- 📅 Date range filtering
- 📈 Item-wise order statistics by date
- 🎨 Clean, modern UI matching the original report design
- 📱 WhatsApp integration for sending Excel reports
- 📤 Export reports to Excel format

## Local Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the dashboard:
```bash
streamlit run vendor_dashboard.py
```

## Deployment to Streamlit Cloud (Recommended)

### Step 1: Push to GitHub

1. Create a new repository on GitHub (if you haven't already)
2. Initialize git and push your code:
```bash
git init
git add .
git commit -m "Initial commit - Vendor Dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch
5. Set the main file path to: `vendor_dashboard.py`
6. Click "Deploy"

Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

## Alternative Deployment Options

### Railway.app
1. Sign up at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Add a `Procfile` with: `web: streamlit run vendor_dashboard.py --server.port $PORT`
4. Railway will auto-detect and deploy

### Render.com
1. Sign up at [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run vendor_dashboard.py --server.port $PORT --server.address 0.0.0.0`

## Configuration

- **Data Source**: Configured in `vendor_dashboard.py` (DATA_URL)
- **Auto-refresh**: Toggle in sidebar, adjust interval (60-600 seconds)
- **Date Range**: Select using date picker in the header
- **WhatsApp API**: Configured in `vendor_dashboard.py` (WHATSAPP_API_URL, WHATSAPP_INSTANCE_ID, WHATSAPP_TOKEN)

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- Requests
- openpyxl (for Excel export)

## Data Format

The dashboard expects CSV data with the following columns:
- Item Name
- Item Date
- Order Status
- Item Amount
- And other cafeteria order fields

## WhatsApp Integration

The dashboard includes WhatsApp integration using UltraMsg API:
- Enter recipient's phone number with country code
- Click "Send Excel Report" to send the report as an Excel file
- Requires valid UltraMsg API credentials

