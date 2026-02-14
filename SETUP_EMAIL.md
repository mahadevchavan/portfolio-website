# Email Setup Instructions for Contact Form

## Quick Setup Guide

Your contact form needs email configuration to send messages. Follow these steps:

### Step 1: Enable 2-Factor Authentication on Gmail

1. Go to your Google Account: https://myaccount.google.com/
2. Click on **Security** in the left sidebar
3. Under "Signing in to Google", enable **2-Step Verification**

### Step 2: Generate Gmail App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Select **Mail** as the app
3. Select **Other (Custom name)** as the device
4. Enter "Portfolio Contact Form" as the name
5. Click **Generate**
6. **Copy the 16-character password** (it will look like: `abcd efgh ijkl mnop`)

### Step 3: Set Environment Variable

**Windows PowerShell:**
```powershell
$env:SMTP_PASSWORD="your-16-character-app-password"
```

**Windows CMD:**
```cmd
set SMTP_PASSWORD=your-16-character-app-password
```

**Note:** Remove spaces from the app password when setting it.

### Step 4: Restart Your Server

After setting the environment variable, restart your FastAPI server:

```powershell
# Stop the current server (Ctrl+C)
# Then restart:
.\portfolio_venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8001
```

## Alternative: Set Password Directly in Code (Not Recommended for Production)

If you want to test quickly, you can temporarily set it in `main.py`:

```python
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your-app-password-here")
```

**⚠️ WARNING:** Never commit your password to Git! Remove it before pushing to GitHub.

## Testing

1. Visit: http://localhost:8001/contact
2. Fill out the contact form
3. Submit it
4. Check your email inbox (chmahadev321@gmail.com)

## Troubleshooting

### Error: "Email service not configured"
- **Solution:** Set the SMTP_PASSWORD environment variable

### Error: "Email authentication failed"
- **Solution:** 
  - Make sure you're using an App Password, not your regular Gmail password
  - Check that 2-Factor Authentication is enabled
  - Verify the password has no spaces

### Error: "SMTP error occurred"
- **Solution:**
  - Check your internet connection
  - Verify SMTP settings (smtp.gmail.com, port 587)
  - Check if Gmail is blocking the connection (check Gmail security settings)

## Current Configuration

- **SMTP Server:** smtp.gmail.com
- **SMTP Port:** 587
- **Your Email:** chmahadev321@gmail.com
- **Recipient Email:** chmahadev321@gmail.com (you'll receive emails here)

## Need Help?

If you're still having issues, check the server console for detailed error messages. The error will show exactly what went wrong.


