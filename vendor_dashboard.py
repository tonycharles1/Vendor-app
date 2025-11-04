import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta, timezone
from io import StringIO, BytesIO
import time
import base64
import os
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
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
        color: #1f1f1f;
    }
    
    .total-orders {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f1f1f;
        margin-bottom: 5px;
    }
    .orders-label {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 20px;
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
    .stDataFrame {
        font-size: 0.9rem;
    }
    /* Yellow header for table */
    .stDataFrame thead th {
        background-color: #FFD66B !important;
        color: #000 !important;
        font-weight: bold !important;
    }
    /* Alternative selector for table headers */
    table thead th {
        background-color: #FFD66B !important;
        color: #000 !important;
        font-weight: bold !important;
    }
    div[data-testid="stDataFrame"] table thead th {
        background-color: #FFD66B !important;
        color: #000 !important;
        font-weight: bold !important;
    }
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Data source URL
DATA_URL = "https://sgs.schoolmanageronline.com/inventoryCafeteriaReportView.php"

# WhatsApp API Configuration
WHATSAPP_API_URL = "https://api.ultramsg.com/"
WHATSAPP_INSTANCE_ID = "instance146293"
WHATSAPP_TOKEN = "kynjwbdp53ktv18w"

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_data():
    """Fetch CSV data from the URL"""
    try:
        response = requests.get(DATA_URL, timeout=10)
        response.raise_for_status()
        # Parse CSV
        df = pd.read_csv(StringIO(response.text))
        return df
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def export_to_excel(df):
    """Export the report DataFrame to Excel format"""
    try:
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Vendor Report', index=True)
        
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error creating Excel file: {str(e)}")
        return None

def send_whatsapp_file(phone_number, file_data, filename, caption=""):
    """Send file via WhatsApp using UltraMsg API"""
    try:
        # UltraMsg API endpoint for sending documents
        url = f"{WHATSAPP_API_URL}/{WHATSAPP_INSTANCE_ID}/messages/document"
        
        # Convert file to base64 for sending as data URL
        # Format: data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{base64_data}
        file_base64 = base64.b64encode(file_data).decode('utf-8')
        document_data_url = f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{file_base64}"
        
        # Prepare form data - UltraMsg expects 'to', 'document' (as URL or base64), and 'filename'
        data = {
            'token': WHATSAPP_TOKEN,
            'to': phone_number,
            'document': document_data_url,
            'filename': filename
        }
        
        # Add caption if provided
        if caption:
            data['caption'] = caption
        
        # Send request as form data
        response = requests.post(url, data=data, timeout=60)
        
        # Check response
        if response.status_code == 200:
            try:
                result = response.json()
                # Check various success indicators
                if (result.get('sent') == True or 
                    result.get('sent') == 'true' or 
                    result.get('success') == True or
                    result.get('error') is None):
                    return True, "File sent successfully via WhatsApp!"
                else:
                    error_msg = result.get('error', result.get('message', 'Unknown error'))
                    return False, f"API Error: {error_msg}"
            except:
                # If response is not JSON, check if it contains success indicators
                if 'sent' in response.text.lower() or 'success' in response.text.lower():
                    return True, "File sent successfully via WhatsApp!"
                else:
                    return False, f"Response: {response.text[:200]}"
        else:
            return False, f"HTTP Error {response.status_code}: {response.text[:200]}"
            
    except requests.exceptions.Timeout:
        return False, "Request timeout - Please try again"
    except requests.exceptions.RequestException as e:
        return False, f"Network error: {str(e)}"
    except Exception as e:
        return False, f"Error sending file: {str(e)}"

def process_data(df, start_date, end_date):
    """Process the data to create vendor report format"""
    if df is None or df.empty:
        return None, 0, None
    
    # Convert Item Date to datetime
    df['Item Date'] = pd.to_datetime(df['Item Date'], errors='coerce')
    
    # Filter by Order Status = 'completed'
    df = df[df['Order Status'] == 'completed'].copy()
    
    if df.empty:
        return None, 0, None
    
    # Filter by date range
    mask = (df['Item Date'] >= start_date) & (df['Item Date'] <= end_date)
    filtered_df = df[mask].copy()
    
    if filtered_df.empty:
        return None, 0, None
    
    # Group by Item Name and Item Date, count orders
    grouped = filtered_df.groupby(['Item Name', 'Item Date']).size().reset_index(name='Quantity')
    
    # Pivot table: Items as rows, Dates as columns
    pivot_df = grouped.pivot_table(
        index='Item Name',
        columns='Item Date',
        values='Quantity',
        fill_value=0
    )
    
    # Sort columns (dates) in ascending order
    pivot_df = pivot_df.sort_index(axis=1)
    
    # Get unique dates for header information
    unique_dates = sorted(pivot_df.columns.tolist())
    
    # Calculate column totals (daily totals) before adding Total column
    column_totals = pivot_df.sum(axis=0)
    
    # Add total row
    total_row = pd.DataFrame([column_totals], index=['Total'])
    pivot_df = pd.concat([pivot_df, total_row])
    
    # Total orders count
    total_orders = int(filtered_df.shape[0])
    
    return pivot_df, total_orders, unique_dates

def main():
    # Auto-refresh configuration
    with st.sidebar:
        st.header("Settings")
        auto_refresh = st.checkbox("Auto-refresh (every 5 minutes)", value=True)
        refresh_interval = st.slider("Refresh interval (seconds)", 60, 600, 300, 60)
    
    # Get date inputs first (needed for data fetching)
    # Default date range (last 2 weeks)
    default_end = datetime.now().date()
    default_start = default_end - timedelta(days=5)
    
    # Use session state to persist date values
    if 'start_date' not in st.session_state:
        st.session_state.start_date = default_start
    if 'end_date' not in st.session_state:
        st.session_state.end_date = default_end
    
    # Fetch and process data early
    with st.spinner("Fetching data..."):
        df = fetch_data()
    

        st.markdown('<div class="main-header">XPRESS SGS VENDOR DETAILS</div>', unsafe_allow_html=True)

    # Refresh button at the top
    col_refresh1, col_refresh2, col_refresh3 = st.columns([1, 1, 1])
    with col_refresh2:
        if st.button("🔄 Refresh Now", use_container_width=True, key="top_refresh"):
            st.cache_data.clear()
            st.rerun()
    
    # Auto-refresh message at the top
    if auto_refresh:
        mins, secs = divmod(refresh_interval, 60)
        st.info(f"⏱️ Auto-refresh enabled: Page will refresh in {mins:02d}:{secs:02d}")
    
    # Header section
    col1, col2, col3 = st.columns([2.5, 4, 2.5])
    
    with col1:
        st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
        
        start_date = st.date_input(
            "Item Date (From)",
            value=st.session_state.start_date,
            key="start_date_input"
        )
        
        end_date = st.date_input(
            "Item Date (To)",
            value=st.session_state.end_date,
            key="end_date_input"
        )
        
        # Update session state
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date
        
        st.markdown('</div>', unsafe_allow_html=True)
    

       
        
    
    with col3:
        # Get current time in IST (Indian Standard Time)
        # IST is UTC+5:30
        try:
            # Get current UTC time
            utc_now = datetime.now(timezone.utc)
            # Convert to IST (UTC+5:30)
            ist = pytz.timezone('Asia/Kolkata')
            ist_now = utc_now.astimezone(ist)
            last_refresh = ist_now.strftime("%d-%m-%Y %I:%M:%S %p IST")
        except Exception as e:
            # Fallback: manual calculation if pytz fails
            try:
                # IST = UTC + 5 hours 30 minutes
                utc_now = datetime.now(timezone.utc)
                ist_offset = timedelta(hours=5, minutes=30)
                ist_now = utc_now + ist_offset
                last_refresh = ist_now.strftime("%d-%m-%Y %I:%M:%S %p IST")
            except:
                # Final fallback to UTC
                utc_now = datetime.now(timezone.utc)
                last_refresh = utc_now.strftime("%d-%m-%Y %I:%M:%S %p UTC")
        st.markdown(f'<div class="date-box" style="margin-top: 20px;">Last Refresh Time<br>{last_refresh}</div>', unsafe_allow_html=True)
    
    # Process data and calculate metrics for display at top
    if df is not None:
        # Process data with current date inputs
        report_df, total_orders, unique_dates = process_data(df, pd.Timestamp(start_date), pd.Timestamp(end_date))
        
        # Calculate metrics for display at top
        if report_df is not None and not report_df.empty:
            unique_items = len([idx for idx in report_df.index if idx != 'Total'])
            unique_dates_count = len([col for col in report_df.columns if col != 'Total'])
            avg_per_day = total_orders / unique_dates_count if unique_dates_count > 0 else 0
        else:
            unique_items = 0
            unique_dates_count = 0
            avg_per_day = 0
    else:
        unique_items = 0
        unique_dates_count = 0
        avg_per_day = 0
        total_orders = 0
        report_df = None
        unique_dates = None
    
    # Display metrics at the top (right after auto-refresh message)
    col_metric1, col_metric2, col_metric3,col_metric4 = st.columns(4)
    with col_metric1:
        st.metric("📦Unique Items", unique_items)
    with col_metric2:
        st.metric("⏳Days in Range", unique_dates_count)
    with col_metric3:
        st.metric("📅Avg Orders/Day", f"{avg_per_day:.1f}")
    with col_metric4:
        st.metric("🧾Total Orders", total_orders)
    
    if df is not None:
        
        
        
        if report_df is not None and not report_df.empty:
            # Format column names for better display
            display_df = report_df.copy()
            
            # Rename date columns to show day number and day name
            new_column_names = {}
            for col in display_df.columns:
                if isinstance(col, pd.Timestamp):
                    day_num = col.strftime('%d')
                    day_name = col.strftime('%a')
                    new_column_names[col] = f"{day_num}\n({day_name})"
                elif col == 'Total':
                    new_column_names[col] = 'Total'
            
            display_df.rename(columns=new_column_names, inplace=True)
            
            # Display header information
            if unique_dates:
                first_date = unique_dates[0]
                year = first_date.year
                months = sorted(set([d.strftime('%B') for d in unique_dates if isinstance(d, pd.Timestamp)]))
                
                st.markdown(f"**Year:** {year} | **Month(s):** {', '.join(months)}")
            
            # Display the main table with styling
            # Use pandas styling for yellow header
            styled_df = display_df.style.set_table_styles([
                {
                    'selector': 'thead th',
                    'props': [
                        ('background-color', 'yellow'),
                        ('color', '#FFD66B'),
                        ('font-weight', 'bold'),
                        ('text-align', 'center')
                    ]
                }
            ])
            
            # Format all numeric columns as whole numbers (no decimals)
            format_dict = {col: '{:.0f}' for col in display_df.columns}
            styled_df = styled_df.format(format_dict)
            
            st.dataframe(
                styled_df,
                use_container_width=True,
                height=400
            )
            
            # WhatsApp send section
            st.markdown("---")
            st.markdown("### 📱 Send Report via WhatsApp")
            
            col_whatsapp1, col_whatsapp2 = st.columns([2, 1])
            
            with col_whatsapp1:
                phone_number = st.text_input(
                    "WhatsApp Number (with country code, e.g., 919876543210)",
                    key="whatsapp_number",
                    placeholder="919876543210"
                )
            
            with col_whatsapp2:
                st.markdown("<br>", unsafe_allow_html=True)  # Spacing
                send_button = st.button("📤 Send Excel Report", use_container_width=True, key="send_whatsapp")
            
            if send_button:
                if not phone_number:
                    st.error("Please enter a WhatsApp number")
                elif not phone_number.replace('+', '').replace(' ', '').replace('-', '').isdigit():
                    st.error("Please enter a valid phone number (numbers only with country code)")
                else:
                    # Clean phone number (remove +, spaces, and dashes)
                    clean_phone = phone_number.replace('+', '').replace(' ', '').replace('-', '')
                    
                    with st.spinner("Creating Excel file and sending via WhatsApp..."):
                        # Export to Excel (use original report_df with proper formatting)
                        # Create a clean copy for Excel export
                        excel_df = report_df.copy()
                        excel_df.index.name = 'Item Name'
                        
                        # Convert numeric columns to integers for Excel
                        for col in excel_df.columns:
                            if col != 'Total':
                                excel_df[col] = excel_df[col].astype(int)
                            else:
                                excel_df[col] = excel_df[col].astype(int)
                        
                        excel_data = export_to_excel(excel_df)
                        
                        if excel_data:
                            # Create filename with date range
                            filename = f"Vendor_Report_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.xlsx"
                            
                            # Send via WhatsApp
                            success, message = send_whatsapp_file(
                                clean_phone,
                                excel_data,
                                filename,
                                caption=f"XPRESS SGS Vendor Report\nDate Range: {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}"
                            )
                            
                            if success:
                                st.success(f"✅ {message}")
                            else:
                                st.error(f"❌ {message}")
                        else:
                            st.error("Failed to create Excel file")
        else:
            st.warning("No data available for the selected date range.")
    else:
        st.error("Unable to fetch data. Please check the connection and try again.")
        # Set default values for metrics when no data
        unique_items = 0
        unique_dates_count = 0
        avg_per_day = 0
    
    # Auto-refresh mechanism using JavaScript
    if auto_refresh:
        # Inject JavaScript to auto-refresh the page
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

