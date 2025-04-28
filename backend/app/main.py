from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from dotenv import load_dotenv
from docx import Document
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# Load environment variables
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
async def root():
    return {"message": "ResumeCopilot Backend is running!"}

def extract_text_from_pdf(file_bytes):
    text = ""
    pdf_file = fitz.open(stream=file_bytes, filetype="pdf")
    for page in pdf_file:
        text += page.get_text()
    return text

def extract_text_from_docx(file_bytes):
    text = ""
    document = Document(io.BytesIO(file_bytes))
    for para in document.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_image(file_bytes):
    image = Image.open(io.BytesIO(file_bytes))
    text = pytesseract.image_to_string(image)
    return text

@app.post("/analyze_resume/")
async def analyze_resume(file: UploadFile, job_description: str = Form(...)):
    try:
        file_bytes = await file.read()
        filename = file.filename.lower()

        if filename.endswith(".txt"):
            resume_text = file_bytes.decode('utf-8', errors='ignore')
        elif filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(file_bytes)
        elif filename.endswith(".docx") or filename.endswith(".doc"):
            resume_text = extract_text_from_docx(file_bytes)
        elif filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            resume_text = extract_text_from_image(file_bytes)
        else:
            return {"error": "Unsupported file type. Please upload a .txt, .pdf, .docx, .doc, .jpg, or .png file."}

        # 🚀 ULTRA-FINAL SMARTER PROMPT
        prompt = f"""
You are an expert resume coach and ATS (Applicant Tracking System) analyzer.

Your goal is to help improve resumes realistically based on true gaps compared to a job description.

**Your task:**
- Review whether important sections exist and if they are strong: Skills, Experience, Projects, Certifications, Education.
- ONLY suggest adding a new section if it is completely missing.
- If a section like "Projects" already exists but lacks relevant personal projects, mobile app projects, or significant examples, suggest adding new content inside that existing section, NOT creating a new section.
- If Certifications are missing and relevant certifications could exist, suggest creating that section.
- Suggest adding missing technologies, important keywords, or missing quantifiable impacts in appropriate sections.
- Always use very specific, actionable advice. No vague or template suggestions.
- Format Suggestions as clear bullet points.

Here is the resume:
{resume_text}

Here is the job description:
{job_description}

**Output format:**

Match Score: __/100

Suggestions:
- [specific suggestion 1]
- [specific suggestion 2]
- [specific suggestion 3]
- [etc.]

If the resume is already strong, suggest only minor improvements (e.g., formatting polish, better bullet points, stronger action verbs, quantified metrics).
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        result_text = response.choices[0].message.content
        return {"result": result_text}

    except Exception as e:
        return {"error": str(e)}
