import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timezone
from io import StringIO
import pytz

# Page configuration
st.set_page_config(
    page_title="XPRESS SGS VENDOR DETAILS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS for styling
st.markdown("""
    <style>
div[data-testid="stMetric"]:nth-child(1) { background-color: #e3f2fd; border-color: #211832; }
div[data-testid="stMetric"]:nth-child(2) { background-color: #f1f8e9; border-color: #211832; }
div[data-testid="stMetric"]:nth-child(3) { background-color: #fff3e0; border-color: #211832; }
div[data-testid="stMetric"]:nth-child(4) { background-color: #fce4ec; border-color: #211832; }
div[data-testid="stMetric"]:nth-child(5) { background-color: #ede7f6; border-color: #211832; }

.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
    color: #1f1f1f;
}
.date-box {
    background-color: #ffebee;
    padding: 10px 15px;
    border-radius: 4px;
    border: 2px solid #ffcdd2;
    display: inline-block;
    margin: 5px;
    color: #c62828;
    font-weight: 500;
}
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Data source URL
DATA_URL = "https://sgs.schoolmanageronline.com/inventoryCafeteriaReportView.php"

@st.cache_data(ttl=300)
def fetch_data():
    """Fetch CSV data from the URL"""
    try:
        response = requests.get(DATA_URL, timeout=10)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        return df
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def format_in_indian_style(num):
    """Format number in Indian style with commas"""
    x = int(num)
    s = f"{x:,}"
    parts = s.split(",")
    if len(parts) <= 3:
        return s
    else:
        return parts[0] + "," + ",".join(["".join(parts[1:-2])] + parts[-2:])

def main():
    # Sidebar refresh config
    with st.sidebar:
        st.header("Settings")
        auto_refresh = st.checkbox("Auto-refresh (every 5 minutes)", value=True)
        refresh_interval = st.slider("Refresh interval (seconds)", 60, 600, 300, 60)

    # Fetch data
    with st.spinner("Fetching data..."):
        df = fetch_data()

    # Refresh button
    col_refresh1, col_refresh2, col_refresh3 = st.columns([1, 1, 1])
    with col_refresh2:
        if st.button("🔄 Refresh Now", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    # Auto-refresh message
    if auto_refresh:
        mins, secs = divmod(refresh_interval, 60)
        st.info(f"⏱️ Auto-refresh enabled: Page will refresh in {mins:02d}:{secs:02d}")

    # Header section
    col1, col2, col3 = st.columns([2.5, 4, 2.5])
    with col1:
        st.markdown('<div class="main-header">XPRESS SGS VENDOR DETAILS</div>', unsafe_allow_html=True)
    with col3:
        # Show last refresh time in IST
        try:
            ist = pytz.timezone('Asia/Kolkata')
            ist_now = datetime.now(pytz.utc).astimezone(ist)
            last_refresh = ist_now.strftime("%d-%m-%Y %I:%M:%S %p IST")
        except:
            last_refresh = datetime.now().strftime("%d-%m-%Y %I:%M:%S")
        st.markdown(f'<div class="date-box">Last Refresh Time<br>{last_refresh}</div>', unsafe_allow_html=True)

    # Calculate basic metrics
    if df is not None and not df.empty:
        df['Item Date'] = pd.to_datetime(df['Item Date'], errors='coerce')
        df = df[df['Order Status'] == 'completed']

        total_orders = len(df)
        unique_items = df['Item Name'].nunique()
        total_item_amount = df['Payment Amount'].sum() if 'Payment Amount' in df.columns else 0
        unique_dates = df['Item Date'].dt.date.nunique()
        avg_per_day = int(round(total_orders / unique_dates)) if unique_dates > 0 else 0
    else:
        total_orders = 0
        unique_items = 0
        total_item_amount = 0
        avg_per_day = 0
        unique_dates = 0

    # Format payment amount with ₹ and Indian comma style
    formatted_amount = f"₹{format_in_indian_style(total_item_amount)}"

    # Display metrics
    col_metric1, col_metric2, col_metric3, col_metric4, col_metric5 = st.columns(5)
    with col_metric1:
        st.metric("📦 Unique Items", unique_items)
    with col_metric2:
        st.metric("📅 Days Available", unique_dates)
    with col_metric3:
        st.metric("📊 Avg Orders/Day", f"{avg_per_day}")
    with col_metric4:
        st.metric("💰 Payment Amount", formatted_amount)
    with col_metric5:
        st.metric("🧾 Total Orders", total_orders)

    # Auto-refresh JavaScript
    if auto_refresh:
        refresh_js = f"""
        <script>
        setTimeout(() => window.location.reload(), {refresh_interval * 1000});
        </script>
        """
        st.markdown(refresh_js, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
