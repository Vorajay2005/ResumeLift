from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from dotenv import load_dotenv
from docx import Document
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    logger.error("OPENAI_API_KEY not found in environment variables!")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
try:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    logger.error(f"Error initializing OpenAI client: {str(e)}")
    client = None


@app.get("/")
async def root():
    """Health check endpoint"""
    # Check if OpenAI client is initialized
    if not client:
        return {"status": "warning", "message": "ResumeCopilot Backend is running but OpenAI client is not initialized!"}
    return {"status": "success", "message": "ResumeCopilot Backend is running!"}


def extract_text_from_pdf(file_bytes):
    """Extract text from PDF file"""
    try:
        text = ""
        pdf_file = fitz.open(stream=file_bytes, filetype="pdf")
        for page in pdf_file:
            text += page.get_text()
        logger.info(f"Successfully extracted {len(text)} characters from PDF")
        return text
    except Exception as e:
        logger.error(f"PDF extraction error: {str(e)}")
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def extract_text_from_docx(file_bytes):
    """Extract text from DOCX file"""
    try:
        text = ""
        document = Document(io.BytesIO(file_bytes))
        for para in document.paragraphs:
            text += para.text + "\n"
        logger.info(f"Successfully extracted {len(text)} characters from DOCX")
        return text
    except Exception as e:
        logger.error(f"DOCX extraction error: {str(e)}")
        raise Exception(f"Failed to extract text from DOCX: {str(e)}")


def extract_text_from_image(file_bytes):
    """Extract text from image file using OCR"""
    try:
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image)
        logger.info(f"Successfully extracted {len(text)} characters using OCR")
        return text
    except Exception as e:
        logger.error(f"Image extraction error: {str(e)}")
        raise Exception(f"Failed to extract text from image: {str(e)}")


@app.post("/analyze_resume/")
async def analyze_resume(file: UploadFile, job_description: str = Form(...)):
    """Analyze a resume against a job description"""
    try:
        if not client:
            raise HTTPException(status_code=500, detail="OpenAI client not initialized. Check API key.")
        
        logger.info(f"Received file: {file.filename}, content_type: {file.content_type}")
        logger.info(f"Job description length: {len(job_description)} characters")
        
        # Read file content
        file_bytes = await file.read()
        logger.info(f"File size: {len(file_bytes)} bytes")
        
        if len(file_bytes) == 0:
            raise HTTPException(status_code=400, detail="File is empty")
            
        # Extract text based on file type
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
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file type. Please upload a .txt, .pdf, .docx, .doc, .jpg, or .png file."
            )
        
        if not resume_text or len(resume_text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Could not extract meaningful text from the file")
            
        logger.info(f"Successfully extracted {len(resume_text)} characters from resume")
        
        # Prepare prompt for OpenAI
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
        
        # Call OpenAI API
        try:
            logger.info("Sending request to OpenAI...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            result_text = response.choices[0].message.content
            logger.info(f"Received response from OpenAI: {len(result_text)} characters")
            
            return {"result": result_text}
            
        except Exception as openai_error:
            logger.error(f"OpenAI API error: {openai_error}")
            raise HTTPException(status_code=500, detail=f"Error from OpenAI API: {str(openai_error)}")
            
    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise he
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}\n{traceback.format_
