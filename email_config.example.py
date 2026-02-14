# Email Configuration Example
# Copy this file to .env or set these as environment variables

# For Gmail:
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USERNAME=your-email@gmail.com
# SMTP_PASSWORD=your-app-password  # Use App Password, not regular password
# RECIPIENT_EMAIL=your-email@gmail.com

# For Outlook/Hotmail:
# SMTP_SERVER=smtp-mail.outlook.com
# SMTP_PORT=587
# SMTP_USERNAME=your-email@outlook.com
# SMTP_PASSWORD=your-password
# RECIPIENT_EMAIL=your-email@outlook.com

# For Yahoo:
# SMTP_SERVER=smtp.mail.yahoo.com
# SMTP_PORT=587
# SMTP_USERNAME=your-email@yahoo.com
# SMTP_PASSWORD=your-app-password
# RECIPIENT_EMAIL=your-email@yahoo.com

# Instructions:
# 1. Set these environment variables in your system or create a .env file
# 2. For Gmail, you need to:
#    - Enable 2-Factor Authentication
#    - Generate an App Password: https://myaccount.google.com/apppasswords
#    - Use the App Password as SMTP_PASSWORD
# 3. Update main.py to load from .env file if you prefer that method

