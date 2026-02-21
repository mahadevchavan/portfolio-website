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

def get_projects():
    return [
      {
        'title': 'Large Language Model Fine-tuning Platform',
        'category': 'Generative AI',
        'cat_class': 'bg-green-100 text-green-800',
        'desc': 'Developed an end-to-end platform for fine-tuning large language models (LLMs) on custom datasets. The system supports multiple model architectures including GPT, BERT, and T5 variants, with automated hyperparameter tuning and model evaluation pipelines.',
        'icon': 'fas fa-robot',
        'gradient': 'from-blue-500 to-purple-600',
        'tags': [
          {'name': 'PyTorch', 'class': 'bg-purple-100 text-purple-800'},
          {'name': 'Transformers', 'class': 'bg-purple-100 text-purple-800'},
          {'name': 'Hugging Face', 'class': 'bg-purple-100 text-purple-800'},
          {'name': 'AWS SageMaker', 'class': 'bg-purple-100 text-purple-800'},
          {'name': 'Docker', 'class': 'bg-purple-100 text-purple-800'}
        ],
        'links': [
          {'text': 'View Code →', 'url': '#', 'class': 'text-green-600 hover:text-green-700'},
          {'text': 'Read Paper →', 'url': '#', 'class': 'text-blue-600 hover:text-blue-700'}
        ]
      },
      {
        'title': 'AI-Powered Image Generation System',
        'category': 'Deep Learning',
        'cat_class': 'bg-purple-100 text-purple-800',
        'desc': 'Built a state-of-the-art image generation system using diffusion models and GANs. The system can generate high-quality images from text prompts with fine-grained control over style, composition, and artistic elements. Achieved FID score of 8.5 on benchmark datasets.',
        'icon': 'fas fa-palette',
        'gradient': 'from-green-500 to-teal-600',
        'tags': [
          {'name': 'TensorFlow', 'class': 'bg-purple-100 text-purple-800'},
          {'name': 'Stable Diffusion', 'class': 'bg-purple-100 text-purple-800'},
          {'name': 'GANs', 'class': 'bg-purple-100 text-purple-800'},
          {'name': 'CUDA', 'class': 'bg-purple-100 text-purple-800'},
          {'name': 'Flask API', 'class': 'bg-purple-100 text-purple-800'}
        ],
        'links': [
          {'text': 'View Code →', 'url': '#', 'class': 'text-green-600 hover:text-green-700'},
          {'text': 'Live Demo →', 'url': '#', 'class': 'text-blue-600 hover:text-blue-700'}
        ]
      },
      {
        'title': 'Real-time Predictive Analytics Platform',
        'category': 'Machine Learning',
        'cat_class': 'bg-green-100 text-green-800',
        'desc': 'Designed and deployed a scalable ML platform for real-time predictions on streaming data. The system processes millions of events per second using distributed computing and serves predictions with sub-10ms latency. Implemented automated model retraining and A/B testing framework.',
        'icon': 'fas fa-chart-line',
        'gradient': 'from-green-500 to-blue-600',
        'tags': [
          {'name': 'Apache Spark', 'class': 'bg-green-100 text-green-800'},
          {'name': 'Kafka', 'class': 'bg-green-100 text-green-800'},
          {'name': 'XGBoost', 'class': 'bg-blue-100 text-blue-800'},
          {'name': 'Kubernetes', 'class': 'bg-blue-100 text-blue-800'},
          {'name': 'MLflow', 'class': 'bg-purple-100 text-purple-800'}
        ],
        'links': [
          {'text': 'View Code →', 'url': '#', 'class': 'text-green-600 hover:text-green-700'},
          {'text': 'Case Study →', 'url': '#', 'class': 'text-blue-600 hover:text-blue-700'}
        ]
      },
      {
        'title': 'Medical Image Analysis with Deep Learning',
        'category': 'Computer Vision',
        'cat_class': 'bg-blue-100 text-blue-800',
        'desc': 'Developed a deep learning system for automated medical image analysis and diagnosis assistance. The model uses convolutional neural networks (CNNs) and attention mechanisms to detect anomalies in medical scans with 94% accuracy. Implemented explainable AI features for clinical interpretability.',
        'icon': 'fas fa-microscope',
        'gradient': 'from-blue-500 to-purple-600',
        'tags': [
          {'name': 'PyTorch', 'class': 'bg-blue-100 text-blue-800'},
          {'name': 'ResNet', 'class': 'bg-blue-100 text-blue-800'},
          {'name': 'Vision Transformers', 'class': 'bg-purple-100 text-purple-800'},
          {'name': 'DICOM', 'class': 'bg-purple-100 text-purple-800'},
          {'name': 'Grad-CAM', 'class': 'bg-purple-100 text-purple-800'}
        ],
        'links': [
          {'text': 'View Code →', 'url': '#', 'class': 'text-blue-600 hover:text-blue-700'},
          {'text': 'Research Paper →', 'url': '#', 'class': 'text-purple-600 hover:text-purple-700'}
        ]
      },
      {
        'title': 'Intelligent Conversational AI Assistant',
        'category': 'NLP',
        'cat_class': 'bg-pink-100 text-pink-800',
        'desc': 'Created an advanced conversational AI system using transformer architectures and reinforcement learning. The assistant can handle multi-turn conversations, maintain context, and perform complex reasoning tasks. Integrated with RAG (Retrieval-Augmented Generation) for domain-specific knowledge.',
        'icon': 'fas fa-comments',
        'gradient': 'from-purple-500 to-rose-600',
        'tags': [
          {'name': 'LangChain', 'class': 'bg-pink-100 text-pink-800'},
          {'name': 'OpenAI GPT', 'class': 'bg-pink-100 text-pink-800'},
          {'name': 'Vector DB', 'class': 'bg-pink-100 text-pink-800'},
          {'name': 'FastAPI', 'class': 'bg-pink-100 text-pink-800'},
          {'name': 'Redis', 'class': 'bg-pink-100 text-pink-800'}
        ],
        'links': [
          {'text': 'View Code →', 'url': '#', 'class': 'text-green-600 hover:text-green-700'},
          {'text': 'Try Demo →', 'url': '#', 'class': 'text-blue-600 hover:text-blue-700'}
        ]
      }
    ]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    projects = get_projects()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "year": datetime.now().year,
        "projects": projects[:3] # Pass only the first 3 projects
    })

def calculate_experience():
    experience = [
      {
        'role': 'Data Science Engineer',
        'company': 'KSolves India Limited, Pune',
        'period': 'April 2024 - Present',
        'start_date': '2024-04-01',
        'end_date': 'Current',
        'mode': 'Hybrid Mode',
        'desc': 'Developing and deploying machine learning models and AI solutions. Working on end-to-end ML pipelines, model optimization, and production-grade AI systems.'
      },
      {
        'role': 'Training Engineer',
        'company': 'Neosoft Technologies',
        'period': 'May 2022 - January 2023',
        'start_date': '2022-05-01',
        'end_date': '2023-01-31',
        'mode': '',
        'desc': 'Conducted technical training sessions and workshops. Developed training materials and curriculum for data science and machine learning topics.'
      }
    ]
    
    total_months = 0
    for job in experience:
        start = datetime.strptime(job['start_date'], "%Y-%m-%d")
        if job['end_date'] == "Current":
            end = datetime.now()
        else:
            end = datetime.strptime(job['end_date'], "%Y-%m-%d")
            
        months = (end.year - start.year) * 12 + (end.month - start.month) + 1
        total_months += months
        
        years = months // 12
        rem_months = months % 12
        job['duration'] = f"{years}.{rem_months} years" if years > 0 else f"{rem_months} months"
            
    total_years = total_months // 12
    total_rem_months = total_months % 12
    total_experience = f"{total_years}.{total_rem_months} years"
    
    return experience, total_experience

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    experience_data, total_exp = calculate_experience()
    return templates.TemplateResponse("about.html", {
        "request": request,
        "year": datetime.now().year,
        "experience": experience_data,
        "total_experience": total_exp
    })

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
