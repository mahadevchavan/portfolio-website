🌐 Portfolio Website (FastAPI)

This repository contains my personal portfolio website built with FastAPI and Jinja2.
It showcases my projects, skills, and includes a fully working contact form with email delivery.

🚀 Live Site: https://mahadevchavan.com/


✨ What this project does

* Serves dynamic pages using FastAPI + Jinja2
* Displays Home, About, Projects, and Contact pages
* Handles contact form submissions
* Validates input (name, email, subject, message)
* Sends emails via SMTP (Gmail App Password)
* Uses environment variables for security


🛠 Tech Stack

* Backend: FastAPI (Python)
* Frontend: HTML, CSS (Tailwind), Jinja2
* Email: SMTP (Gmail)
* Deployment-ready

▶️ Run locally

* pip install -r requirements.txt
* uvicorn main:app --reload

Then open:
* http://127.0.0.1:8000

📂 Project Structure

* static/       → CSS, images  
* templates/    → HTML templates  
* main.py       → FastAPI app  
* requirements.txt
