"""
Career Knowledge Base & Multi-Domain Taxonomy.
Comprehensive Knowledge Base covering ALL 24 dataset domains:
ACCOUNTANT, ADVOCATE, AGRICULTURE, APPAREL, ARTS, AUTOMOBILE, AVIATION, BANKING,
BPO, BUSINESS-DEVELOPMENT, CHEF, CONSTRUCTION, CONSULTANT, DESIGNER, DIGITAL-MEDIA,
ENGINEERING, FINANCE, FITNESS, HEALTHCARE, HR, INFORMATION-TECHNOLOGY,
PUBLIC-RELATIONS, SALES, TEACHER.

Defines required skills, project patterns, education criteria, experience indicators,
and structured 3-phase career roadmaps for each role.
"""

CAREER_TAXONOMY = {
    # 1. INFORMATION-TECHNOLOGY
    "Software Engineer": {
        "domain": "INFORMATION-TECHNOLOGY",
        "skills": ["Python", "Java", "C#", "C++", "JavaScript", "TypeScript", "SQL", "Git", "REST APIs", "Docker", "Linux"],
        "project_keywords": ["api", "web application", "backend", "full stack", "microservices", "database", "crud", "frontend", "system architecture"],
        "education_keywords": ["computer science", "software engineering", "computer engineering", "information technology", "informatics"],
        "experience_keywords": ["developer", "software engineer", "programmer", "backend engineer", "full stack engineer"],
        "roadmap": {
            "phase_1": "Core CS Fundamentals: Data Structures, Algorithms (LeetCode/Codeforces), OOP, Git, SQL, and Clean Code Architecture.",
            "phase_2": "Backend/Full-Stack Mastery: Build production REST/GraphQL APIs, Relational & NoSQL databases, Docker containerization, and unit testing (xUnit/PyTest/Jest).",
            "phase_3": "System Design & Cloud: Distributed systems, microservices, caching (Redis), message queues (Kafka/RabbitMQ), and CI/CD pipelines."
        }
    },
    "Machine Learning Engineer": {
        "domain": "INFORMATION-TECHNOLOGY",
        "skills": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "Scikit-Learn", "NumPy", "Pandas", "Docker", "SQL", "MLOps"],
        "project_keywords": ["classification", "regression", "neural network", "deep learning", "nlp", "computer vision", "model training", "prediction", "transformers"],
        "education_keywords": ["computer science", "artificial intelligence", "data science", "machine learning", "computational engineering"],
        "experience_keywords": ["machine learning engineer", "ai engineer", "data scientist", "ml researcher", "algorithm developer"],
        "roadmap": {
            "phase_1": "Math & ML Foundations: Linear Algebra, Calculus, Statistics, NumPy, Pandas, and Scikit-Learn baseline modeling.",
            "phase_2": "Deep Learning & NLP/CV: PyTorch/TensorFlow, Transformers (Hugging Face), CNNs/RNNs, and fine-tuning pretrained LLMs.",
            "phase_3": "Production MLOps: Model quantization (ONNX), containerized serving (FastAPI/Triton), MLflow experiment tracking, and CI/CD pipelines."
        }
    },
    "Data Scientist": {
        "domain": "INFORMATION-TECHNOLOGY",
        "skills": ["Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Machine Learning", "Matplotlib", "Seaborn", "Statistical Modeling", "Tableau", "Power BI"],
        "project_keywords": ["data analysis", "exploratory data analysis", "statistical analysis", "predictive model", "clustering", "hypothesis testing", "dashboard"],
        "education_keywords": ["data science", "statistics", "mathematics", "computer science", "econometrics"],
        "experience_keywords": ["data scientist", "data analyst", "quantitative analyst", "statistical researcher"],
        "roadmap": {
            "phase_1": "Data Wrangling & Stats: Advanced SQL, Pandas, EDA, Probability, Hypothesis Testing, and Data Storytelling.",
            "phase_2": "Predictive Modeling: Supervised & unsupervised learning with Scikit-Learn, Feature Engineering, and model evaluation metrics.",
            "phase_3": "Advanced Analytics & BI: Interactive BI dashboards (Tableau/Power BI), A/B testing frameworks, and scalable BigQuery/Spark processing."
        }
    },
    "DevOps / Cloud Engineer": {
        "domain": "INFORMATION-TECHNOLOGY",
        "skills": ["Docker", "Kubernetes", "AWS", "Azure", "GCP", "CI/CD", "Linux", "Bash", "Terraform", "Git", "Prometheus", "Grafana"],
        "project_keywords": ["deployment", "infrastructure", "pipeline", "container", "monitoring", "cloud architecture", "automation", "iac"],
        "education_keywords": ["computer science", "information systems", "network engineering", "cloud computing"],
        "experience_keywords": ["devops engineer", "cloud architect", "site reliability engineer", "infrastructure engineer"],
        "roadmap": {
            "phase_1": "Linux & Networking: Advanced Linux CLI, Bash scripting, TCP/IP, DNS, SSL/TLS, and Git version control.",
            "phase_2": "Containers & CI/CD: Docker containerization, multi-stage builds, GitHub Actions / GitLab CI pipelines, and cloud platform fundamentals (AWS/Azure).",
            "phase_3": "Orchestration & IaC: Kubernetes cluster management (Helm), Terraform Infrastructure as Code, Prometheus/Grafana monitoring, and SRE best practices."
        }
    },
    "Cybersecurity Analyst": {
        "domain": "INFORMATION-TECHNOLOGY",
        "skills": ["Network Security", "Penetration Testing", "SIEM", "Wireshark", "Vulnerability Assessment", "Firewalls", "Incident Response", "Linux", "Python"],
        "project_keywords": ["security audit", "vulnerability scan", "threat detection", "penetration test", "incident response", "firewall configuration"],
        "education_keywords": ["cybersecurity", "information security", "computer science", "network engineering"],
        "experience_keywords": ["security analyst", "soc analyst", "penetration tester", "security engineer"],
        "roadmap": {
            "phase_1": "Networking & System Security: Network protocols, Linux/Windows administration, Wireshark packet analysis, and security principles (CIA Triad).",
            "phase_2": "Defensive Security & SOC: SIEM monitoring (Splunk/ELK), log analysis, vulnerability scanning (Nessus), and incident response procedures.",
            "phase_3": "Offensive Security & Compliance: Penetration testing (Metasploit, Burp Suite), ISO 27001 / NIST frameworks, and certifications (CompTIA Security+, CEH, OSCP)."
        }
    },

    # 2. ACCOUNTANT
    "Senior Accountant & Tax Specialist": {
        "domain": "ACCOUNTANT",
        "skills": ["General Ledger", "Auditing", "Tax Preparation", "Balance Sheet", "Reconciliation", "QuickBooks", "GAAP", "Excel", "Financial Reporting", "ERP Systems"],
        "project_keywords": ["annual audit", "tax filing", "payroll processing", "financial statements", "accounts payable", "reconciliation", "erp implementation"],
        "education_keywords": ["accounting", "finance", "auditing", "commerce", "business administration"],
        "experience_keywords": ["accountant", "auditor", "tax consultant", "bookkeeper", "controller"],
        "roadmap": {
            "phase_1": "Foundational Accounting: Master double-entry bookkeeping, GAAP/IFRS standards, Balance Sheets, and Advanced Excel modeling.",
            "phase_2": "Financial Systems & Compliance: Hands-on ERP (SAP/Oracle/QuickBooks), corporate tax preparation, and internal controls.",
            "phase_3": "Strategic Accounting & Certification: Forensic auditing, cash flow optimization, financial statement consolidation, and CPA/CMA certification."
        }
    },

    # 3. ADVOCATE
    "Corporate Legal Counsel & Advocate": {
        "domain": "ADVOCATE",
        "skills": ["Legal Research", "Contract Drafting", "Litigation", "Corporate Governance", "Compliance", "Dispute Resolution", "Intellectual Property", "Negotiation"],
        "project_keywords": ["contract review", "litigation brief", "regulatory compliance", "legal audit", "arbitration", "intellectual property filing"],
        "education_keywords": ["law", "llb", "llm", "juris doctor", "legal studies"],
        "experience_keywords": ["lawyer", "advocate", "legal counsel", "attorney", "legal advisor"],
        "roadmap": {
            "phase_1": "Legal Foundations: Constitutional law, contract law, procedural litigation rules, and comprehensive legal research databases (LexisNexis/Westlaw).",
            "phase_2": "Corporate & Contract Practice: Commercial contract drafting, compliance auditing, employment law, and alternative dispute resolution (ADR).",
            "phase_3": "Senior Advisory: Cross-border M&A transactions, corporate governance frameworks, intellectual property strategy, and Bar leadership."
        }
    },

    # 4. AGRICULTURE
    "Agronomist & Agricultural Specialist": {
        "domain": "AGRICULTURE",
        "skills": ["Crop Management", "Soil Science", "Irrigation Systems", "Agribusiness", "Pest Management", "Sustainable Agriculture", "Precision Farming", "GIS"],
        "project_keywords": ["crop yield optimization", "soil analysis", "irrigation design", "sustainable farming", "precision agriculture", "farm management"],
        "education_keywords": ["agriculture", "agronomy", "soil science", "agricultural engineering", "horticulture"],
        "experience_keywords": ["agronomist", "farm manager", "agricultural officer", "agricultural consultant"],
        "roadmap": {
            "phase_1": "Agricultural Science Basics: Soil mechanics, plant physiology, crop genetics, and meteorological data analysis.",
            "phase_2": "Applied Agronomy & Irrigation: Drip irrigation systems, integrated pest management (IPM), soil nutrient balancing, and farm machinery.",
            "phase_3": "Precision & AgTech: Drone imaging, GIS mapping, IoT soil sensors, agricultural supply chain economics, and organic certification."
        }
    },

    # 5. APPAREL
    "Fashion & Apparel Designer": {
        "domain": "APPAREL",
        "skills": ["Fashion Design", "Pattern Making", "Textile Technology", "Garment Construction", "Adobe Illustrator", "Tech Packs", "Trend Forecasting", "Quality Assurance"],
        "project_keywords": ["apparel collection", "tech pack creation", "garment sample", "textile sourcing", "trend forecast", "pattern grading"],
        "education_keywords": ["fashion design", "apparel manufacturing", "textile engineering", "garment technology"],
        "experience_keywords": ["fashion designer", "apparel merchandiser", "textile designer", "pattern maker"],
        "roadmap": {
            "phase_1": "Design Foundations: Sketching, fabric anatomy, color theory, and digital CAD tools (Adobe Illustrator/Photoshop).",
            "phase_2": "Garment Engineering: Technical pack development, manual & digital pattern grading, draping, and garment sampling.",
            "phase_3": "Commercial Production: Supply chain sourcing, sustainable textile manufacturing, collection line planning, and fashion brand direction."
        }
    },

    # 6. ARTS
    "Creative Director & Visual Artist": {
        "domain": "ARTS",
        "skills": ["Visual Arts", "Creative Direction", "Illustration", "Digital Painting", "Adobe Photoshop", "Concept Art", "Typography", "Art History"],
        "project_keywords": ["art exhibition", "visual branding", "illustration series", "concept art", "storyboarding", "gallery curation"],
        "education_keywords": ["fine arts", "visual arts", "graphic design", "illustration", "art history"],
        "experience_keywords": ["artist", "creative director", "illustrator", "visual designer", "art instructor"],
        "roadmap": {
            "phase_1": "Artistic Fundamentals: Perspective drawing, anatomy, color theory, composition, and traditional media mastery.",
            "phase_2": "Digital Media & Conceptualization: Digital illustration (Procreate/Photoshop), 3D asset integration (Blender), and narrative visual storytelling.",
            "phase_3": "Creative Leadership: Brand visual direction, large-scale exhibition curation, IP development, and creative studio management."
        }
    },

    # 7. AUTOMOBILE
    "Automotive Systems Engineer": {
        "domain": "AUTOMOBILE",
        "skills": ["Automotive Engineering", "Vehicle Diagnostics", "CAD/SolidWorks", "Powertrain Systems", "CAN Bus", "Electric Vehicles (EV)", "Quality Control", "MATLAB"],
        "project_keywords": ["vehicle diagnostic system", "ev battery modeling", "powertrain optimization", "automotive cad design", "chassis simulation"],
        "education_keywords": ["automotive engineering", "mechanical engineering", "electrical engineering", "mechatronics"],
        "experience_keywords": ["automotive engineer", "vehicle technician", "automotive quality engineer", "fleet engineer"],
        "roadmap": {
            "phase_1": "Engineering Principles: Thermodynamics, fluid mechanics, CAD modeling (SolidWorks/CATIA), and automotive electrical circuits.",
            "phase_2": "Vehicle Systems & Diagnostics: ECU programming, CAN bus communication, OBD-II diagnostics, and internal combustion/transmission systems.",
            "phase_3": "EV & Autonomous Tech: Battery management systems (BMS), electric motor controls, ADAS sensors, and automotive safety standards (ISO 26262)."
        }
    },

    # 8. AVIATION
    "Aviation Operations & Aerospace Specialist": {
        "domain": "AVIATION",
        "skills": ["Flight Operations", "Aviation Safety (FAA/ICAO)", "Aircraft Maintenance", "Avionics", "Air Traffic Management", "Aerodynamics", "Logistics"],
        "project_keywords": ["flight planning", "safety management system (sms)", "aircraft inspection", "fleet maintenance scheduling", "avionics upgrade"],
        "education_keywords": ["aviation management", "aerospace engineering", "aeronautical science", "aircraft maintenance"],
        "experience_keywords": ["aviation officer", "flight dispatcher", "aircraft maintenance engineer", "aviation operations manager"],
        "roadmap": {
            "phase_1": "Aviation Basics: Aerodynamics, meteorology, air navigation, aircraft systems, and FAA/ICAO regulatory frameworks.",
            "phase_2": "Operations & Avionics: Flight dispatch protocols, avionics diagnostics, aircraft weight and balance calculation, and SMS implementation.",
            "phase_3": "Airline Leadership: Fleet reliability engineering, airport operations management, aerospace quality standards (AS9100), and IATA certifications."
        }
    },

    # 9. BANKING
    "Commercial & Investment Banking Analyst": {
        "domain": "BANKING",
        "skills": ["Commercial Banking", "Credit Risk Analysis", "Financial Modeling", "Loan Underwriting", "KYC/AML Compliance", "Core Banking Systems", "Wealth Management"],
        "project_keywords": ["credit appraisal", "loan portfolio review", "aml compliance audit", "risk assessment model", "wealth management strategy"],
        "education_keywords": ["banking", "finance", "economics", "commerce", "business administration"],
        "experience_keywords": ["banker", "credit analyst", "loan officer", "relationship manager", "branch manager"],
        "roadmap": {
            "phase_1": "Banking Operations: Retail & commercial banking instruments, double-entry financial analysis, credit scoring models, and AML/KYC regulations.",
            "phase_2": "Underwriting & Credit Risk: Debt service coverage analysis (DSCR), corporate loan underwriting, collateral valuation, and financial modeling in Excel.",
            "phase_3": "Capital Markets & Compliance: Basel III regulatory frameworks, syndicated loan facilities, treasury management, and CFA/FRM credentials."
        }
    },

    # 10. BPO
    "BPO Operations & Customer Experience Lead": {
        "domain": "BPO",
        "skills": ["BPO Operations", "Customer Support", "Service Level Agreements (SLA)", "CRM (Salesforce/Zendesk)", "Quality Monitoring", "Workforce Management (WFM)", "Call Center Analytics"],
        "project_keywords": ["sla optimization", "csat improvement program", "workforce scheduling", "customer service automation", "process migration"],
        "education_keywords": ["business administration", "communications", "information technology", "management"],
        "experience_keywords": ["bpo team lead", "customer service manager", "operations supervisor", "technical support specialist"],
        "roadmap": {
            "phase_1": "Customer Service Excellence: Multi-channel support (voice, email, chat), CRM tools (Salesforce/Zendesk), active listening, and conflict de-escalation.",
            "phase_2": "Operational Metrics & Quality: CSAT, NPS, FCR, and AHT monitoring, SLA adherence tracking, and quality assurance auditing.",
            "phase_3": "Workforce & Process Optimization: Erlang-C staffing models, conversational AI/chatbot escalation workflows, and Six Sigma Green Belt process optimization."
        }
    },

    # 11. BUSINESS-DEVELOPMENT
    "Business Development Manager": {
        "domain": "BUSINESS-DEVELOPMENT",
        "skills": ["Business Strategy", "Sales Management", "Market Research", "Negotiation", "Client Relationship", "Lead Generation", "Strategic Partnerships", "B2B Sales"],
        "project_keywords": ["revenue growth", "partnership", "market expansion", "business plan", "client acquisition", "sales pipeline"],
        "education_keywords": ["business administration", "marketing", "management", "economics", "finance"],
        "experience_keywords": ["business development manager", "account executive", "sales manager", "commercial manager"],
        "roadmap": {
            "phase_1": "Prospecting & Market Intelligence: B2B lead generation, market sizing (TAM/SAM/SOM), competitor analysis, and CRM pipeline hygiene.",
            "phase_2": "Deal Structuring & Pitching: High-stakes contract negotiation, stakeholder pitch decks, consultative selling, and partnership agreements.",
            "phase_3": "Strategic Expansion: International market entry, channel partner networks, revenue forecasting models, and executive P&L leadership."
        }
    },

    # 12. CHEF
    "Executive Chef & Culinary Director": {
        "domain": "CHEF",
        "skills": ["Culinary Arts", "Menu Engineering", "Food Safety (HACCP)", "Kitchen Operations", "Food Cost Control", "Inventory Management", "Recipe Standardization"],
        "project_keywords": ["menu redesign", "food cost reduction", "haccp food safety compliance", "culinary event management", "kitchen workflow optimization"],
        "education_keywords": ["culinary arts", "hospitality management", "food science", "hotel management"],
        "experience_keywords": ["executive chef", "sous chef", "head chef", "culinary manager"],
        "roadmap": {
            "phase_1": "Culinary Fundamentals: Classical cooking techniques, knife skills, recipe execution, and ServSafe / HACCP hygiene protocols.",
            "phase_2": "Kitchen Management & Plating: Menu development, food cost calculation (target < 30%), inventory FIFO systems, and station workflow coordination.",
            "phase_3": "Culinary Innovation & Directorship: Fine dining menu curation, farm-to-table sourcing, restaurant P&L management, and culinary team mentorship."
        }
    },

    # 13. CONSTRUCTION
    "Construction Project Manager & Civil Specialist": {
        "domain": "CONSTRUCTION",
        "skills": ["Construction Management", "AutoCAD", "Site Safety (OSHA)", "Project Scheduling (Primavera/MS Project)", "Cost Estimation", "Structural Engineering", "Quality Control"],
        "project_keywords": ["commercial building project", "structural inspection", "osha safety audit", "schedule optimization", "bill of quantities (boq)"],
        "education_keywords": ["civil engineering", "construction management", "structural engineering", "architecture"],
        "experience_keywords": ["construction manager", "site engineer", "project engineer", "civil supervisor"],
        "roadmap": {
            "phase_1": "Engineering Drawings & Safety: Blueprint reading, AutoCAD/Revit drafting, concrete & steel material properties, and OSHA site safety compliance.",
            "phase_2": "Project Controls & Estimation: Bill of Quantities (BOQ), contractor bidding, Primavera P6 / MS Project critical path scheduling, and quality testing.",
            "phase_3": "Megaproject Delivery: BIM (Building Information Modeling) 4D/5D management, LEED green building certifications, contract risk mitigation, and PMP credential."
        }
    },

    # 14. CONSULTANT
    "Management Consultant & Strategy Advisor": {
        "domain": "CONSULTANT",
        "skills": ["Strategic Planning", "Process Optimization", "Financial Analysis", "Stakeholder Management", "Project Management", "Business Case Development", "Change Management"],
        "project_keywords": ["transformation", "consulting project", "efficiency improvement", "cost reduction", "benchmarking", "operating model redesign"],
        "education_keywords": ["business administration", "mba", "economics", "industrial engineering", "management"],
        "experience_keywords": ["consultant", "strategy consultant", "management analyst", "advisor"],
        "roadmap": {
            "phase_1": "Structured Problem Solving: MECE frameworks, hypothesis-driven issue trees, quantitative data synthesis, and executive PowerPoint storytelling.",
            "phase_2": "Operational Transformation: Lean Six Sigma process mapping, organization redesign, financial valuation, and enterprise software benchmarking.",
            "phase_3": "C-Suite Advisory: Digital transformation strategy, change management execution, board-level stakeholder alignment, and partner-track practice growth."
        }
    },

    # 15. DESIGNER
    "UI/UX Product Designer": {
        "domain": "DESIGNER",
        "skills": ["Figma", "Adobe XD", "Wireframing", "Prototyping", "User Research", "Usability Testing", "Design Systems", "Interaction Design", "HTML/CSS"],
        "project_keywords": ["user interface", "user experience", "app redesign", "design system", "mockup", "prototype", "user journey map"],
        "education_keywords": ["design", "human computer interaction", "interaction design", "fine arts", "visual communication"],
        "experience_keywords": ["ui designer", "ux designer", "product designer", "interaction designer"],
        "roadmap": {
            "phase_1": "UX Research & Wireframing: User personas, journey mapping, information architecture, and low-fidelity Figma wireframing.",
            "phase_2": "UI Mastery & Design Systems: Auto-layout, component variants, typography hierarchy, accessibility (WCAG), and interactive micro-animations.",
            "phase_3": "Product Strategy & Cross-Functional Delivery: Quantitative usability metrics (SUS/HEART), engineering handoff tokens, and product vision alignment."
        }
    },

    # 16. DIGITAL-MEDIA
    "Digital Media & Content Marketing Specialist": {
        "domain": "DIGITAL-MEDIA",
        "skills": ["Digital Marketing", "Content Creation", "SEO", "Social Media Marketing", "Video Editing (Premiere/After Effects)", "Graphic Design", "Google Analytics", "Copywriting"],
        "project_keywords": ["campaign", "branding", "audience engagement", "social media strategy", "media production", "seo ranking improvement"],
        "education_keywords": ["digital media", "mass communication", "journalism", "multimedia", "graphic design", "marketing"],
        "experience_keywords": ["media specialist", "content creator", "digital marketer", "social media manager"],
        "roadmap": {
            "phase_1": "Content Production Foundations: Copywriting, Adobe Premiere/Canva asset creation, social channel algorithms, and basic on-page SEO.",
            "phase_2": "Performance Marketing & Analytics: Meta & Google Ads campaign management, Google Analytics 4 (GA4) attribution, and email marketing funnels.",
            "phase_3": "Omnichannel Media Strategy: High-production video storytelling, brand partnerships, viral growth loops, and brand reputation management."
        }
    },

    # 17. ENGINEERING
    "Mechanical & Systems Engineer": {
        "domain": "ENGINEERING",
        "skills": ["Mechanical Engineering", "SolidWorks", "AutoCAD", "Thermodynamics", "Finite Element Analysis (FEA)", "MATLAB", "Manufacturing Processes", "Quality Control"],
        "project_keywords": ["mechanical design", "fea structural simulation", "thermal analysis", "prototype fabrication", "manufacturing optimization"],
        "education_keywords": ["mechanical engineering", "mechatronics", "aerospace engineering", "industrial engineering"],
        "experience_keywords": ["mechanical engineer", "design engineer", "systems engineer", "manufacturing engineer"],
        "roadmap": {
            "phase_1": "Core Mechanical Sciences: Statics, dynamics, mechanics of materials, fluid dynamics, and 3D CAD modeling (SolidWorks/Inventor).",
            "phase_2": "Simulation & Prototyping: Finite Element Analysis (ANSYS), thermal CFD modeling, CNC machining, and rapid 3D printing prototyping.",
            "phase_3": "Systems Engineering: DFM/DFA (Design for Manufacturing/Assembly), Six Sigma tolerancing, GD&T standards, and multidisciplinary systems integration."
        }
    },

    # 18. FINANCE
    "Financial Analyst & Portfolio Specialist": {
        "domain": "FINANCE",
        "skills": ["Financial Modeling", "Valuation", "Excel", "SQL", "Risk Management", "Corporate Finance", "Portfolio Management", "Reporting", "Bloomberg Terminal"],
        "project_keywords": ["portfolio analysis", "cash flow modeling", "investment analysis", "budget forecasting", "variance analysis", "dcf valuation"],
        "education_keywords": ["finance", "economics", "accounting", "banking", "commerce"],
        "experience_keywords": ["financial analyst", "investment analyst", "portfolio manager", "credit analyst"],
        "roadmap": {
            "phase_1": "Financial Statement Analysis: 3-statement financial modeling in Excel, DCF valuation, ratio analysis, and capital budgeting.",
            "phase_2": "Quantitative Modeling & Risk: Statistical portfolio optimization (Sharpe Ratio/VaR), Python for financial data (yfinance/pandas), and SQL querying.",
            "phase_3": "Investment Strategy & Advisory: Private equity / venture capital deal structuring, M&A due diligence, and CFA Charterholder track."
        }
    },

    # 19. FITNESS
    "Fitness & Wellness Coach": {
        "domain": "FITNESS",
        "skills": ["Personal Training", "Exercise Physiology", "Sports Nutrition", "Strength & Conditioning", "Injury Prevention", "Kinesiology", "Client Assessment"],
        "project_keywords": ["fitness transformation program", "athletic conditioning plan", "nutrition meal plan", "biomechanical posture correction"],
        "education_keywords": ["exercise science", "kinesiology", "sports medicine", "physical education"],
        "experience_keywords": ["fitness trainer", "strength coach", "wellness consultant", "gym instructor"],
        "roadmap": {
            "phase_1": "Anatomy & Biomechanics: Human anatomy, muscle mechanics, energy systems, and certified personal trainer credentials (NASM / ACE / ISSA).",
            "phase_2": "Program Periodization & Nutrition: Progressive overload periodization, macronutrient calculation, functional movement screening, and injury rehabilitation.",
            "phase_3": "High-Performance Coaching: Olympic lifting / sport-specific conditioning, wearable biometric tracking (HRV/VO2 Max), and elite athlete mentoring."
        }
    },

    # 20. HEALTHCARE
    "Clinical Healthcare & Medical Professional": {
        "domain": "HEALTHCARE",
        "skills": ["Patient Care", "Clinical Diagnosis", "Medical Records (EMR/EHR)", "Healthcare Compliance (HIPAA)", "Pharmacology", "Vital Signs Monitoring", "Infection Control"],
        "project_keywords": ["patient management system", "clinical trial protocol", "health quality initiative", "medical emergency drill"],
        "education_keywords": ["medicine", "nursing", "pharmacy", "biomedical science", "public health"],
        "experience_keywords": ["nurse", "clinical practitioner", "medical officer", "physician assistant"],
        "roadmap": {
            "phase_1": "Medical Fundamentals: Human anatomy, pathophysiology, medical terminology, pharmacology, and BLS/ACLS certification.",
            "phase_2": "Clinical Care & EMR: Patient assessment protocols, EMR documentation (Epic/Cerner), medication administration, and infection control compliance.",
            "phase_3": "Advanced Clinical Leadership: Specialty clinical management, clinical research data collection, healthcare policy enforcement, and hospital unit leadership."
        }
    },

    # 21. HR
    "Human Resources & Talent Acquisition Specialist": {
        "domain": "HR",
        "skills": ["Talent Acquisition", "Recruitment", "Employee Relations", "Performance Management", "HRIS (Workday/BambooHR)", "Onboarding", "Labor Law", "Compensation & Benefits"],
        "project_keywords": ["recruitment campaign", "training program", "policy development", "retention strategy", "hris implementation"],
        "education_keywords": ["human resources", "organizational psychology", "business administration", "public administration"],
        "experience_keywords": ["hr specialist", "talent acquisition specialist", "recruiter", "hr manager", "people partner"],
        "roadmap": {
            "phase_1": "Talent Sourcing & Onboarding: Job description design, candidate sourcing (LinkedIn Recruiter/Boolean search), structured interviewing, and onboarding.",
            "phase_2": "Employee Relations & HRIS: Employment law compliance, performance review cycles, HRIS administration (Workday/BambooHR), and employee engagement surveys.",
            "phase_3": "Strategic People Leadership: Total rewards benchmarking, organizational design, succession planning, culture transformation, and SHRM-CP/SHRM-SCP certification."
        }
    },

    # 22. PUBLIC-RELATIONS
    "Public Relations & Media Communications Strategist": {
        "domain": "PUBLIC-RELATIONS",
        "skills": ["Public Relations", "Press Releases", "Crisis Communication", "Media Relations", "Corporate Communications", "Brand Reputation", "Event Planning", "Media Monitoring"],
        "project_keywords": ["pr campaign", "press conference", "crisis management plan", "media coverage report", "brand reputation recovery"],
        "education_keywords": ["public relations", "communications", "journalism", "mass media"],
        "experience_keywords": ["pr specialist", "communications officer", "media relations manager", "pr executive"],
        "roadmap": {
            "phase_1": "Media Writing & Pitching: Press release drafting (AP Style), media list building (Muck Rack/Cision), and media contact outreach.",
            "phase_2": "Campaigns & Reputation: Brand launch events, media interview prep for executives, influencer PR outreach, and sentiment tracking.",
            "phase_3": "Crisis Management & Strategy: High-stakes crisis communications protocols, corporate stakeholder alignment, brand narrative sovereignty, and PR agency leadership."
        }
    },

    # 23. SALES
    "Enterprise Sales & Account Specialist": {
        "domain": "SALES",
        "skills": ["B2B Sales", "Sales Pipeline Management", "CRM (Salesforce/HubSpot)", "Cold Outreach", "Account Management", "Contract Closing", "Negotiation", "Customer Retention"],
        "project_keywords": ["sales target achievement", "enterprise client acquisition", "crm pipeline overhaul", "account retention program"],
        "education_keywords": ["business administration", "marketing", "economics", "communications"],
        "experience_keywords": ["sales representative", "account manager", "sales executive", "inside sales specialist"],
        "roadmap": {
            "phase_1": "Outbound Prospecting: Cold calling, personalized cold email sequences, qualification frameworks (BANT/MEDDIC), and CRM logging.",
            "phase_2": "Discovery & Closing: Value-based demo presentations, overcoming enterprise objections, contract negotiation, and quota achievement.",
            "phase_3": "Key Account Management & Leadership: Large-scale enterprise renewals, cross-selling/upselling expansion, sales team coaching, and revenue leadership."
        }
    },

    # 24. TEACHER
    "Academic Educator & Curriculum Specialist": {
        "domain": "TEACHER",
        "skills": ["Curriculum Development", "Classroom Management", "Lesson Planning", "Educational Technology (LMS)", "Student Assessment", "Instructional Design", "Differentiated Instruction"],
        "project_keywords": ["curriculum redesign", "interactive learning module", "stem education program", "student evaluation framework"],
        "education_keywords": ["education", "pedagogy", "curriculum and instruction", "teaching"],
        "experience_keywords": ["teacher", "educator", "instructor", "lecturer", "instructional designer"],
        "roadmap": {
            "phase_1": "Pedagogy & Classroom Basics: Lesson planning (Bloom's Taxonomy), classroom management, formative/summative assessments, and teaching license credentials.",
            "phase_2": "EdTech & Interactive Learning: Learning Management Systems (Canvas/Google Classroom), interactive STEM tools, and differentiated learning for diverse needs.",
            "phase_3": "Curriculum Leadership: School curriculum standards alignment, teacher mentoring, instructional design evaluation, and academic department leadership."
        }
    }
}

CATEGORY_METADATA = {
    "ACCOUNTANT": {"name": "Accounting & Auditing", "icon": "Calculator", "focus": "Financial reporting, GAAP compliance, taxation, and auditing."},
    "ADVOCATE": {"name": "Legal & Advocacy", "icon": "Scale", "focus": "Corporate law, litigation, contract management, and compliance."},
    "AGRICULTURE": {"name": "Agriculture & AgTech", "icon": "Sprout", "focus": "Agronomy, precision farming, crop management, and agribusiness."},
    "APPAREL": {"name": "Fashion & Apparel", "icon": "Scissors", "focus": "Apparel design, tech pack production, textiles, and quality control."},
    "ARTS": {"name": "Creative & Fine Arts", "icon": "Palette", "focus": "Visual arts, illustration, concept art, and creative direction."},
    "AUTOMOBILE": {"name": "Automotive Engineering", "icon": "Car", "focus": "Vehicle engineering, diagnostics, EV technology, and powertrain."},
    "AVIATION": {"name": "Aviation & Aerospace", "icon": "Plane", "focus": "Flight operations, aerospace maintenance, avionics, and safety."},
    "BANKING": {"name": "Banking & Financial Services", "icon": "Landmark", "focus": "Commercial banking, credit analysis, loan underwriting, and wealth."},
    "BPO": {"name": "BPO & Customer Operations", "icon": "Headphones", "focus": "Customer experience, SLA compliance, workforce management, and CRM."},
    "BUSINESS-DEVELOPMENT": {"name": "Business Development", "icon": "TrendingUp", "focus": "B2B growth, strategic partnerships, and client acquisition."},
    "CHEF": {"name": "Culinary Arts & Hospitality", "icon": "Utensils", "focus": "Menu engineering, kitchen operations, HACCP food safety, and fine dining."},
    "CONSTRUCTION": {"name": "Construction & Structural", "icon": "HardHat", "focus": "Project management, civil engineering, site safety, and BOQ."},
    "CONSULTANT": {"name": "Management Consulting", "icon": "Briefcase", "focus": "Strategic planning, operational transformation, and business cases."},
    "DESIGNER": {"name": "UI/UX & Product Design", "icon": "Layout", "focus": "User interface, UX research, prototyping, and design systems."},
    "DIGITAL-MEDIA": {"name": "Digital Media & Marketing", "icon": "Video", "focus": "Content creation, SEO, social media, and digital campaigns."},
    "ENGINEERING": {"name": "Engineering & Technology", "icon": "Cpu", "focus": "Mechanical, civil, electrical, and multidisciplinary engineering."},
    "FINANCE": {"name": "Finance & Investment", "icon": "DollarSign", "focus": "Financial modeling, DCF valuation, portfolio strategy, and risk."},
    "FITNESS": {"name": "Fitness & Sports Science", "icon": "Dumbbell", "focus": "Strength conditioning, personal training, and sports nutrition."},
    "HEALTHCARE": {"name": "Healthcare & Medicine", "icon": "HeartPulse", "focus": "Clinical care, patient diagnosis, EMR systems, and pharmacology."},
    "HR": {"name": "Human Resources & Talent", "icon": "Users", "focus": "Talent acquisition, employee relations, HRIS, and people strategy."},
    "INFORMATION-TECHNOLOGY": {"name": "Information Technology", "icon": "Terminal", "focus": "Software engineering, ML/AI, cloud/DevOps, and cybersecurity."},
    "PUBLIC-RELATIONS": {"name": "Public Relations & Media", "icon": "Megaphone", "focus": "Media relations, crisis communication, and corporate messaging."},
    "SALES": {"name": "Enterprise Sales & Accounts", "icon": "ShoppingBag", "focus": "B2B sales execution, account management, and pipeline closing."},
    "TEACHER": {"name": "Education & Teaching", "icon": "GraduationCap", "focus": "Pedagogy, curriculum development, classroom instruction, and EdTech."}
}

def get_career_profile(career_name: str) -> dict:
    """Retrieve full taxonomy profile for a specific career."""
    return CAREER_TAXONOMY.get(career_name, None)

def get_career_roadmap(career_name: str) -> dict:
    """Retrieve the 3-phase structured learning roadmap for a specific career."""
    profile = CAREER_TAXONOMY.get(career_name)
    if profile and "roadmap" in profile:
        return profile["roadmap"]
    return {
        "phase_1": "Foundational Mastery: Learn essential core competencies, tools, and industry standards.",
        "phase_2": "Applied Practice & Projects: Build real-world portfolio deliverables and obtain relevant credentials.",
        "phase_3": "Advanced Specialization: Master complex workflows, architecture, and team leadership."
    }

def get_all_categories() -> list:
    """Returns list of all 24 canonical dataset categories."""
    return sorted(list(CATEGORY_METADATA.keys()))
