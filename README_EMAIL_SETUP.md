# Email Setup Instructions

## Quick Setup

To enable email functionality for the contact form, you need to configure your email settings.

### Option 1: Environment Variables (Recommended)

Set these environment variables before running the server:

**Windows PowerShell:**
```powershell
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SMTP_USERNAME="your-email@gmail.com"
$env:SMTP_PASSWORD="your-app-password"
$env:RECIPIENT_EMAIL="your-email@gmail.com"
```

**Windows CMD:**
```cmd
set SMTP_SERVER=smtp.gmail.com
set SMTP_PORT=587
set SMTP_USERNAME=your-email@gmail.com
set SMTP_PASSWORD=your-app-password
set RECIPIENT_EMAIL=your-email@gmail.com
```

**Linux/Mac:**
```bash
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="your-email@gmail.com"
```

### Option 2: Direct Configuration

Edit `main.py` and update these lines (around line 16-20):

```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password"
RECIPIENT_EMAIL = "your-email@gmail.com"
```

## Gmail Setup (Most Common)

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate an App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "Portfolio Contact Form"
   - Copy the generated 16-character password
   - Use this as your `SMTP_PASSWORD`

3. **Update your configuration** with:
   - `SMTP_SERVER`: `smtp.gmail.com`
   - `SMTP_PORT`: `587`
   - `SMTP_USERNAME`: Your Gmail address
   - `SMTP_PASSWORD`: The App Password you generated
   - `RECIPIENT_EMAIL`: Your Gmail address (where you want to receive emails)

## Other Email Providers

### Outlook/Hotmail
- `SMTP_SERVER`: `smtp-mail.outlook.com`
- `SMTP_PORT`: `587`

### Yahoo
- `SMTP_SERVER`: `smtp.mail.yahoo.com`
- `SMTP_PORT`: `587`
- Requires App Password (similar to Gmail)

### Custom SMTP Server
- Check with your email provider for SMTP settings
- Common ports: 587 (TLS) or 465 (SSL)

## Testing

After configuration, test the contact form:
1. Start your server: `uvicorn main:app --reload --port 8001`
2. Visit: `http://localhost:8001/contact`
3. Fill out and submit the form
4. Check your email inbox for the message

## Security Note

⚠️ **Never commit your email password to version control!**

- Use environment variables
- Add `.env` to `.gitignore` if using a .env file
- Use App Passwords instead of your main password

