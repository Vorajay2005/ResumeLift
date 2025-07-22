import json
from http.server import BaseHTTPRequestHandler
import openai
import os
from docx import Document
import fitz  # PyMuPDF
import io
import urllib.parse
from PIL import Image

# Note: pytesseract requires system tesseract installation which isn't available in Vercel
# We'll skip OCR for Vercel deployment to keep it simple

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

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Handle CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        try:
            # Get content length and read the request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            
            # Parse multipart form data (simplified for this case)
            content_type = self.headers.get('Content-Type', '')
            
            if 'multipart/form-data' in content_type:
                # Extract boundary
                boundary = content_type.split('boundary=')[1]
                parts = body.split(f'--{boundary}'.encode())
                
                file_content = None
                job_description = None
                filename = None
                
                for part in parts:
                    if b'Content-Disposition' in part:
                        if b'name="file"' in part:
                            # Extract file content
                            file_start = part.find(b'\r\n\r\n') + 4
                            file_content = part[file_start:].rstrip(b'\r\n')
                            
                            # Extract filename
                            disp_line = part.split(b'\r\n')[1].decode()
                            if 'filename=' in disp_line:
                                filename = disp_line.split('filename="')[1].split('"')[0]
                                
                        elif b'name="job_description"' in part:
                            # Extract job description
                            desc_start = part.find(b'\r\n\r\n') + 4
                            job_description = part[desc_start:].rstrip(b'\r\n').decode()
                
                if not file_content or not job_description:
                    self.wfile.write(json.dumps({"error": "Missing file or job description"}).encode())
                    return
                
                # Process the file based on extension
                filename_lower = filename.lower() if filename else ""
                
                if filename_lower.endswith(".txt"):
                    resume_text = file_content.decode('utf-8', errors='ignore')
                elif filename_lower.endswith(".pdf"):
                    resume_text = extract_text_from_pdf(file_content)
                elif filename_lower.endswith((".docx", ".doc")):
                    resume_text = extract_text_from_docx(file_content)
                else:
                    self.wfile.write(json.dumps({"error": "Unsupported file type. Please upload a .txt, .pdf, .docx, or .doc file."}).encode())
                    return
                
                # Call OpenAI API
                client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                
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
                result = {"result": result_text}
                
                self.wfile.write(json.dumps(result).encode())
            else:
                self.wfile.write(json.dumps({"error": "Content-Type must be multipart/form-data"}).encode())
                
        except Exception as e:
            error_result = {"error": str(e)}
            self.wfile.write(json.dumps(error_result).encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
    def do_GET(self):
        # Health check endpoint
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "ResumeCopilot Backend is running!"}).encode())