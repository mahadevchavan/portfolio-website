from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
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
RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY", "your_site_key_here")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY", "your_secret_key_here")

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
        'desc': 'Developed an end-to-end platform for fine-tuning LLMs on custom datasets. Reduced training costs by 40% using LoRA adapters and quantization. The system supports GPT, BERT, and T5 variants with automated evaluation pipelines.',
        'image': None, # Example: '/static/llm-dashboard.jpg'
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
        'image': None,
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
        'desc': 'Designed a scalable ML platform processing 50k+ events per second with sub-10ms latency. The system leverages distributed computing for real-time predictions and includes an automated retraining framework that improved model freshness by 200%.',
        'image': None,
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
        'desc': 'Developed a deep learning system for automated medical image analysis, achieving 94% diagnostic accuracy. The model uses CNNs and attention mechanisms to detect anomalies, reducing manual review time for radiologists by approximately 30%.',
        'image': None,
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
        'desc': 'Created an advanced conversational AI system using RAG (Retrieval-Augmented Generation). The assistant handles multi-turn conversations with context retention, reducing customer support ticket volume by 45% in pilot testing.',
        'image': None,
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

def get_static_about_data():
    skills = [
      {
        'title': 'Programming Languages',
        'items': [
          {'name': 'Python', 'class': 'bg-emerald-100 text-emerald-700'},
          {'name': 'R', 'class': 'bg-emerald-100 text-emerald-700'},
          {'name': 'SQL', 'class': 'bg-emerald-100 text-emerald-700'},
          {'name': 'Scala', 'class': 'bg-emerald-100 text-emerald-700'}
        ]
      },
      {
        'title': 'ML/DL Frameworks',
        'items': [
          {'name': 'TensorFlow', 'class': 'bg-sky-100 text-sky-700'},
          {'name': 'PyTorch', 'class': 'bg-sky-100 text-sky-700'},
          {'name': 'Keras', 'class': 'bg-sky-100 text-sky-700'},
          {'name': 'Scikit-learn', 'class': 'bg-sky-100 text-sky-700'}
        ]
      },
      {
        'title': 'Generative AI',
        'items': [
          {'name': 'Transformers', 'class': 'bg-violet-100 text-violet-700'},
          {'name': 'Hugging Face', 'class': 'bg-violet-100 text-violet-700'},
          {'name': 'LangChain', 'class': 'bg-violet-100 text-violet-700'},
          {'name': 'OpenAI API', 'class': 'bg-violet-100 text-violet-700'}
        ]
      },
      {
        'title': 'Tools & Technologies',
        'items': [
          {'name': 'Docker', 'class': 'bg-emerald-100 text-emerald-700'},
          {'name': 'Kubernetes', 'class': 'bg-emerald-100 text-emerald-700'},
          {'name': 'MLflow', 'class': 'bg-sky-100 text-sky-700'},
          {'name': 'Airflow', 'class': 'bg-sky-100 text-sky-700'},
          {'name': 'AWS/GCP', 'class': 'bg-violet-100 text-violet-700'}
        ]
      }
    ]
    
    expertise = [
      'Neural Networks & Deep Learning Architectures',
      'Large Language Models (LLMs) & Fine-tuning',
      'Computer Vision & Image Generation',
      'Natural Language Processing (NLP)',
      'Model Training, Optimization & MLOps',
      'Production ML System Design'
    ]
    
    education = [
      {'degree': 'Diploma of Education, Artificial Intelligence and Machine Learning', 'school': 'University of Hyderabad', 'year': '2021 - 2022'},
      {'degree': 'Master of Science in Computer Science', 'school': 'Savitribai Phule Pune University', 'year': '2018 - 2020'},
      {'degree': 'Bachelor of Science in Computer Science', 'school': 'Savitribai Phule Pune University', 'year': '2015 - 2018'}
    ]
    
    certifications = [
      {'name': 'Generative AI with Large Language Models', 'issuer': 'Coursera', 'date': 'August 28, 2025', 'meta': 'Credential ID • 2PT7EW8G5857', 'color': 'emerald'},
      {'name': 'Fundamental course in the AWS Machine Learning Scholarship!', 'issuer': 'Udacity', 'date': 'Aug 2020', 'meta': 'Issue Date • Aug 2020', 'color': 'sky'},
      {'name': 'Microsoft Technology Associate: Windows Server Administration Fundamentals (MTA)', 'issuer': 'Microsoft', 'date': 'Jun 2019', 'meta': 'Issue Date • Jun 2019', 'color': 'violet'}
    ]
    
    return skills, expertise, education, certifications

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    projects = get_projects()
    experience, total_experience = calculate_experience()
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

def calculate_experience():
    experience = [
      {
        'role': 'Data Science Engineer',
        'company': 'KSolves India Limited, Pune',
        'period': 'April 2024 - Present',
        'start_date': '2024-04-01',
        'end_date': 'Current',
        'mode': 'Hybrid Mode',
        'desc': """
<ul class="list-disc pl-4 space-y-4 mt-2">
    <li>
        <span class="font-bold text-gray-900">ML-Powered Automation (Salesforce):</span> Engineered an end-to-end machine learning ticket routing system integrated with Salesforce. Designed custom feature engineering logic to evaluate ticket complexity, resolution trends, and engineer efficiency.
        <div class="mt-1 text-emerald-700 font-medium text-sm">Impact: Achieved a ~60% reduction in manual intervention, drastically improving service response times and customer satisfaction.</div>
    </li>
    <li>
        <span class="font-bold text-gray-900">NLP & Search Systems:</span> Built an automated backend system using Python, Pandas, and advanced NLP (similarity search) to precisely match customer requirements with relevant inventory materials.
        <div class="mt-1 text-emerald-700 font-medium text-sm">Impact: Streamlined material quantity estimation, reducing manual effort by ~75% while increasing decision accuracy.</div>
    </li>
    <li>
        <span class="font-bold text-gray-900">Computer Vision Solutions:</span> Developed a real-time Computer Vision POC for applicant monitoring. Leveraged facial landmarks, gaze estimation, and geometric analysis to track eye movement and attention during coding assessments.
    </li>
    <li>
        <span class="font-bold text-gray-900">Predictive Analytics:</span> Built and deployed an AI-powered predictive maintenance model for enterprise HVAC systems, enabling proactive monitoring and significant operational efficiency improvements for the client.
    </li>
    <li>
        <span class="font-bold text-gray-900">MLOps & Deployment:</span> Collaborated across teams to deploy, maintain, and scale production-ready AI solutions using Docker and custom data ingestion pipelines (XML-RPC APIs).
    </li>
</ul>
<div class="mt-4 flex flex-wrap gap-2 border-t border-gray-100 pt-3">
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">Salesforce</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">ML Automation</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">NLP</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">Python</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">Computer Vision</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">Predictive Analytics</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">MLOps</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">Docker</span>
</div>
"""
      },
      {
        'role': 'Trainee Engineer',
        'company': 'Neosoft Technologies',
        'period': 'May 2022 - January 2023',
        'start_date': '2022-05-01',
        'end_date': '2023-01-31',
        'mode': '',
        'desc': """
<ul class="list-disc pl-4 space-y-4 mt-2">
    <li>
        Conducted comprehensive exploratory data analysis (EDA) using Pandas, SQL, and Matplotlib to extract actionable business insights.
    </li>
    <li>
        Developed and trained Computer Vision models for image processing tasks, utilizing OpenCV and CNN architectures.
    </li>
    <li>
        Supported the end-to-end machine learning lifecycle, from initial data preparation to model training and performance evaluation.
    </li>
</ul>
<div class="mt-4 flex flex-wrap gap-2 border-t border-gray-100 pt-3">
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">EDA</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">Pandas</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">SQL</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">Computer Vision</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">OpenCV</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">CNN</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">ML Lifecycle</span>
</div>
"""
      },
      {
        'role': 'Data Science Intern',
        'company': 'Sciffer Analytics Pte Ltd',
        'period': 'May 2021 - Aug 2021',
        'start_date': '2021-05-01',
        'end_date': '2021-08-31',
        'mode': 'Remote',
        'desc': """
<ul class="list-disc pl-4 space-y-4 mt-2">
    <li>
        Sourced, curated, and annotated large-scale, complex datasets to directly support the training of Computer Vision models.
    </li>
    <li>
        Supervised a 5-person data annotation team during interim periods, ensuring workflow continuity, task delegation, and strict data quality standards.
    </li>
</ul>
<div class="mt-4 flex flex-wrap gap-2 border-t border-gray-100 pt-3">
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">Data Annotation</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">Computer Vision</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">Team Supervision</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">Data Quality</span>
    <span class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded font-semibold">Workflow Management</span>
</div>
"""
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

def verify_recaptcha(token: str) -> bool:
    """Verify Google reCAPTCHA token"""
    if not token:
        return False
        
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = urllib.parse.urlencode({
        'secret': RECAPTCHA_SECRET_KEY,
        'response': token
    }).encode()
    
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        return result.get('success', False)

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
        "error": error,
        "recaptcha_site_key": RECAPTCHA_SITE_KEY
    })

@app.post("/contact", response_class=HTMLResponse)
async def submit_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    recaptcha_response: str = Form(..., alias="g-recaptcha-response")
):
    try:
        # Validate form data using simple validation
        is_valid, error_message = validate_contact_form(name, email, subject, message)
        
        if not is_valid:
            return templates.TemplateResponse("contact.html", {
                "request": request,
                "year": datetime.now().year,
                "error": error_message,
                "recaptcha_site_key": RECAPTCHA_SITE_KEY,
                "form_data": {
                    "name": name,
                    "email": email,
                    "subject": subject,
                    "message": message
                }
            })
            
        # Verify reCAPTCHA
        if not verify_recaptcha(recaptcha_response):
            return templates.TemplateResponse("contact.html", {
                "request": request,
                "year": datetime.now().year,
                "error": "reCAPTCHA verification failed. Please try again.",
                "recaptcha_site_key": RECAPTCHA_SITE_KEY,
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
                "recaptcha_site_key": RECAPTCHA_SITE_KEY,
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
            "recaptcha_site_key": RECAPTCHA_SITE_KEY,
            "form_data": {
                "name": name,
                "email": email,
                "subject": subject,
                "message": message
            }
        })
