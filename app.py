import streamlit as st  # Import Streamlit framework for web app interface
import pandas as pd  # Import Pandas for data manipulation and analysis
import numpy as np  # Import NumPy for numerical calculations
import plotly.express as px  # Import Plotly Express for quick interactive charts
import plotly.graph_objects as go  # Import Plotly Graph Objects for custom charts 
from plotly.subplots import make_subplots 

     
# Configure page settings (title, tab icon, and layout behavior)
st.set_page_config(
    page_title="Ethiopia Coffee Market Dashboard",  # Set the title shown on browser tab
    page_icon="☕",  # Set the icon shown on browser tab
    layout="wide",  # Force layout to span full browser width
    initial_sidebar_state="expanded"  # Keep sidebar expanded by default
)

# Apply global CSS styling for full-width layout and compact spacing
st.markdown("""
<style>
header[data-testid="stHeader"] {
    display:none;  /* Hide the default top Streamlit header bar */
}
.block-container {
    padding-top: 0rem !important;  /* Remove top page padding */
    padding-bottom: 0rem !important;  /* Remove bottom page padding */
    padding-left: 0rem !important;  /* Remove left page padding */
    padding-right: 0rem !important;  /* Remove right page padding */
    max-width: 100% !important;  /* Force maximum width to 100% */
}
div[data-testid="stVerticalBlock"] {
    gap: 0rem !important;  /* Remove spacing between stacked components */
}
div[data-testid="stVerticalBlock"] > div {
    gap: 0rem !important;  /* Remove inner spacing between layout divs */
    margin-bottom: 0.1rem !important;  /* Reduce space below components */
}
h1, h2, h3 {
    margin-top: 0.8rem !important;  /* Adjust top margins for all headings */
    margin-bottom: 0.2rem !important;  /* Adjust bottom margins for all headings */
    padding-top: 0.2rem !important;  /* Adjust top padding for headings */
    padding-bottom: 0.2rem !important;  /* Adjust bottom padding for headings */
}
div[data-testid="stHorizontalBlock"] {
    gap: 0.3rem !important;  /* Reduce horizontal gap between columns */
}
</style>
""", unsafe_allow_html=True)  # Apply raw CSS styles to the Streamlit app

st.sidebar.title(" Navigation")  # Set sidebar navigation section title
app_mode = st.sidebar.radio(  # Display radio selection for app operating mode
    "Select Operating dashboard:",  # Radio button selection label
    [
        "☕ dashboard 1: Ethiopia Coffee Market Analytics",  # First application mode option
        "📁 dashboard 2: Dynamic Upload & Analytics dashboard",  # Second application mode option
    ],
)
st.sidebar.markdown("---")  # Add horizontal separator line in sidebar

if app_mode == "☕ dashboard 1: Ethiopia Coffee Market Analytics":  # If user selects dashboard 1

    st.markdown(  # Render top header banner for dashboard 1 using custom HTML
        """
<div style="background-color: #4A2C11; padding: 15px; border-radius: 6px; color: white; margin-bottom: 2px;">   
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <h1 style="margin: 0; color: white; font-size: 2rem;">☕ Ethiopia Coffee Market And Dynamic Upload & Analytics dashboard</h1>   
        <div style="text-align: right; whitespace: nowrap;">
    
</div>
    """,
        unsafe_allow_html=True,  # Allow inline HTML rendering
    )  

    @st.cache_data  # Cache dataset in memory to optimize app performance
    def load_data():  # Function to safely load and preprocess dataset
        try:  # Try block to read dataset from CSV file
            df = pd.read_csv("cleaned_coffee_data.csv")  # Load cleaned dataset into DataFrame
            df["Year"] = pd.to_numeric(df["Year"], errors="coerce")  # Cast Year column to numeric
            df["Day"] = pd.to_numeric(df["Day"], errors="coerce")  # Cast Day column to numeric
            return df  # Return processed DataFrame
        except Exception:  # Handle missing file or parsing exceptions
            return pd.DataFrame()  # Return empty DataFrame as fallback

    df = load_data()  # Execute data loading function and store result

    st.sidebar.header("🔎 Filters")  # Render filter header in sidebar
    st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Add minor vertical spacing

    if st.sidebar.button("🔄 Reset Filters"):  # Reset button to clear selected filters
        st.session_state["year_filter"] = "All"  # Reset year selection to All
        st.session_state["month_filter"] = "All"  # Reset month selection to All
        st.session_state["day_filter"] = "All"  # Reset day selection to All
        st.session_state["warehouse_filter"] = "All"  # Reset warehouse selection to All
        st.session_state["symbol_filter"] = "All"  # Reset symbol selection to All
        st.rerun()  # Trigger full app rerun to reflect reset state

    if not df.empty:  # If dataset loaded successfully and is not empty
        year_options = sorted(df["Year"].dropna().astype(int).unique().tolist())  # Extract unique sorted years
        selected_year = st.sidebar.selectbox("Select Year", options=["All"] + year_options, key="year_filter")  # Year select dropdown

        month_options = sorted(df["Month"].dropna().unique().tolist())  # Extract unique sorted months
        selected_month = st.sidebar.selectbox("Select Month", options=["All"] + month_options, key="month_filter")  # Month select dropdown

        day_options = sorted(df["Day"].dropna().astype(int).unique().tolist())  # Extract unique sorted days
        selected_day = st.sidebar.selectbox("Select Day", options=["All"] + day_options, key="day_filter")  # Day select dropdown

        warehouse_options = sorted(df["Warehouse"].dropna().unique().tolist())  # Extract unique sorted warehouses
        selected_warehouse = st.sidebar.selectbox("Select Warehouse", options=["All"] + warehouse_options, key="warehouse_filter")  # Warehouse select dropdown

        symbol_options = sorted(df["Symbol"].dropna().unique().tolist())  # Extract unique sorted coffee symbols
        selected_symbol = st.sidebar.selectbox("Select Coffee Symbol", options=["All"] + symbol_options, key="symbol_filter")  # Symbol select dropdown

        filtered_df = df.copy()  # Create working copy of DataFrame for filtering
        if selected_year != "All":  # Filter by selected year
            filtered_df = filtered_df[filtered_df["Year"] == selected_year]  # Apply year filter
        if selected_month != "All":  # Filter by selected month
            filtered_df = filtered_df[filtered_df["Month"] == selected_month]  # Apply month filter
        if selected_day != "All":  # Filter by selected day
            filtered_df = filtered_df[filtered_df["Day"] == selected_day]  # Apply day filter
        if selected_warehouse != "All":  # Filter by selected warehouse
            filtered_df = filtered_df[filtered_df["Warehouse"] == selected_warehouse]  # Apply warehouse filter
        if selected_symbol != "All":  # Filter by selected coffee symbol
            filtered_df = filtered_df[filtered_df["Symbol"] == selected_symbol]  # Apply symbol filter
    else:  # If dataset is empty
        filtered_df = pd.DataFrame()  # Initialize empty DataFrame

    st.sidebar.success(f"Total Records: {len(filtered_df):,}")  # Display total count of filtered records

    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        background-color: #4A2C11 !important;  /* Set custom dark brown background for sidebar */
        border-right: 0px solid #DDD;  /* Remove sidebar right border */
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: white !important;  /* Force all sidebar headings to white */
    }
    section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p {
        color: #F5E6CA !important;  /* Set light cream color for input labels */
        font-weight: 600 !important;  /* Set semi-bold font weight for labels */
        font-size: 1rem !important;  /* Set font size for input labels */
    }
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
        color: #F5E6CA !important;  /* Set general text color in sidebar */
    }
    section[data-testid="stSidebar"] .stAlert {
        color: white !important;  /* Set alert component text color in sidebar */
    }
    </style>
    """, unsafe_allow_html=True)  # Apply sidebar styling rules

    st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: #D4AF37;  /* Set metric card background color (gold) */
        padding: 2px 2px !important;  /* Apply compact padding inside cards */
        border-radius: 10px;  /* Apply rounded corners to metric cards */
        border: 1px solid #B8860B;  /* Apply subtle border line around cards */
        box-shadow: 0px 2px 5px rgba(0,0,0,0.15);  /* Apply subtle drop shadow */
        min-height: 5px !important;  /* Set minimal card height */
    }
    div[data-testid="stMetricLabel"] {
        color: #3E2723 !important;  /* Set dark brown font color for metric labels */
        font-size: 8px !important;  /* Set small font size for metric labels */
        font-weight: 600 !important;  /* Set semi-bold weight for metric labels */
        line-height: 1.2 !important;  /* Set line height for label text */
    }
    div[data-testid="stMetricValue"] {
        color: #2E1B0E !important;  /* Set main metric value color */
        font-size: 15px !important;  /* Set metric numeric value font size */
        font-weight: 700 !important;  /* Set bold weight for metric values */
        line-height: 1.2 !important;  /* Set line height for values */
    }
    div[data-testid="column"] {
        padding-left: 0px;  /* Remove left padding from grid columns */
        padding-right: 0px;  /* Remove right padding from grid columns */
    }
    </style>
    """, unsafe_allow_html=True)  # Apply custom CSS styling for metric components

    st.markdown("""
    <div style="background-color:#1B5E20; color:white; font-size:15px; font-weight:700;
    padding:6px 10px; border-radius:8px; text-align:center; margin-top:0px; margin-bottom:15px;">
     Key Performance Indicators (KPIs) Overview
    </div>
    """, unsafe_allow_html=True)  # Render green header bar for KPI section
    
      ## kpi

    if not filtered_df.empty:  # Compute aggregations if filtered dataset is non-empty
        total_volume = filtered_df["Volume (Ton)"].sum() if "Volume (Ton)" in filtered_df.columns else 0  # Calculate total volume
        avg_opening = filtered_df["Opening Price"].mean() if "Opening Price" in filtered_df.columns else 0  # Calculate mean opening price
        avg_closing = filtered_df["Closing Price"].mean() if "Closing Price" in filtered_df.columns else 0  # Calculate mean closing price
        highest_price = filtered_df["High"].max() if "High" in filtered_df.columns else 0  # Find peak recorded price
        lowest_price = filtered_df["Low"].min() if "Low" in filtered_df.columns else 0  # Find lowest recorded price
        total_warehouses = filtered_df["Warehouse"].nunique() if "Warehouse" in filtered_df.columns else 0  # Count distinct warehouses
        total_symbols = filtered_df["Symbol"].nunique() if "Symbol" in filtered_df.columns else 0  # Count distinct coffee symbols
    else:  # Set zero defaults if dataset is empty
        total_volume, avg_opening, avg_closing, highest_price, lowest_price, total_warehouses, total_symbols = 0, 0, 0, 0, 0, 0, 0

    yoy_str = "N/A"  # Set default value for Year-over-Year growth
    try:  # Try block to calculate YoY growth percentage
        if not filtered_df.empty and selected_year == "All":  # Compute only when all years selected
            yearly_avg = filtered_df.groupby("Year")["Closing Price"].mean().reset_index().sort_values("Year")  # Yearly average closing prices
            if len(yearly_avg) >= 2:  # Ensure at least two years are available
                latest_price = yearly_avg.iloc[-1]["Closing Price"]  # Get most recent year closing price
                prev_price = yearly_avg.iloc[-2]["Closing Price"]  # Get previous year closing price
                if prev_price > 0:  # Prevent division by zero
                    growth = ((latest_price - prev_price) / prev_price) * 100  # Compute percentage growth
                    yoy_str = f"{growth:+.2f}%"  # Format string with explicit sign and two decimals
    except Exception:  # Handle runtime calculation exceptions
        yoy_str = "N/A"  # Fallback to N/A on exception

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)  # Partition layout into 8 equal width columns
    with col1: st.metric(" Total Volume", f"{total_volume:,.0f} Ton")  # Render Total Volume metric
    with col2: st.metric(" Avg Opening", f"{avg_opening:,.2f} ETB")  # Render Average Opening Price metric
    with col3: st.metric(" Avg Closing", f"{avg_closing:,.2f} ETB")  # Render Average Closing Price metric
    with col4: st.metric(" Highest Price", f"{highest_price:,.2f} ETB")  # Render Highest Price metric
    with col5: st.metric(" Lowest Price", f"{lowest_price:,.2f} ETB")  # Render Lowest Price metric
    with col6: st.metric(" Warehouses", total_warehouses)  # Render Unique Warehouses metric
    with col7: st.metric(" Symbols", total_symbols)  # Render Unique Coffee Symbols metric
    with col8: st.metric(" YoY Growth", yoy_str)  # Render Year-over-Year Growth metric
    
    ## insights

    st.markdown("""
    <div style="background-color:#8B0000; color:white; font-size:15px; font-weight:700;
    padding:8px 12px; border-radius:8px; text-align:center; margin-top:0px; margin-bottom:15px;">
     Market insight summary
    </div>
    """, unsafe_allow_html=True)  # Render dark red section title for market insights

    def create_blue_card(title, value, subtext="", bg_color="#0F172A", border_color="#3B82F6",
                         text_color="#F8FAFC", sub_color="#94A3B8"):  # Function to generate custom styled card
        subtext_html = f'<p style="margin: 2px 0 0 0; font-size: 12px; color: {border_color}; font-weight: 700; line-height: 1.1;">{subtext}</p>' if subtext else ""  # Build subtext HTML string
        html_code = f"""
        <div style="background-color: #4A2C11; border-left: 4px solid {border_color}; 
        padding: 6px 0px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.15); margin-bottom: 10px; margin-top: 0.8rem !important; height: 50%; display: flex; flex-direction: column; justify-content: center;">
            <p style="margin: 0; font-size: 15px; color: {sub_color}; font-weight: 600; 
            line-height: 0;">{title}</p>
            <h3 style="margin: 2px 0; color: {text_color}; font-size: 15px; font-weight: bold; 
            line-height: 1.1;">{value}</h3>
            {subtext_html}
        </div>
        """  # Construct complete HTML structure for individual insight card
        return st.markdown(html_code, unsafe_allow_html=True)  # Render HTML component directly to Streamlit

    if not filtered_df.empty:  # Derive analytical metrics if data exists
        # Yearly average closing price
        yearly_price = filtered_df.groupby("Year")["Closing Price"].mean().reset_index()  
        # Identify year with highest average price
        best_price_year = yearly_price.loc[yearly_price["Closing Price"].idxmax(), "Year"] if not yearly_price.empty else "N/A" 
        # Peak yearly average price 
        highest_avg_price = yearly_price["Closing Price"].max() if not yearly_price.empty else 0 
         
 # Total volume grouped by year
        yearly_volume = filtered_df.groupby("Year")["Volume (Ton)"].sum().reset_index()
        # Identify year with peak trade volume 
        peak_vol_year = yearly_volume.loc[yearly_volume["Volume (Ton)"].idxmax(), "Year"] if not yearly_volume.empty else "N/A"  
        # Maximum aggregated yearly volume
        peak_volume = yearly_volume["Volume (Ton)"].max() if not yearly_volume.empty else 0 
         # Average monthly closing prices
        monthly_price = filtered_df.groupby("Month")["Closing Price"].mean().reset_index() if "Month" in filtered_df.columns else pd.DataFrame() 
        # Month with highest price average
        peak_month = monthly_price.loc[monthly_price["Closing Price"].idxmax(), "Month"] if not monthly_price.empty else "N/A" 
        # Most heavily traded symbol
        top_symbol = filtered_df.groupby("Symbol")["Volume (Ton)"].sum().idxmax() if "Symbol" in filtered_df.columns else "N/A" 
         # Warehouse handling highest volume 
        top_warehouse = filtered_df.groupby("Warehouse")["Volume (Ton)"].sum().idxmax() if "Warehouse" in filtered_df.columns else "N/A" 
        # Evaluate overall price direction trend

        trend = " Upward" if len(yearly_price) > 1 and yearly_price["Closing Price"].iloc[-1] >= yearly_price["Closing Price"].iloc[0] else "➡️ Stable" 
         # Calculate percentage of positive trading days
 
        gain_ratio = ((filtered_df["Change"] > 0).sum() / len(filtered_df)) * 100 if "Change" in filtered_df.columns else 0 
        df_gainer_calc = filtered_df.copy()  # Create copy for top gainers computation
        # Compute percentage change if missing
        if "Percentage Change (%)" not in df_gainer_calc.columns and "Opening Price" in df_gainer_calc.columns:  
            df_gainer_calc["Percentage Change (%)"] = ((df_gainer_calc["Closing Price"] - df_gainer_calc["Opening Price"]) / df_gainer_calc["Opening Price"]) * 100  # Percentage change formula
         # Validate percentage column exists
        pct_col = "Percentage Change (%)" if "Percentage Change (%)" in df_gainer_calc.columns else "" 
        if pct_col:  # If percentage column exists
            avg_gain = df_gainer_calc.groupby("Symbol")[pct_col].mean()  # Mean gain grouped by symbol
            top_gainer_symbol = avg_gain.idxmax() if not avg_gain.empty else "N/A"  # Highest gainer symbol
            top_gainer_val = avg_gain.max() if not avg_gain.empty else 0  # Highest average gain value
        else:  # If column absent
            top_gainer_symbol, top_gainer_val = "N/A", 0  # Fallback default values
            
     # Create second row of 8 columns for insight cards
     
        c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)  
        with c1: create_blue_card(" Top Symbol", top_symbol, "Most Traded",
                                  "#0F172A", "#3B82F6", "#FFFFFF", "#94A3B8")  # Top symbol insight card
        with c2: create_blue_card(" Best Price Year", str(best_price_year),
                                  f"{highest_avg_price:,.0f} ETB", "#0F172A", 
                                  "#3B82F6", "#FFFFFF", "#94A3B8")  # Best price year insight card
        with c3: create_blue_card(" Price Trend", trend, "Market Direction",
                                  "#0F172A", "#3B82F6", "#FFFFFF", "#94A3B8")  # Market trend insight card
        with c4: create_blue_card(" Top Warehouse", top_warehouse, "Top Location",
                                  "#0F172A", "#3B82F6", "#FFFFFF", "#94A3B8")  # Top warehouse insight card
        with c5: create_blue_card(" Gain Ratio", f"{gain_ratio:.1f}%", "Positive Days",
                                  "#1E293B", "#4ADE80", "#FFFFFF", "#CBD5E1")  # Gain ratio insight card
        with c6: create_blue_card(" Peak Volume Year", str(peak_vol_year),
                                  f"{peak_volume:,.0f} Ton", "#1E293B",
                                  "#60A5FA", "#FFFFFF", "#CBD5E1")  # Peak volume year insight card
        with c7: create_blue_card(" Peak Month", str(peak_month),
                                  "Highest Avg Price", "#1E293B",
                                  "#60A5FA", "#FFFFFF", "#CBD5E1")  # Peak month insight card
        with c8: create_blue_card(" Top Gainer", top_gainer_symbol,
                                  f"+{top_gainer_val:.2f}% Avg", "#1E293B", "#22C55E",
                                  "#FFFFFF", "#CBD5E1")  # Top gainer insight card
    else:  # If dataset empty
        st.warning("⚠️ No data available for selected filters.")  # Display warning alert message
        
        ## Visualizations

    col1, col2, col3, col4 = st.columns(4)  # Create 4 columns for first row of charts
    
    with col1:  # 1. Bar Chart: Top Traded Coffee Symbols
        top_symbols = filtered_df.groupby("Symbol")["Volume (Ton)"].sum().reset_index().sort_values("Volume (Ton)", ascending=False).head(10) if not filtered_df.empty else pd.DataFrame()  # Extract top 10 symbols by volume
        fig_symbol = px.bar(top_symbols, x="Symbol", y="Volume (Ton)", title=" Top Symbols")  # Create bar chart instance
        fig_symbol.update_layout(template="plotly_white", height=200, margin=dict(t=40, b=5, l=0, r=0),
                                 plot_bgcolor="#F5F1E8", paper_bgcolor="#F5F1E8", showlegend=False,
                                 title_x=0.25,  # Customize layout
                                  xaxis=dict(tickangle=45))  # Rotate X-axis date labels by 45 degrees
        fig_symbol.update_traces(marker_color="#2C1D11")  # Set bar color to dark brown
        st.plotly_chart(fig_symbol, use_container_width=True, config={"displayModeBar": False})  # Display chart

    with col2:  # 2. Bar Chart: Yearly Price Distribution
        yearly_market = filtered_df.groupby("Year").agg({"Closing Price": "mean", "Volume (Ton)": "sum"}).reset_index() if not filtered_df.empty else pd.DataFrame()  # Group by year and calculate aggregations
        fig_yearly = px.bar(yearly_market, x="Year", y="Closing Price",
                            title="Yearly Price")  # Create bar chart instance
        fig_yearly.update_layout(template="plotly_white", height=200,
                                 margin=dict(t=40, b=5, l=0, r=0), plot_bgcolor="#F5F1E8",
                                 paper_bgcolor="#F5F1E8", showlegend=False, title_x=0.25)  # Customize layout
        fig_yearly.update_traces(marker_color="#3D2314")  # Set bar color
        st.plotly_chart(fig_yearly, use_container_width=True, config={"displayModeBar": False})  # Display chart

    with col3:  # 3. Line Chart: Monthly Price Trend
        temp_df = filtered_df.copy() if not filtered_df.empty else pd.DataFrame()  # Create working copy of DataFrame
        if not temp_df.empty and "Trade Date" in temp_df.columns:  # Check if Trade Date exists
            temp_df["Trade Date"] = pd.to_datetime(temp_df["Trade Date"], errors="coerce")  # Convert column to datetime
            monthly_p = temp_df.dropna(subset=["Trade Date"]).set_index("Trade Date").resample("ME")["Closing Price"].mean().reset_index()  # Resample monthly average
            fig_price = px.line(monthly_p, x="Trade Date", y="Closing Price", title=" Price Trend")  # Create line chart instance
            fig_price.update_layout(template="plotly_white", height=200, margin=dict(t=40, b=20, l=0, r=0),
                                    plot_bgcolor="#F5F1E8", paper_bgcolor="#F5F1E8", title_x=0.25)  # Customize layout
            fig_price.update_traces(line=dict(color="#121212", width=2))  # Set line width and color
            st.plotly_chart(fig_price, use_container_width=True, config={"displayModeBar": False})  # Display chart

    with col4:  # 4. Bar Chart: Warehouse Volume Distribution
        warehouse_volume = filtered_df.groupby("Warehouse")["Volume (Ton)"].sum().reset_index().sort_values("Volume (Ton)", ascending=False) if not filtered_df.empty else pd.DataFrame()  # Aggregate volume by warehouse
        fig_warehouse = px.bar(warehouse_volume, x="Warehouse", y="Volume (Ton)", title=" Warehouse Volume")  # Create bar chart instance
        fig_warehouse.update_layout(template="plotly_white", height=200, margin=dict(t=40, b=5, l=0, r=0), 
                                    plot_bgcolor="#F5F1E8", 
                                    paper_bgcolor="#F5F1E8", title_x=0.2)  # Customize layout
        fig_warehouse.update_traces(marker_color="#264653")  # Set custom marker color
        st.plotly_chart(fig_warehouse, use_container_width=True, config={"displayModeBar": False})  # Display chart

    col1, col2, col3, col4 = st.columns(4)  # Create 4 columns for second row of charts
    
    with col1:  # 5. Line Chart: High vs Low Price Comparison
        if not filtered_df.empty and "Trade Date" in filtered_df.columns:  # Validate non-empty data and Trade Date column
            df_temp = filtered_df.copy()  # Create working copy
            df_temp["Trade Date"] = pd.to_datetime(df_temp["Trade Date"], errors="coerce")  # Parse datetimes
            df_monthly_range = df_temp.dropna(subset=["Trade Date"]).set_index("Trade Date").resample("ME").agg({"High": "max", "Low": "min"}).reset_index()  # Monthly max high and min low
            df_melted = df_monthly_range.melt(id_vars=["Trade Date"], value_vars=["High", "Low"], 
                                              var_name="Price Type", value_name="Price (ETB)")  # Unpivot DataFrame for multi-line plot
                                # Multi-line plot
            fig_high_low = px.line(df_melted, x="Trade Date", y="Price (ETB)", color="Price Type",
                                   title=" High vs Low", color_discrete_map={"High":"#2A9D8F", "Low": "#C87D55"})  
            fig_high_low.update_layout(template="plotly_white",
                                       height=200, plot_bgcolor="#F5F1E8", 
                                       paper_bgcolor="#F5F1E8", title_x=0.15,
                                       margin=dict(t=40, b=5, l=0, r=0)) # Customize layout
                                          
            st.plotly_chart(fig_high_low, use_container_width=True, config={"displayModeBar": False})  # Display chart

    with col2:  # 6. Bar Chart: Yearly Volume Trend
        if not filtered_df.empty and "Trade Date" in filtered_df.columns:  # Check prerequisites
            df_vol = filtered_df.copy()  # Create copy
            df_vol["Trade Date"] = pd.to_datetime(df_vol["Trade Date"], errors="coerce")  # Parse dates
            df_vol["Year"] = df_vol["Trade Date"].dt.year  # Extract year component
            df_y_vol = df_vol.groupby("Year")["Volume (Ton)"].sum().reset_index()  # Aggregate annual volume
            fig_y_vol = px.bar(df_y_vol, x="Year", y="Volume (Ton)", title=" Volume Trend")  # Create bar chart instance
            fig_y_vol.update_layout(template="plotly_white", height=200, plot_bgcolor="#FAF6EE", 
                                    # Customize layout
                                    paper_bgcolor="#FAF6EE", title_x=0.15, margin=dict(t=40, b=5, l=0, r=0))  
            fig_y_vol.update_traces(marker_color="#0F172A")  # Set dark bar color
            st.plotly_chart(fig_y_vol, use_container_width=True, config={"displayModeBar": False})  # Display chart

    with col3:  # 7. Line Chart: Monthly Seasonality Trend
        if not filtered_df.empty and "Trade Date" in filtered_df.columns:  # Check prerequisites
            df_s = filtered_df.copy()  # Create copy
            df_s["Trade Date"] = pd.to_datetime(df_s["Trade Date"], errors="coerce")  # Parse dates
            df_s["Month_Name"] = df_s["Trade Date"].dt.month_name()  # Extract full month names
            # Define correct chronological month order
            m_order = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]  
            m_pattern = df_s.groupby("Month_Name")["Closing Price"].mean().reset_index()  # Calculate average price per month
            m_pattern["Month_Name"] = pd.Categorical(m_pattern["Month_Name"], categories=m_order, ordered=True)  # Apply categorical ordering
            m_pattern = m_pattern.sort_values("Month_Name")  # Sort DataFrame by month order
            # Create line chart with markers
            fig_season = px.line(m_pattern, x="Month_Name", y="Closing Price",
                                 markers=True, title="Seasonality")  
            fig_season.update_traces(line=dict(color="#2C1D11", width=2))  # Customize line properties
             # Customize layout
            fig_season.update_layout(template="plotly_white", height=200, plot_bgcolor="#F5F1E8",
                                     paper_bgcolor="#F5F1E8", 
                                     title_x=0.15, margin=dict(t=40, b=5, l=0, r=0), 
                                      xaxis=dict(tickangle=45))  # Rotate X-axis date labels by 45 degrees
            st.plotly_chart(fig_season, use_container_width=True, config={"displayModeBar": False})  # Display chart

    with col4:  # 8. Horizontal Bar Chart: Top 5 Price Gainers
        if not filtered_df.empty:  # If dataset non-empty
            df_g = filtered_df.copy()  # Create working copy
            if "Percentage Change (%)" not in df_g.columns and "Opening Price" in df_g.columns:  # Calculate percentage change if needed
                df_g["Percentage Change (%)"] = ((df_g["Closing Price"] - df_g["Opening Price"]) / df_g["Opening Price"]) * 100  # Compute percentage change
            if "Percentage Change (%)" in df_g.columns:  # Check column presence
                top_g_df = df_g.groupby("Symbol")["Percentage Change (%)"].mean().reset_index().sort_values("Percentage Change (%)", ascending=True).tail(5)  # Get top 5 gainers
                # Create horizontal bar chart
                fig_g = px.bar(top_g_df, x="Percentage Change (%)", y="Symbol", orientation="h",
                               title=" Top 5 Gainers (%)")  
                fig_g.update_traces(marker_color="#4A2E19", texttemplate="%{x:.2f}%", textposition="outside")  # Format bar text labels
                # Customize layout
                fig_g.update_layout(template="plotly_white", height=200, plot_bgcolor="#F5F1E8", 
                                    paper_bgcolor="#F5F1E8", title_x=0.15,
                                    margin=dict(t=40, b=10, l=0, r=30))  
                   
                        
                st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar": False})  # Display chart
                
    with st.expander("2️⃣ Year vs Warehouse", expanded=False):

                   cross_tab_2 = pd.pivot_table(
                       filtered_df,
                       index="Year",
                       columns="Warehouse",
                       values="Volume (Ton)",
                       aggfunc="sum",
                       fill_value=0
                )

                   st.dataframe(
                   cross_tab_2,
                   use_container_width=True
                )
                
               ### Forecasting section    
                
    st.markdown("""
    <div style="background-color: #4A2C11; color:white; font-size:15px; font-weight:700;
    padding:8px 12px; border-radius:8px; text-align:center; margin-top:15px; margin-bottom:15px;">
     3-Year Price Forecast Model
    </div>
    """, unsafe_allow_html=True)  # Render forecasting section banner title

    forecast_data = filtered_df.copy() if not filtered_df.empty else pd.DataFrame()  # Copy dataset for forecast modeling
    if not forecast_data.empty and "Trade Date" in forecast_data.columns:  # Check data validity
        forecast_data["Trade Date"] = pd.to_datetime(forecast_data["Trade Date"], errors="coerce")  # Parse dates
        forecast_data = forecast_data.dropna(subset=["Trade Date", "Closing Price"])  # Clean missing date/price rows

        if not forecast_data.empty:  # Ensure clean dataset is non-empty
            monthly_price = forecast_data.groupby(forecast_data["Trade Date"].dt.to_period("M"))["Closing Price"].mean().reset_index()  # Aggregate prices monthly
            monthly_price["Trade Date"] = monthly_price["Trade Date"].dt.to_timestamp()  # Convert period index back to timestamp
            monthly_price = monthly_price.sort_values("Trade Date").reset_index(drop=True)  # Sort by timestamp

            if len(monthly_price) >= 6:  # Require at least 6 months of data for forecasting
                last_date = monthly_price["Trade Date"].iloc[-1]  # Get latest historic date
                last_price = monthly_price["Closing Price"].iloc[-1]  # Get latest historic price
                future_dates = [last_date + pd.DateOffset(months=i) for i in range(1, 37)]  # Generate 36 future month dates
                recent_trend = (monthly_price["Closing Price"].iloc[-1] - monthly_price["Closing Price"].iloc[-6]) / 5  # Calculate 5-month linear slope trend
                forecast_prices = [last_price + (recent_trend * i) for i in range(1, 37)]  # Project future prices based on linear slope

                forecast_df = pd.DataFrame({"Trade Date": future_dates, "Closing Price": forecast_prices})  # Construct forecast DataFrame

                fig_trend = go.Figure()  # Initialize empty Plotly Graph Objects figure
                # Plot historic line trace
                fig_trend.add_trace(go.Scatter(x=monthly_price["Trade Date"], y=monthly_price["Closing Price"], 
                                               mode="lines", name="Historical Price", line=dict(color="#4A2C11", width=2)))  
# Connect historic and future X axes
                forecast_x = pd.concat([monthly_price[["Trade Date"]].tail(1), forecast_df[["Trade Date"]]], 
                                       ignore_index=True)["Trade Date"]  
                forecast_y = pd.concat([monthly_price[["Closing Price"]].tail(1), forecast_df[["Closing Price"]]], ignore_index=True)["Closing Price"]  # Connect historic and future Y axes
# Plot forecast dotted line trace
                fig_trend.add_trace(go.Scatter(x=forecast_x, y=forecast_y, mode="lines+markers",
                                               name="3-Year Forecast", line=dict(color="#E67E22", width=2, dash="dot")))  

                fig_trend.update_layout(  # Set forecast figure styling and layout dimensions
                    title=" Coffee Price Trend --- 3-Year Forecast",
                    margin=dict(l=10, r=10, t=40, b=10),
                    height=280,
                    template="plotly_white",
                    plot_bgcolor="#F5F1E8",
                    paper_bgcolor="#F5F1E8"
                )
                st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})  # Display forecast chart
            else:  # If dataset has fewer than 6 monthly observations
                st.info("At least 6 months of historical data is required for the 3-year forecast.")  # Display information notice
           ## Executive Summary and Dataset Table
    with st.expander("📌 Executive Summary", expanded=False):  # Create collapsable expander for executive summary
        if not filtered_df.empty:  # If dataset non-empty
            st.write(f"""
            - **Total Trading Volume:** The Ethiopian coffee market recorded a total trading volume of **{total_volume:,.0f} tons**.
            - **Top Traded Symbol:** **{top_symbol}** was the most actively traded coffee symbol.
            - **Top Warehouse:** **{top_warehouse}** handled the highest trading volume overall.
            - **Market Peak Year:** The highest average coffee price was observed in **{best_price_year}**.
            """)
        else:  # If dataset empty
            st.write("No active market summary available for current filter selection.")  # Display fallback message

    with st.expander("📄 View Dataset & Download Options", expanded=False):  # Create expander for dataset table and export options
        if not filtered_df.empty:  # If data exists
            st.subheader("Filtered Coffee Market Dataset Table")  # Section title
            st.dataframe(filtered_df, use_container_width=True)  # Render interactive dataset table
            
            csv_data = filtered_df.to_csv(index=False).encode('utf-8')  # Convert filtered dataset to CSV bytes
            st.download_button(  # Render download button component
                label="📥 Download Filtered Dataset (.CSV)",
                data=csv_data,
                file_name="filtered_coffee_market_data.csv",
                mime="text/csv",
            )
        else:  # If data missing
            st.warning("No data available to display or download.")  # Display warning notice
            
            ## Dynamic EDA and Outlier treatment section (Dynamic upload and analytics dashboard)

else:  # If user selects Mode 2 (Dynamic Upload & Analytics Engine) 
    st.markdown(  # Render top header banner for Mode 2 using custom HTML 
        """ 
    <div style="background-color: #0F172A; padding: 15px; border-radius: 6px; color: white; margin-bottom: 10px;">    
        <h1 style="margin: 0; color: white; font-size: 2rem;">📁 Dynamic Data Cleaning & Analytics dashboard</h1>    
        <p style="margin: 5px 0 0 0; color: #94A3B8; font-size: 1.05rem;">    
            Upload any CSV or Excel file to run automated data cleaning, outlier treatment, 
            dynamic EDA, and export structured reports. 
        </p> 
    </div> 
    """, 
        unsafe_allow_html=True,  # Enable HTML rendering 
    ) 

  
 
    # Configure the main Streamlit application layout and page title 
    st.set_page_config( 
        page_title="Dynamic Analytics Dashboard", page_icon="📊", layout="wide" 
    ) 
 
    # Render the sidebar title for file uploading 
    st.sidebar.header("📁 File Upload Options") 
 
    # Display file uploader accepting CSV and Excel file types 
    uploaded_file = st.sidebar.file_uploader( 
        "Upload dataset (.csv or .xlsx)", 
        type=["csv", "xlsx"], 
        key="dataset_file_uploader", 
    ) 
 
    # Process the data only when a file has been uploaded 
    if uploaded_file is not None: 
        try: 
            # Check if the uploaded file is a CSV format 
            if uploaded_file.name.endswith(".csv"): 
                raw_df = pd.read_csv(uploaded_file)  # Load CSV dataset into pandas 
            else: 
                raw_df = pd.read_excel( 
                    uploaded_file 
                )  # Load Excel dataset into pandas 
 
            # Show a success notification with the file name 
            st.success(f"Successfully loaded `{uploaded_file.name}`") 
 
            # Create a deep copy of the raw dataframe for data cleaning operations 
            clean_df = raw_df.copy(deep=True) 
 
            # Create two columns layout for data cleaning controls 
            col_c1, col_c2 = st.columns(2) 
 
            # First column for missing value handling strategies 
            with col_c1: 
                st.markdown("**Handling Missing Values:**")  # Subheading 
                null_strategy = st.selectbox( 
                    "Choose Strategy for Missing Values:",  # Select dropdown for missing value strategies 
                    [ 
                        "None", 
                        "Drop Rows with Missing Values", 
                        "Impute Numeric (Mean)", 
                        "Impute Numeric (Median)", 
                    ], 
                    key="missing_value_strategy_select", 
                ) 
                # Drop all rows that contain missing values 
                if null_strategy == "Drop Rows with Missing Values": 
                    clean_df = clean_df.dropna() 
                # Replace missing numeric values with the column mean 
                elif null_strategy == "Impute Numeric (Mean)": 
                    num_cols = clean_df.select_dtypes(include=[np.number]).columns 
                    clean_df[num_cols] = clean_df[num_cols].fillna( 
                        clean_df[num_cols].mean() 
                    ) 
                # Replace missing numeric values with the column median 
                elif null_strategy == "Impute Numeric (Median)": 
                    num_cols = clean_df.select_dtypes(include=[np.number]).columns 
                    clean_df[num_cols] = clean_df[num_cols].fillna( 
                        clean_df[num_cols].median() 
                    ) 
 
            # Second column for duplicate row removal 
            with col_c2: 
                st.markdown("**Duplicate Management:**")  # Subheading 
                remove_dupes = st.checkbox( 
                    "Remove Duplicate Rows automatically",  # Checkbox to trigger duplicate removal 
                    value=True, 
                    key="remove_duplicates_checkbox", 
                ) 
                if remove_dupes: 
                    clean_df = ( 
                        clean_df.drop_duplicates() 
                    )  # Drop duplicate records from dataframe 
 
            # Extract numeric column names into a list 
            numeric_columns = clean_df.select_dtypes( 
                include=[np.number] 
            ).columns.tolist() 
 
            # Extract categorical column names into a list 
            categorical_columns = clean_df.select_dtypes( 
                include=["object", "category"] 
            ).columns.tolist() 
 
            st.markdown("""
    <div style="background-color:#1B5E20; color:white; font-size:15px; font-weight:700;
    padding:6px 10px; border-radius:8px; text-align:center; margin-top:0px; margin-bottom:15px;">
     Key Performance Indicators (KPIs) Overview
    </div>
    """, unsafe_allow_html=True)  # Render green header bar for KPI section
            # Section 1 Header for dataset overview 
            
 
            # Create 4 columns for displaying raw overview KPIs 
            p1, p2, p3, p4 = st.columns(4) 
            p1.metric( 
                "Total Rows", f"{raw_df.shape[0]:,}" 
            )  # Display total row count 
            p2.metric( 
                "Total Columns", f"{raw_df.shape[1]:,}" 
            )  # Display total column count 
            p3.metric( 
                "Missing Values", f"{raw_df.isnull().sum().sum():,}" 
            )  # Display total null count 
            p4.metric( 
                "Duplicate Rows", f"{raw_df.duplicated().sum():,}" 
            )  # Display total duplicate count 
 
            st.markdown("---")  # Horizontal divider line 
 
            # Calculate and display metrics if numeric columns exist 
            if numeric_columns: 
                selected_kpi_col = st.selectbox( 
                    "Select Metric Column for Summary KPIs:",  # Select box for chosen metric 
                    numeric_columns, 
                    key="combined_kpi_select", 
                ) 
 
                # Compute key summary statistics for the chosen numeric column 
                total_val = clean_df[selected_kpi_col].sum()  # Calculate total sum 
                avg_val = ( 
                    clean_df[selected_kpi_col].mean() 
                )  # Calculate average mean 
                max_val = clean_df[selected_kpi_col].max()  # Find maximum value 
                min_val = clean_df[selected_kpi_col].min()  # Find minimum value 
                count_val = clean_df[ 
                    selected_kpi_col 
                ].count()  # Count non-null items 
 
                # Render summary metrics across 5 columns 
                k1, k2, k3, k4, k5 = st.columns(5) 
                k1.metric("🔢 Total Count", f"{count_val:,.0f}")  # Display count 
                k2.metric("➕ Total Sum", f"{total_val:,.2f}")  # Display sum 
                k3.metric("📈 Average (Mean)", f"{avg_val:,.2f}")  # Display average 
                k4.metric("⬆️ Maximum", f"{max_val:,.2f}")  # Display max 
                k5.metric("⬇️ Minimum", f"{min_val:,.2f}")  # Display min 
            else: 
                st.warning( 
                    "No numeric columns found for metric calculation." 
                )  # Display warning if no numbers found 
 
            # Section 2 Header for Cross-Tabulation 
            
            st.markdown("""
    <div style="background-color:#0F172A; color:white; font-size:15px; font-weight:700;
    padding:6px 10px; border-radius:8px; text-align:center; margin-top:0px; margin-bottom:15px;">
     2. Automated Cross-Tabulation Analysis
    </div>
    """, unsafe_allow_html=True)  # Render green header bar for KPI section
            
 
            # Wrap Cross-Tabulation inside a collapsed expander panel 
            with st.expander( 
                "🔍 Open / Collapse Cross-Tabulation Analysis", expanded=False 
            ): 
                # Check if at least 2 categorical columns are present 
                if len(categorical_columns) >= 2: 
                    ct_col1, ct_col2, ct_col3 = st.columns( 
                        3 
                    )  # Create 3 columns for inputs 
                    with ct_col1: 
                        row_var = st.selectbox( 
                            "Select Row Variable (Categorical):",  # Select row categorical feature 
                            categorical_columns, 
                            index=0, 
                            key="crosstab_row_variable_select", 
                        ) 
                    with ct_col2: 
                        col_var = st.selectbox( 
                            "Select Column Variable (Categorical):",  # Select column categorical feature 
                            [c for c in categorical_columns if c != row_var], 
                            index=0, 
                            key="crosstab_col_variable_select", 
                        ) 
                    with ct_col3: 
                        agg_func = st.selectbox( 
                            "Aggregation Type:",  # Select calculation aggregation 
                            ["Count (Frequency)", "Percentage (%)"], 
                            key="crosstab_agg_func_select", 
                        ) 
 
                    # Compute frequency count crosstab 
                    if agg_func == "Count (Frequency)": 
                        ct_df = pd.crosstab( 
                            clean_df[row_var], 
                            clean_df[col_var], 
                            margins=True, 
                            margins_name="Total", 
                        ) 
                    # Compute percentage breakdown crosstab 
                    else: 
                        ct_df = ( 
                            pd.crosstab( 
                                clean_df[row_var], 
                                clean_df[col_var], 
                                normalize="index", 
                            ) 
                            * 100 
                        ).round(2) 
 
                    # Render cross-tabulation table in Streamlit 
                    st.dataframe(ct_df, use_container_width=True) 
 
                    # Create heat map matrix plot for categorical cross-tabulation 
                    fig_ct = px.imshow( 
                        pd.crosstab(clean_df[row_var], clean_df[col_var]), 
                        text_auto=True, 
                        color_continuous_scale="Viridis", 
                        title=f"Heatmap: {row_var} vs {col_var}", 
                    ) 
                    fig_ct.update_layout(height=350)  # Adjust figure height 
                    st.plotly_chart( 
                        fig_ct, use_container_width=True 
                    )  # Render heatmap chart 
                else: 
                    st.warning( 
                        "Automatic Cross-Tabulation requires at least 2 categorical columns." 
                    )  # Show warning 
 
            # Section 3 Header for Interactive Visualizations 
            st.subheader("3. Dynamic Visualizations") 
 
            # Check if dataset contains necessary features for plotting 
            if numeric_columns and categorical_columns: 
                v1, v2, v3 = st.columns(3)  # Create 3 columns for select controls 
                with v1: 
                    x_var = st.selectbox( 
                        "Select Primary Variable (Categorical / X-Axis):",  # Select X-axis variable 
                        categorical_columns, 
                        key="dynamic_chart_x_var_select", 
                    ) 
                with v2: 
                    y_var = st.selectbox( 
                        "Select Primary Metric (Numeric / Y-Axis):",  # Select Y-axis variable 
                        numeric_columns, 
                        key="dynamic_chart_y_var_select", 
                    ) 
                with v3: 
                    chart_kind = st.selectbox( 
                        "Chart Type:",  # Select chart visual style 
                        [ 
                            "Bar Chart", 
                            "Box Plot (Outliers)", 
                            "Line Trend", 
                            "Scatter Plot", 
                            "Pie Chart", 
                            "Heatmap Matrix", 
                            "Dual-Axis Chart", 
                        ], 
                        key="dynamic_chart_type_select", 
                    ) 
 
                # Build selected Bar Chart model 
                if chart_kind == "Bar Chart": 
                    fig_dyn = px.bar( 
                        clean_df, 
                        x=x_var, 
                        y=y_var, 
                        color=x_var, 
                        title=f"{y_var} aggregated by {x_var}", 
                    ) 
                # Build selected Box Plot model 
                elif chart_kind == "Box Plot (Outliers)": 
                    fig_dyn = px.box( 
                        clean_df, 
                        x=x_var, 
                        y=y_var, 
                        color=x_var, 
                        title=f"Outlier & Distribution Analysis: {y_var}", 
                    ) 
                # Build selected Line Trend model 
                elif chart_kind == "Line Trend": 
                    fig_dyn = px.line( 
                        clean_df, x=x_var, y=y_var, title=f"{y_var} trend across {x_var}" 
                    ) 
                # Build selected Scatter Plot model 
                elif chart_kind == "Scatter Plot": 
                    fig_dyn = px.scatter( 
                        clean_df, 
                        x=x_var, 
                        y=y_var, 
                        color=x_var, 
                        title=f"Correlation Scatter Plot: {x_var} vs {y_var}", 
                    ) 
                # Build selected Pie Chart model 
                elif chart_kind == "Pie Chart": 
                    pie_df = clean_df.groupby(x_var)[y_var].sum().reset_index() 
                    fig_dyn = px.pie( 
                        pie_df, 
                        names=x_var, 
                        values=y_var, 
                        title=f"Proportional Share of {y_var} by {x_var}", 
                        hole=0.3, 
                    ) 
                # Build selected Heatmap Matrix model 
                elif chart_kind == "Heatmap Matrix": 
                    other_cats = [c for c in categorical_columns if c != x_var] 
                    if other_cats: 
                        secondary_cat = st.selectbox( 
                            "Select Secondary Category (Y-Axis):",  # Select Y-axis secondary category 
                            other_cats, 
                            key="heatmap_secondary_cat_select", 
                        ) 
                        heatmap_df = pd.crosstab( 
                            clean_df[x_var], 
                            clean_df[secondary_cat], 
                            values=clean_df[y_var], 
                            aggfunc="mean", 
                        ).fillna(0) 
                        fig_dyn = px.imshow( 
                            heatmap_df, 
                            labels=dict( 
                                x=secondary_cat, y=x_var, color=f"Avg {y_var}" 
                            ), 
                            title=( 
                                f"Heatmap Matrix: Average {y_var} across {x_var} &" 
                                f" {secondary_cat}" 
                            ), 
                            color_continuous_scale="Viridis", 
                            text_auto=True, 
                        ) 
                    else: 
                        st.warning( 
                            "Heatmap requires at least 2 categorical columns in the dataset." 
                        ) 
                        fig_dyn = px.bar(clean_df, x=x_var, y=y_var) 
                # Build selected Dual-Axis Chart model 
                elif chart_kind == "Dual-Axis Chart": 
                    other_nums = [n for n in numeric_columns if n != y_var] 
                    if other_nums: 
                        y2_var = st.selectbox( 
                            "Select Secondary Metric (Right Y-Axis):",  # Select secondary Y-axis numeric column 
                            other_nums, 
                            key="dual_axis_secondary_metric_select", 
                        ) 
                        grouped = ( 
                            clean_df.groupby(x_var)[[y_var, y2_var]].mean().reset_index() 
                        ) 
 
                        fig_dyn = make_subplots( 
                            specs=[[{"secondary_y": True}]] 
                        )  # Create dual subplot 
                        fig_dyn.add_trace( 
                            go.Bar( 
                                x=grouped[x_var], 
                                y=grouped[y_var], 
                                name=f"Mean {y_var}", 
                                marker_color="royalblue", 
                            ), 
                            secondary_y=False, 
                        ) 
                        fig_dyn.add_trace( 
                            go.Scatter( 
                                x=grouped[x_var], 
                                y=grouped[y2_var], 
                                name=f"Mean {y2_var}", 
                                mode="lines+markers", 
                                line=dict(color="firebrick", width=3), 
                            ), 
                            secondary_y=True, 
                        ) 
 
                        fig_dyn.update_xaxes(title_text=x_var) 
                        fig_dyn.update_yaxes( 
                            title_text=f"<b>{y_var}</b>", secondary_y=False 
                        ) 
                        fig_dyn.update_yaxes( 
                            title_text=f"<b>{y2_var}</b>", secondary_y=True 
                        ) 
                        fig_dyn.update_layout( 
                            title=f"Dual-Axis Comparison: {y_var} vs {y2_var}" 
                        ) 
                    else: 
                        st.warning( 
                            "Dual-Axis Chart requires at least 2 numeric columns in the dataset." 
                        ) 
                        fig_dyn = px.bar(clean_df, x=x_var, y=y_var) 
 
                # Apply white theme and height to dynamic chart 
                fig_dyn.update_layout(template="plotly_white", height=420) 
                st.plotly_chart( 
                    fig_dyn, use_container_width=True 
                )  # Render chart output 
            else: 
                st.warning( 
                    "Dataset needs at least one Numeric and one Categorical column for automated charting." 
                ) 
 
            # Section 4 Header for Smart Automated Insights 
            st.markdown("---") 
            st.subheader("4.Automated Smart Insights ") 
 
            # Wrap Smart Insights inside a collapsed expander panel 
            with st.expander( 
                " Open / Collapse Key Insights & Takeaways", expanded=False 
            ): 
                insights = []  # Initialize empty list to hold dynamic text insights 
                if not clean_df.empty: 
                    # Insight 1: Find the top performing group 
                    if categorical_columns and numeric_columns: 
                        c_col, n_col = categorical_columns[0], numeric_columns[0] 
                        grp_top = ( 
                            clean_df.groupby(c_col)[n_col].sum().reset_index() 
                        )  # Group and aggregate 
                        if not grp_top.empty and grp_top[n_col].notnull().any(): 
                            top_row = grp_top.loc[ 
                                grp_top[n_col].idxmax() 
                            ]  # Extract maximum index 
                            insights.append( 
                                f"🏆 **Top Performing Group:** Category" 
                                f" **'{top_row[c_col]}'** has the highest total" 
                                f" **{n_col}** with **{top_row[n_col]:,.2f}**." 
                            ) 
 
                    # Insight 2: Find the lowest performing group 
                    if categorical_columns and numeric_columns: 
                        c_col, n_col = categorical_columns[0], numeric_columns[0] 
                        grp_low = ( 
                            clean_df.groupby(c_col)[n_col].sum().reset_index() 
                        )  # Group and aggregate 
                        if not grp_low.empty and grp_low[n_col].notnull().any(): 
                            low_row = grp_low.loc[ 
                                grp_low[n_col].idxmin() 
                            ]  # Extract minimum index 
                            insights.append( 
                                f"🔻 **Lowest Performing Group:** Category" 
                                f" **'{low_row[c_col]}'** recorded the lowest total" 
                                f" **{n_col}** with **{low_row[n_col]:,.2f}**." 
                            ) 
 
                    # Insight 3: Metric Average & Peak calculation 
                    if numeric_columns: 
                        n_col = numeric_columns[0] 
                        if clean_df[n_col].notnull().any(): 
                            mean_v = clean_df[n_col].mean()  # Calculate column mean 
                            max_v = clean_df[n_col].max()  # Calculate column peak 
                            insights.append( 
                                f"📈 **Metric Average & Peak:** Overall average for" 
                                f" **{n_col}** is **{mean_v:,.2f}**, reaching a" 
                                f" maximum peak of **{max_v:,.2f}**." 
                            ) 
 
                    # Insight 4: Coefficient of Variation / Volatility analysis 
                    if numeric_columns: 
                        n_col = numeric_columns[0] 
                        if clean_df[n_col].notnull().any(): 
                            std_v = clean_df[ 
                                n_col 
                            ].std()  # Calculate standard deviation 
                            mean_v = clean_df[n_col].mean()  # Calculate mean 
                            if mean_v and not np.isnan(mean_v) and mean_v != 0: 
                                cv = ( 
                                    std_v / mean_v 
                                ) * 100  # Calculate CV percentage 
                                insights.append( 
                                    f"⚠️ **Variability Risk:** The Coefficient of" 
                                    f" Variation for **{n_col}** is **{cv:.1f}%**," 
                                    " indicating" 
                                    f" {'high volatility' if cv > 50 else 'stable distribution'}" 
                                    " across records." 
                                ) 
 
                    # Insight 5: Compute most frequent category (Mode) 
                    if categorical_columns: 
                        c_col = categorical_columns[0] 
                        top_cat_mode = ( 
                            clean_df[c_col].mode() 
                        )  # Calculate statistical mode 
                        if not top_cat_mode.empty: 
                            mode_val = top_cat_mode[0] 
                            cnt = (clean_df[c_col] == mode_val).sum()  # Count occurrences 
                            pct = (cnt / len(clean_df)) * 100  # Compute percentage 
                            insights.append( 
                                f"🎯 **Dominant Category:** **'{mode_val}'** is the" 
                                f" most frequent entry in **{c_col}**, accounting" 
                                f" for **{pct:.1f}%** of total records." 
                            ) 
 
                    # Insight 6: Report missing values data cleaning impact 
                    raw_nulls = raw_df.isnull().sum().sum() 
                    if raw_nulls > 0: 
                        insights.append( 
                            f"🧹 **Data Cleaning Impact:** A total of **{raw_nulls:,}" 
                            " missing values** were detected and processed during" 
                            " automated cleaning." 
                        ) 
                    else: 
                        insights.append( 
                            "✅ **Data Integrity:** The uploaded dataset is fully" 
                            " complete with **0 missing values**." 
                        ) 
 
                    # Insight 7: Statistical Correlation check between numeric features 
                    if len(numeric_columns) >= 2: 
                        corr_m = ( 
                            clean_df[numeric_columns].corr().abs() 
                        )  # Compute absolute correlation matrix 
                        corr_array = corr_m.to_numpy( 
                            copy=True 
                        )  # Convert matrix to array 
                        np.fill_diagonal( 
                            corr_array, 0 
                        )  # Zero out self-correlation diagonal 
                        corr_m = pd.DataFrame( 
                            corr_array, index=corr_m.index, columns=corr_m.columns 
                        ) 
 
                        if not corr_m.isna().all().all() and (corr_m > 0).any().any(): 
                            max_corr_idx = ( 
                                corr_m.unstack().idxmax() 
                            )  # Identify highest correlation pair 
                            max_corr_val = ( 
                                corr_m.unstack().max() 
                            )  # Extract correlation value 
                            insights.append( 
                                "🔗 **Strongest Metric Correlation:**" 
                                f" **'{max_corr_idx[0]}'** and" 
                                f" **'{max_corr_idx[1]}'** show the strongest" 
                                " statistical relationship (R =" 
                                f" **{max_corr_val:.2f}**)." 
                            ) 
 
                    # Insight 8: Overall Historical Trend direction 
                    if numeric_columns: 
                        n_col = numeric_columns[0] 
                        first_val = clean_df[n_col].iloc[0]  # First value 
                        last_val = clean_df[n_col].iloc[-1]  # Latest value 
                        diff = last_val - first_val  # Absolute change 
                        pct_chg = ( 
                            (diff / abs(first_val) * 100) if first_val != 0 else 0 
                        )  # Percent change 
                        direction = ( 
                            "increased 📈" if diff >= 0 else "decreased 📉" 
                        )  # Direction text 
                        insights.append( 
                            f"📊 **Trend Snapshot:** Across the dataset order," 
                            f" **{n_col}** {direction} by **{abs(pct_chg):.1f}%**" 
                            " from initial to latest record." 
                        ) 
 
                # Display all generated insights sequentially using info boxes 
                for ins in insights: 
                    st.info(ins) 
            # Section 6 Header for Raw Data Preview 
            st.markdown("---") 
            st.subheader("") 
            with st.expander("📋 View Raw Data ", expanded=False): 
                st.dataframe( 
                    raw_df.head(10), use_container_width=True 
                )  # Display head of raw dataframe 
 
            # Section 7 Header for Exporting Clean Dataset 
            st.markdown("---") 
            st.subheader("") 
            cleaned_csv = clean_df.to_csv(index=False).encode( 
                "utf-8" 
            )  # Convert cleaned dataframe to CSV bytes 
            st.download_button( 
                label="📥 Download Cleaned Dataset (.CSV)",  # Render file download button 
                data=cleaned_csv, 
                file_name="cleaned_dataset.csv", 
                mime="text/csv", 
                key="download_cleaned_dataset_btn", 
            ) 
 
        # Catch and output any unexpected runtime errors 
        except Exception as err: 
            st.error(f"Error processing file: {err}") 
 
    # Show instruction if no dataset file is uploaded yet 
    else: 
        st.info( 
            "👆 Please upload a `.csv` or `.xlsx` file from the sidebar panel to activate the Dynamic Analytics Engine." 
        ) 