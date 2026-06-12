import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pdfplumber
from fpdf import FPDF
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page Settings
st.set_page_config(
    page_title="AI Powered Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("AI Powered Resume Analyzer")
st.write("Analyze Resume | ATS Score | Job Match")

# Upload Resume
resume_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

# Job Description Input
job_des = st.text_area("Paste Job Description Here")

# Main logic
resume_text = ""
if resume_file:
    with pdfplumber.open(resume_file) as pdf:
        resume_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                resume_text += text
    st.success("Resume uploaded Successfully")

# Skills List
skills = [
    "python",
    "java",
    "sql",
    "html",
    "javascript",
    "css",
    "react",
    "machine learning",
    "excel",
    "power bi",
    "django",
    "c++"
]

# Find skills
found_skills = []
for skill in skills:
    if skill in resume_text.lower():
        found_skills.append(skill)

# Show skills
st.subheader("⚔ Skills found")
st.write(found_skills)

# ATS Score
ats_score = len(found_skills) * 10
if ats_score > 100:
    ats_score = 100

st.subheader("📊 ATS Score")
st.progress(ats_score / 100)
st.write(f"{ats_score}%")

# Pie chart
fig, ax = plt.subplots()

labels = [
    "Skills found",
    "Missing"
]
sizes = [
    len(found_skills),
    10 - len(found_skills)
]

ax.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%"
)
st.pyplot(fig)

# Resume Suggestions
st.subheader("Resume Suggestions")
if ats_score < 50:
    st.error("Your resume is weak. Add more technical skills and project")
elif ats_score < 80:
    st.warning("Your resume is good but add more technical skills as per the job requirements")
else:
    st.success("Excellent Resume for ATS!")

# Resume Improvement Advisor
st.subheader("🚀 Resume Improvement Advisor")
improvements = []

# Check projects
if "project" not in resume_text.lower():
    improvements.append("Add 2 strong projects in your resume")

# Check skills
if len(found_skills) < 4:
    improvements.append("Add more technical skills like Python, SQL, Excel")

# Check internships
if ("internship" not in resume_text.lower() and "experience" not in resume_text.lower()):
    improvements.append("Add internship or practical experience")

# Check Github
if "GitHub" not in resume_text.lower():
    improvements.append("Add Github Repo")

# Show Improvements Tips
if improvements:
    st.warning("Ways to Improve Resume")
    for tip in improvements:
        st.write(f"✔ {tip}")
else:
    st.success("Excellent Resume! No Major improvements are required😎")

# Resume VS Job Description
if job_des:
    text = [
        resume_text,
        job_des
    ]
    cv = CountVectorizer()
    matrix = cv.fit_transform(text)
    similarity = cosine_similarity(matrix)[0][1]
    
    st.subheader("🎯 Resume Match Score")
    st.write(f"{round(similarity * 100, 2)}%")

    # Missing Skills
    missing_skills = []
    for skill in skills:
        if (skill in job_des.lower() and skill not in resume_text.lower()):
            missing_skills.append(skill)

    st.subheader("🚨 Missing Skills")
    st.write(missing_skills)

# Interview Questions
st.subheader("Interview Questions")
if "python" in found_skills:
    st.write(". What is OOPS in Python?")
    st.write(". What is the difference between Python and Java?")

if "sql" in found_skills:
    st.write(". Difference between HAVING AND WHERE clause?")
    st.write(". What is JOINS in SQL?")

if "java" in found_skills:
    st.write(". What is Inheritance?")

# Career roadmap
st.subheader("Career Roadmap")
role = st.selectbox("Choose Career Role", [
    "Python Developer",
    "Data Analyst"
])

if role == "Python Developer":
    st.info("Roadmap: Python -> OOP -> SQL -> Django -> Projects")
elif role == "Data Analyst":
    st.info("Roadmap: Excel -> SQL -> Python -> PowerBI")

# PDF Report
st.subheader("📄 Download Report")
if st.button("Generate PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resume Analysis Report", ln=True)
    pdf.cell(200, 10, txt=f"ATS Score: {ats_score}", ln=True)
    pdf.cell(200, 10, txt=f"Skills: {','.join(found_skills)}", ln=True)
    
    st.write("ATS SCORE:", ats_score)
    st.write("SKILLS:", found_skills)
    
    pdf.output("Resume_Report.pdf")
    st.success("PDF Generated Successfully")
