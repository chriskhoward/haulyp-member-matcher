# HAULYP Member Matcher

A Streamlit application that helps match and manage members between Wild Apricot and Circle.so platforms. The app provides tools for tracking renewals, filtering members, and generating renewal messages.

## Features

- Match members between Wild Apricot and Circle.so using email addresses
- View matching statistics
- Filter members by renewal month or specific date range
- Show only active Circle.so users
- Generate personalized renewal messages
- Export filtered data to CSV

## Required Data Files

### Wild Apricot CSV
Required columns:
- Email
- First name
- Last name
- Renewal due

### Circle.so CSV
Required columns:
- Email
- Last sign in at (optional, for active user filtering)

## Local Development

1. Clone this repository:
```bash
git clone https://github.com/chriskhoward/haulyp-member-matcher.git
cd haulyp-member-matcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

## Deployment

This app is deployed using [Streamlit Community Cloud](https://streamlit.io/cloud). 

Visit the live app at: https://haulyp-member-matcher.streamlit.app

## Security Note

Please ensure that any sensitive member data is handled according to your organization's data privacy policies. The app does not store any uploaded data permanently. 