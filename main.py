from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.request
import urllib.parse
import json
import os
import re
import random
import hashlib
import time
import hmac
import secrets
from typing import Optional, Tuple

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from portfolio_data import get_projects, get_static_about_data, get_experience

if os.getenv("VERCEL") is None:
    from dotenv import load_dotenv
    load_dotenv()
    print("INFO: Local environment detected. Loaded .env file.")
else:
    print("INFO: Vercel environment detected. Using system environment variables.")

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Email configuration - Set these as environment variables or update directly
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")  # Your email
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # Your Gmail App Password (set as environment variable)
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")  # Where to receive contact form emails
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    projects = get_projects()
    experience, total_experience = get_experience()
    skills, expertise, education, certifications = get_static_about_data()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "year": datetime.now().year,
        "projects": projects[:3], # Pass only the first 3 projects
        "experience": experience,
        "total_experience": total_experience,
        "skills": skills,
        "expertise": expertise,
        "education": education,
        "certifications": certifications
    })

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    experience_data, total_exp = get_experience()
    skills, expertise, education, certifications = get_static_about_data()
    return templates.TemplateResponse("about.html", {
        "request": request,
        "year": datetime.now().year,
        "experience": experience_data,
        "total_experience": total_exp,
        "skills": skills,
        "expertise": expertise,
        "education": education,
        "certifications": certifications
    })

@app.get("/sitemap.xml", response_class=FileResponse)
async def sitemap():
    return FileResponse("static/sitemap.xml", media_type="application/xml")

@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request):
    projects = get_projects()
    return templates.TemplateResponse("projects.html", {
        "request": request,
        "year": datetime.now().year,
        "projects": projects
    })

@app.get("/resources", response_class=HTMLResponse)
async def resources_page(request: Request):
    return templates.TemplateResponse("resources.html", {
        "request": request,
        "year": datetime.now().year
    })

# Simple email validation function
def is_valid_email(email: str) -> bool:
    """Simple email validation using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_security_token() -> str:
    """Generate a signed timestamp token for the form"""
    timestamp = str(int(time.time()))
    # Create a signature of the timestamp using the secret key
    signature = hmac.new(SECRET_KEY.encode(), timestamp.encode(), hashlib.sha256).hexdigest()
    return f"{timestamp}:{signature}"

def verify_security_token(token: str, honeypot: Optional[str]) -> Tuple[bool, str]:
    """Verify honeypot is empty and form wasn't submitted too quickly"""
    # 1. Check Honeypot (Must be empty)
    if honeypot:
        return False, "Spam detected (honeypot)."
    
    try:
        timestamp_str, signature = token.split(':')
        timestamp = int(timestamp_str)
        
        # 2. Verify Signature
        expected_signature = hmac.new(SECRET_KEY.encode(), timestamp_str.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected_signature):
            return False, "Invalid security token."
            
        # 3. Check Time (Must take at least 3 seconds to fill form)
        current_time = int(time.time())
        if current_time - timestamp < 3:
            return False, "Form submitted too quickly. Please wait a moment."
            
        # 4. Enforce Token Expiration (Expire after 1 hour)
        if current_time - timestamp > 3600:
            return False, "Security token expired. Please refresh the page."
            
        return True, None
    except (ValueError, AttributeError):
        return False, "Invalid token format."

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
    form_token = generate_security_token()
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "year": datetime.now().year,
        "success": success,
        "error": error,
        "form_token": form_token
    })

@app.post("/contact", response_class=HTMLResponse)
@limiter.limit("3/minute")
async def submit_contact(
    request: Request,
    name: str = Form(..., min_length=2, max_length=100),
    email: str = Form(...),
    subject: str = Form(..., min_length=3, max_length=200),
    message: str = Form(..., min_length=10, max_length=5000),
    website_hp: Optional[str] = Form(None), # Honeypot field
    form_token: str = Form(...)
):
    try:
        # Validate email manually because it is a regex based check
        is_valid = is_valid_email(email.strip()) if email else False
        
        if not is_valid:
            new_token = generate_security_token()
            return templates.TemplateResponse("contact.html", {
                "request": request,
                "year": datetime.now().year,
                "error": "Please enter a valid email address.",
                "form_token": new_token,
                "form_data": {
                    "name": name,
                    "email": email,
                    "subject": subject,
                    "message": message
                }
            })
            
        # Verify Invisible Security (Honeypot + Time)
        is_secure, security_msg = verify_security_token(form_token, website_hp)
        if not is_secure:
            new_token = generate_security_token()
            return templates.TemplateResponse("contact.html", {
                "request": request,
                "year": datetime.now().year,
                "error": security_msg,
                "form_token": new_token,
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
            new_token = generate_security_token()
            error_message = email_error if email_error else "Sorry, there was an error sending your message. Please try again later or contact me directly via email."
            return templates.TemplateResponse("contact.html", {
                "request": request,
                "year": datetime.now().year,
                "error": error_message,
                "form_token": new_token,
                "form_data": {
                    "name": name,
                    "email": email,
                    "subject": subject,
                    "message": message
                }
            })
            
    except Exception as e:
        new_token = generate_security_token()
        return templates.TemplateResponse("contact.html", {
            "request": request,
            "title": "Contact - Mahadev Chavan | Data Science Engineer",
            "year": datetime.now().year,
            "error": "An unexpected error occurred. Please try again later.",
            "form_token": new_token,
            "form_data": {
                "name": name,
                "email": email,
                "subject": subject,
                "message": message
            }
        })
