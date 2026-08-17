import sys
import os
import json
from fpdf import FPDF

# Create a sample PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="John Doe", ln=1, align='C')
pdf.cell(200, 10, txt="SKILLS", ln=1)
pdf.cell(200, 10, txt="Python, SQL, Java, React, Next.js", ln=1)
pdf.cell(200, 10, txt="EXPERIENCE", ln=1)
pdf.cell(200, 10, txt="Software Engineer at Google", ln=1)
pdf.cell(200, 10, txt="Developed APIs.", ln=1)
pdf.cell(200, 10, txt="PROJECTS", ln=1)
pdf.cell(200, 10, txt="CareerLens AI", ln=1)
pdf.cell(200, 10, txt="Built an AI resume parser.", ln=1)
pdf.cell(200, 10, txt="EDUCATION", ln=1)
pdf.cell(200, 10, txt="Bachelor of Computer Science from MIT", ln=1)
pdf.cell(200, 10, txt="CERTIFICATIONS", ln=1)
pdf.cell(200, 10, txt="AWS Certified Solutions Architect", ln=1)
pdf.output("dummy_resume.pdf")

sys.path.append('lib')
from resume import extract_resume

profile = extract_resume("dummy_resume.pdf")
print(json.dumps(profile, indent=2))
