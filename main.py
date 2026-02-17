from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import re
from typing import Optional, Tuple
if os.getenv("VERCEL") is None:
    from dotenv import load_dotenv
    load_dotenv()

app = FastAPI()

# Email configuration - Set these as environment variables or update directly
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")  # Your email
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # Your Gmail App Password (set as environment variable)
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")  # Where to receive contact form emails

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "year": datetime.now().year
    })

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {
        "request": request,
        "year": datetime.now().year
    })

@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request):
    return templates.TemplateResponse("projects.html", {
        "request": request,
        "year": datetime.now().year
    })

# Simple email validation function
def is_valid_email(email: str) -> bool:
    """Simple email validation using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Simple validation function
def validate_contact_form(name: str, email: str, subject: str, message: str) -> Tuple[bool, Optional[str]]:
    """
    Validate contact form data
    Returns: (is_valid, error_message)
    """
    # Validate name
    name = name.strip() if name else ""
    if len(name) < 2:
        return False, "Name must be at least 2 characters long"
    if len(name) > 100:
        return False, "Name must be less than 100 characters"
    
    # Validate email
    email = email.strip() if email else ""
    if not email:
        return False, "Email is required"
    if not is_valid_email(email):
        return False, "Please enter a valid email address"
    
    # Validate subject
    subject = subject.strip() if subject else ""
    if len(subject) < 3:
        return False, "Subject must be at least 3 characters long"
    if len(subject) > 200:
        return False, "Subject must be less than 200 characters"
    
    # Validate message
    message = message.strip() if message else ""
    if len(message) < 10:
        return False, "Message must be at least 10 characters long"
    if len(message) > 5000:
        return False, "Message must be less than 5000 characters"
    
    return True, None

def send_email(name: str, email: str, subject: str, message: str) -> Tuple[bool, str]:
    """Send email using SMTP
    Returns: (success: bool, error_message: str)
    """
    # Check if email is configured
    if not SMTP_PASSWORD or SMTP_PASSWORD == "":
        error_msg = "Email service not configured. Please set SMTP_PASSWORD environment variable with your Gmail App Password."
        print(f"EMAIL ERROR: {error_msg}")
        return False, error_msg
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"Portfolio Contact Form: {subject}"
        msg['Reply-To'] = email
        
        # Email body
        body = f"""
New contact form submission from your portfolio website:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This email was sent from your portfolio contact form.
You can reply directly to this email to respond to {name} at {email}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USERNAME, RECIPIENT_EMAIL, text)
        server.quit()
        
        print(f"SUCCESS: Email sent successfully from {email} to {RECIPIENT_EMAIL}")
        return True, ""
    except smtplib.SMTPAuthenticationError as e:
        error_msg = "Email authentication failed. Please check your Gmail App Password."
        print(f"EMAIL ERROR: {error_msg} - {str(e)}")
        return False, error_msg
    except smtplib.SMTPException as e:
        error_msg = f"SMTP error occurred: {str(e)}"
        print(f"EMAIL ERROR: {error_msg}")
        return False, error_msg
    except Exception as e:
        error_msg = f"Error sending email: {str(e)}"
        print(f"EMAIL ERROR: {error_msg}")
        return False, error_msg

@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request, success: Optional[str] = None, error: Optional[str] = None):
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "year": datetime.now().year,
        "success": success,
        "error": error
    })

@app.post("/contact", response_class=HTMLResponse)
async def submit_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...)
):
    try:
        # Validate form data using simple validation
        is_valid, error_message = validate_contact_form(name, email, subject, message)
        
        if not is_valid:
            return templates.TemplateResponse("contact.html", {
                "request": request,
                "year": datetime.now().year,
                "error": error_message,
                "form_data": {
                    "name": name,
                    "email": email,
                    "subject": subject,
                    "message": message
                }
            })
        
        # Clean the data
        clean_name = name.strip()
        clean_email = email.strip()
        clean_subject = subject.strip()
        clean_message = message.strip()
        
        # Send email
        email_sent, email_error = send_email(
            name=clean_name,
            email=clean_email,
            subject=clean_subject,
            message=clean_message
        )
        
        if email_sent:
            return RedirectResponse(
                url=f"/contact?success=Thank you for your message! I'll get back to you soon.",
                status_code=303
            )
        else:
            # Show specific error message
            error_message = email_error if email_error else "Sorry, there was an error sending your message. Please try again later or contact me directly via email."
            return templates.TemplateResponse("contact.html", {
                "request": request,
                "year": datetime.now().year,
                "error": error_message,
                "form_data": {
                    "name": name,
                    "email": email,
                    "subject": subject,
                    "message": message
                }
            })
            
    except Exception as e:
        return templates.TemplateResponse("contact.html", {
            "request": request,
            "title": "Contact - Mahadev Chavan | Data Science Engineer",
            "year": datetime.now().year,
            "error": "An unexpected error occurred. Please try again later.",
            "form_data": {
                "name": name,
                "email": email,
                "subject": subject,
                "message": message
            }
        })
