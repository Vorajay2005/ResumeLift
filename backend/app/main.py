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

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup OpenAI client correctly
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
async def root():
    return {"message": "ResumeLift Backend is running!"}

# Helper functions
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

        # New smarter prompt
        prompt = f"""
You are an expert resume coach and ATS (Applicant Tracking System) analyzer.

Review the resume text and the job description.

**Return output ONLY in this strict format:**

Match Score: (number)/100

Suggestions:
- (suggestion 1)
- (suggestion 2)
- (suggestion 3)

Only suggest things realistically missing. Be practical and specific.

Resume:
{resume_text}

Job Description:
{job_description}
        """

        # Ask OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        # Correct way to extract result
        result_text = response.choices[0].message.content

        return {"result": result_text}

    except Exception as e:
        return {"error": str(e)}

