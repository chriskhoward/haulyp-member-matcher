import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

st.set_page_config(page_title="Wild Apricot & Circle.so Member Matcher", layout="wide")

st.title("Wild Apricot & Circle.so Member Matcher")

# File upload section
col1, col2 = st.columns(2)
with col1:
    wa_file = st.file_uploader("Upload Wild Apricot CSV", type=['csv'])
with col2:
    circle_file = st.file_uploader("Upload Circle.so CSV", type=['csv'])

if wa_file and circle_file:
    # Load the data
    wa_df = pd.read_csv(wa_file)
    circle_df = pd.read_csv(circle_file)
    
    # Clean and prepare email addresses
    wa_df['Email'] = wa_df['Email'].str.lower().str.strip()
    circle_df['Email'] = circle_df['Email'].str.lower().str.strip()
    
    # Match users by email
    matched_users = pd.merge(wa_df, circle_df, on='Email', how='outer', indicator=True)
    
    # Calculate statistics
    total_wa = len(wa_df)
    total_circle = len(circle_df)
    matched = len(matched_users[matched_users['_merge'] == 'both'])
    unmatched_wa = len(matched_users[matched_users['_merge'] == 'left_only'])
    unmatched_circle = len(matched_users[matched_users['_merge'] == 'right_only'])
    
    # Display statistics
    st.header("Matching Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Wild Apricot Members", total_wa)
        st.metric("Unmatched Wild Apricot", unmatched_wa)
    with col2:
        st.metric("Total Circle.so Members", total_circle)
        st.metric("Unmatched Circle.so", unmatched_circle)
    with col3:
        st.metric("Matched Members", matched)
    
    # Process matched users
    matched_only = matched_users[matched_users['_merge'] == 'both'].copy()
    
    # Convert renewal date to datetime
    matched_only['Renewal due'] = pd.to_datetime(matched_only['Renewal due'], errors='coerce')
    matched_only['Renewal Month'] = matched_only['Renewal due'].dt.strftime('%B %Y')
    
    # Handle NaN values in Renewal Month
    matched_only['Renewal Month'] = matched_only['Renewal Month'].fillna('No Renewal Date')
    
    # Add last active status (assuming 'Last sign in at' column exists in Circle.so data)
    if 'Last sign in at' in matched_only.columns:
        matched_only['Last sign in at'] = pd.to_datetime(matched_only['Last sign in at'], errors='coerce')
        matched_only['Active in Circle'] = matched_only['Last sign in at'] > (datetime.now() - timedelta(days=30))
    
    # Filters
    st.header("Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        month_options = ['All'] + sorted([m for m in matched_only['Renewal Month'].unique() if pd.notna(m)])
        selected_month = st.selectbox(
            "Filter by Renewal Month",
            options=month_options
        )
    
    with col2:
        date_range = st.date_input(
            "Filter by Specific Date Range",
            value=(datetime.now().date(), (datetime.now() + timedelta(days=30)).date())
        )
    
    with col3:
        if 'Active in Circle' in matched_only.columns:
            show_active_only = st.checkbox("Show only Active Circle Users")
    
    # Apply filters
    filtered_df = matched_only.copy()
    
    if selected_month != 'All':
        filtered_df = filtered_df[filtered_df['Renewal Month'] == selected_month]
    
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['Renewal due'].dt.date >= date_range[0]) &
            (filtered_df['Renewal due'].dt.date <= date_range[1])
        ]
    
    if 'Active in Circle' in filtered_df.columns and show_active_only:
        filtered_df = filtered_df[filtered_df['Active in Circle']]
    
    # Display results
    st.header("Matched Members")
    
    if not filtered_df.empty:
        # Generate renewal messages
        filtered_df['Renewal Message'] = filtered_df.apply(
            lambda x: f"Hi {x['First name']}, your HAULYP membership is due for renewal on {x['Renewal due'].strftime('%B %d, %Y')}. "
                     f"Would you like to renew your membership to continue accessing our community and events?",
            axis=1
        )
        
        # Prepare columns to display
        display_columns = ['First name', 'Last name', 'Email', 'Renewal due', 'Renewal Message']
        if 'Active in Circle' in filtered_df.columns:
            display_columns.append('Active in Circle')
        
        # Display the data
        st.dataframe(
            filtered_df[display_columns].sort_values('Renewal due'),
            hide_index=True
        )
        
        # Export functionality
        st.download_button(
            label="Download Filtered Data as CSV",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name=f"member_renewals_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No members match the selected filters.")
else:
    st.info("Please upload both Wild Apricot and Circle.so CSV files to begin.") 