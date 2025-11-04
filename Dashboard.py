import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta, timezone
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
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
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

def process_data(df, start_date, end_date):
    """Process the data to create vendor report format"""
    if df is None or df.empty:
        return None, 0, None
    
    df['Item Date'] = pd.to_datetime(df['Item Date'], errors='coerce')
    df = df[df['Order Status'] == 'completed'].copy()
    
    if df.empty:
        return None, 0, None
    
    mask = (df['Item Date'] >= start_date) & (df['Item Date'] <= end_date)
    filtered_df = df[mask].copy()
    
    if filtered_df.empty:
        return None, 0, None
    
    grouped = filtered_df.groupby(['Item Name', 'Item Date']).size().reset_index(name='Quantity')
    pivot_df = grouped.pivot_table(index='Item Name', columns='Item Date', values='Quantity', fill_value=0)
    pivot_df = pivot_df.sort_index(axis=1)
    
    unique_dates = sorted(pivot_df.columns.tolist())
    column_totals = pivot_df.sum(axis=0)
    total_row = pd.DataFrame([column_totals], index=['Total'])
    pivot_df = pd.concat([pivot_df, total_row])
    total_orders = int(filtered_df.shape[0])
    
    return pivot_df, total_orders, unique_dates

def main():
    # Sidebar auto-refresh settings
    with st.sidebar:
        st.header("Settings")
        auto_refresh = st.checkbox("Auto-refresh (every 5 minutes)", value=True)
        refresh_interval = st.slider("Refresh interval (seconds)", 60, 600, 300, 60)
    
    # Default date range (last 3 days)
    default_end = datetime.now().date()
    default_start = default_end - timedelta(days=3)
    
    if 'start_date' not in st.session_state:
        st.session_state.start_date = default_start
    if 'end_date' not in st.session_state:
        st.session_state.end_date = default_end

    # Fetch data
    with st.spinner("Fetching data..."):
        df = fetch_data()
    
    # Refresh button
    col_refresh1, col_refresh2, col_refresh3 = st.columns([1, 1, 1])
    with col_refresh2:
        if st.button("🔄 Refresh Now", use_container_width=True, key="top_refresh"):
            st.cache_data.clear()
            st.rerun()
    
    if auto_refresh:
        mins, secs = divmod(refresh_interval, 60)
        st.info(f"⏱️ Auto-refresh enabled: Page will refresh in {mins:02d}:{secs:02d}")

    # Header and date inputs
    col1, col2, col3 = st.columns([2.5, 4, 2.5])
    
    with col1:
        st.markdown('<div class="main-header">XPRESS SGS VENDOR DETAILS</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
        start_date = st.date_input("Item Date (From)", value=st.session_state.start_date)
        end_date = st.date_input("Item Date (To)", value=st.session_state.end_date)
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        try:
            utc_now = datetime.now(timezone.utc)
            ist = pytz.timezone('Asia/Kolkata')
            ist_now = utc_now.astimezone(ist)
            last_refresh = ist_now.strftime("%d-%m-%Y %I:%M:%S %p IST")
        except:
            last_refresh = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        st.markdown(f'<div class="date-box" style="margin-top: 20px;">Last Refresh Time<br>{last_refresh}</div>', unsafe_allow_html=True)
    
    # Process data and calculate metrics
    if df is not None:
        report_df, total_orders, unique_dates = process_data(df, pd.Timestamp(start_date), pd.Timestamp(end_date))
        df['Item Date'] = pd.to_datetime(df['Item Date'], errors='coerce')
        df_filtered = df[
            (df['Order Status'] == 'completed') &
            (df['Item Date'] >= pd.Timestamp(start_date)) &
            (df['Item Date'] <= pd.Timestamp(end_date))
        ]
        total_item_amount = df_filtered['Payment Amount'].sum() if 'Payment Amount' in df_filtered.columns else 0

        if report_df is not None and not report_df.empty:
            unique_items = len([idx for idx in report_df.index if idx != 'Total'])
            unique_dates_count = len(report_df.columns)
            avg_per_day = total_orders / unique_dates_count if unique_dates_count > 0 else 0
        else:
            unique_items, unique_dates_count, avg_per_day = 0, 0, 0
    else:
        unique_items = unique_dates_count = avg_per_day = total_orders = total_item_amount = 0
    
    # Display metrics only
    col_metric1, col_metric2, col_metric3, col_metric4, col_metric5 = st.columns(5)
    with col_metric1:
        st.metric("📦 Unique Items", unique_items)
    with col_metric2:
        st.metric("📅 Days in Range", unique_dates_count)
    with col_metric3:
        st.metric("📊 Avg Orders/Day", avg_per_day)
    with col_metric4:
        st.metric("💰 Payment Amount", total_item_amount)
    with col_metric5:
        st.metric("🧾 Total Orders", total_orders)

    st.markdown("---")

    # Auto-refresh JavaScript
    if auto_refresh:
        refresh_js = f"""
        <script>
        (function() {{
            setTimeout(function() {{
                window.location.reload();
            }}, {refresh_interval * 1000});
        }})();
        </script>
        """
        st.markdown(refresh_js, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
