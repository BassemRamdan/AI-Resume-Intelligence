"""
Career Knowledge Base & Taxonomy.
Defines required skills, preferred skills, project patterns,
education criteria, and experience indicators for career roles across all 24 dataset domains.
"""

CAREER_TAXONOMY = {
    # IT & Software Engineering
    "Software Engineer": {
        "domain": "INFORMATION-TECHNOLOGY",
        "skills": ["Python", "Java", "C++", "JavaScript", "TypeScript", "SQL", "Git", "REST APIs", "Docker", "Linux"],
        "project_keywords": ["api", "web application", "backend", "full stack", "microservices", "database", "crud", "frontend"],
        "education_keywords": ["computer science", "software engineering", "computer engineering", "information technology", "informatics"],
        "experience_keywords": ["developer", "software engineer", "programmer", "backend engineer", "full stack engineer"]
    },
    "Machine Learning Engineer": {
        "domain": "INFORMATION-TECHNOLOGY",
        "skills": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "Scikit-Learn", "NumPy", "Pandas", "Docker", "SQL"],
        "project_keywords": ["classification", "regression", "neural network", "deep learning", "nlp", "computer vision", "model training", "prediction"],
        "education_keywords": ["computer science", "artificial intelligence", "data science", "machine learning", "computational engineering"],
        "experience_keywords": ["machine learning engineer", "ai engineer", "data scientist", "ml researcher", "algorithm developer"]
    },
    "Data Scientist": {
        "domain": "INFORMATION-TECHNOLOGY",
        "skills": ["Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Machine Learning", "Matplotlib", "Seaborn", "Statistical Modeling"],
        "project_keywords": ["data analysis", "exploratory data analysis", "statistical analysis", "predictive model", "clustering", "hypothesis testing"],
        "education_keywords": ["data science", "statistics", "mathematics", "computer science", "econometrics"],
        "experience_keywords": ["data scientist", "data analyst", "quantitative analyst", "statistical researcher"]
    },
    "DevOps / Cloud Engineer": {
        "domain": "INFORMATION-TECHNOLOGY",
        "skills": ["Docker", "Kubernetes", "AWS", "Azure", "GCP", "CI/CD", "Linux", "Bash", "Terraform", "Git"],
        "project_keywords": ["deployment", "infrastructure", "pipeline", "container", "monitoring", "cloud architecture", "automation"],
        "education_keywords": ["computer science", "information systems", "network engineering", "cloud computing"],
        "experience_keywords": ["devops engineer", "cloud architect", "site reliability engineer", "infrastructure engineer"]
    },
    
    # Business & Management
    "Business Development Manager": {
        "domain": "BUSINESS-DEVELOPMENT",
        "skills": ["Business Strategy", "Sales Management", "Market Research", "Negotiation", "Client Relationship", "Lead Generation"],
        "project_keywords": ["revenue growth", "partnership", "market expansion", "business plan", "client acquisition"],
        "education_keywords": ["business administration", "marketing", "management", "economics", "finance"],
        "experience_keywords": ["business development", "account executive", "sales manager", "commercial manager"]
    },
    "Management Consultant": {
        "domain": "CONSULTANT",
        "skills": ["Strategic Planning", "Process Optimization", "Financial Analysis", "Stakeholder Management", "Project Management"],
        "project_keywords": ["transformation", "consulting project", "efficiency improvement", "cost reduction", "benchmarking"],
        "education_keywords": ["business administration", "mba", "economics", "industrial engineering"],
        "experience_keywords": ["consultant", "strategy consultant", "management analyst", "advisor"]
    },
    
    # Finance & Accounting
    "Financial Analyst": {
        "domain": "FINANCE",
        "skills": ["Financial Modeling", "Valuation", "Excel", "SQL", "Risk Management", "Accounting", "Reporting"],
        "project_keywords": ["portfolio analysis", "cash flow modeling", "investment analysis", "budget forecasting", "variance analysis"],
        "education_keywords": ["finance", "economics", "accounting", "banking", "commerce"],
        "experience_keywords": ["financial analyst", "investment analyst", "portfolio manager", "credit analyst"]
    },
    "Accountant": {
        "domain": "ACCOUNTANT",
        "skills": ["General Ledger", "Auditing", "Tax Preparation", "Balance Sheet", "Reconciliation", "QuickBooks", "GAAP"],
        "project_keywords": ["annual audit", "tax filing", "payroll processing", "financial statements", "accounts payable"],
        "education_keywords": ["accounting", "finance", "auditing", "commerce"],
        "experience_keywords": ["accountant", "auditor", "tax consultant", "bookkeeper"]
    },

    # Digital Media & Design
    "Digital Media Specialist": {
        "domain": "DIGITAL-MEDIA",
        "skills": ["Digital Marketing", "Content Creation", "SEO", "Social Media Marketing", "Video Editing", "Graphic Design"],
        "project_keywords": ["campaign", "branding", "audience engagement", "social media strategy", "media production"],
        "education_keywords": ["digital media", "mass communication", "journalism", "multimedia", "graphic design"],
        "experience_keywords": ["media specialist", "content creator", "digital marketer", "social media manager"]
    },
    "UI/UX Designer": {
        "domain": "DESIGNER",
        "skills": ["Figma", "Adobe XD", "Wireframing", "Prototyping", "User Research", "Usability Testing", "Design Systems"],
        "project_keywords": ["user interface", "user experience", "app redesign", "design system", "mockup", "prototype"],
        "education_keywords": ["design", "human computer interaction", "interaction design", "fine arts"],
        "experience_keywords": ["ui designer", "ux designer", "product designer", "interaction designer"]
    },

    # Human Resources
    "Human Resources Specialist": {
        "domain": "HR",
        "skills": ["Talent Acquisition", "Recruitment", "Employee Relations", "Performance Management", "HRIS", "Onboarding"],
        "project_keywords": ["recruitment campaign", "training program", "policy development", "retention strategy"],
        "education_keywords": ["human resources", "organizational psychology", "business administration", "public administration"],
        "experience_keywords": ["hr specialist", "talent acquisition", "recruiter", "hr manager"]
    },

    # Healthcare & Engineering
    "Clinical Healthcare Professional": {
        "domain": "HEALTHCARE",
        "skills": ["Patient Care", "Clinical Diagnosis", "Medical Records", "Healthcare Compliance", "Pharmacology"],
        "project_keywords": ["patient management", "clinical trial", "health initiative", "medical research"],
        "education_keywords": ["medicine", "nursing", "pharmacy", "biomedical science", "public health"],
        "experience_keywords": ["physician", "nurse", "clinical practitioner", "medical officer"]
    },
    "Civil / Structural Engineer": {
        "domain": "ENGINEERING",
        "skills": ["AutoCAD", "Structural Analysis", "Project Management", "Site Inspection", "Construction Management"],
        "project_keywords": ["building design", "infrastructure project", "structural calculation", "site planning"],
        "education_keywords": ["civil engineering", "structural engineering", "construction engineering"],
        "experience_keywords": ["civil engineer", "structural engineer", "site supervisor", "project engineer"]
    }
}
