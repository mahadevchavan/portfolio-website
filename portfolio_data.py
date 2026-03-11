from datetime import datetime

def get_projects():
    return [
      {
        'title': 'Large Language Model Fine-tuning Platform',
        'category': 'Generative AI',
        'cat_class': 'bg-green-100 text-green-800',
        'desc': 'Developed an end-to-end platform for fine-tuning LLMs on custom datasets. Reduced training costs by 40% using LoRA adapters and quantization. The system supports GPT, BERT, and T5 variants with automated evaluation pipelines.',
        'image': '/static/project_llm.png',
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
        'image': '/static/project_image_gen.png',
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
        'image': '/static/project_analytics.png',
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
        'image': '/static/project_medical.png',
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
        'image': '/static/project_chat.png',
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
      {
          'name': 'Generative AI with Large Language Models', 
          'issuer': 'Coursera', 
          'date': 'August 28, 2025', 
          'meta': 'Credential ID • 2PT7EW8G5857', 
          'border_class': 'border-emerald-600',
          'text_class': 'text-emerald-600',
          'bg_hover': 'hover:bg-emerald-50'
      },
      {
          'name': 'Fundamental course in the AWS Machine Learning Scholarship!', 
          'issuer': 'Udacity', 
          'date': 'Aug 2020', 
          'meta': 'Issue Date • Aug 2020', 
          'border_class': 'border-sky-600',
          'text_class': 'text-sky-600',
          'bg_hover': 'hover:bg-sky-50'
      },
      {
          'name': 'Microsoft Technology Associate: Windows Server Administration Fundamentals (MTA)', 
          'issuer': 'Microsoft', 
          'date': 'Jun 2019', 
          'meta': 'Issue Date • Jun 2019', 
          'border_class': 'border-violet-600',
          'text_class': 'text-violet-600',
          'bg_hover': 'hover:bg-violet-50'
      }
    ]
    
    return skills, expertise, education, certifications


# Compute experience once instead of every function call
_cached_experience = None
_cached_total_experience = None
_last_calc_date = None

def get_experience():
    global _cached_experience, _cached_total_experience, _last_calc_date
    
    # Update cache if it"s a new month to avoid recalculating on every request
    current_month = datetime.now().strftime("%Y-%m")
    if _last_calc_date == current_month and _cached_experience:
        return _cached_experience, _cached_total_experience

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
    total_exp = f"{total_years}.{total_rem_months} years"
    
    _cached_experience = experience
    _cached_total_experience = total_exp
    _last_calc_date = current_month
    
    return experience, total_exp
