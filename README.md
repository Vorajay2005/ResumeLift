# ResumeLift 🚀

An AI-powered resume analyzer that helps you optimize your resume for specific job descriptions using OpenAI's GPT technology.

![ResumeLift](https://img.shields.io/badge/ResumeLift-AI%20Resume%20Analyzer-blue)
![React](https://img.shields.io/badge/React-19.1.0-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?logo=fastapi)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-412991?logo=openai)

## ✨ Features

- **Multi-format Resume Support**: Upload PDF, DOC, DOCX, TXT, PNG, JPG, or JPEG files
- **AI-Powered Analysis**: Uses OpenAI GPT-3.5-turbo for intelligent resume evaluation
- **Job Matching**: Compare your resume against specific job descriptions
- **Smart Scoring**: Get a match score out of 100
- **Actionable Suggestions**: Receive specific, implementable improvement recommendations
- **OCR Support**: Extract text from image-based resumes
- **Export Options**: Copy results to clipboard or save as text file
- **Modern UI**: Clean, professional interface with responsive design

## 🛠️ Tech Stack

### Frontend

- **React 19.1.0** - Modern React with latest features
- **Axios** - HTTP client for API requests
- **CSS3** - Custom styling with gradients and animations

### Backend

- **FastAPI** - High-performance Python web framework
- **OpenAI API** - GPT-3.5-turbo for resume analysis
- **PyMuPDF** - PDF text extraction
- **python-docx** - Word document processing
- **Pytesseract** - OCR for image text extraction
- **Pillow** - Image processing
- **Uvicorn** - ASGI server

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v14 or higher)
- **Python 3.8+**
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd ResumeLift
   ```

2. **Set up the Backend**

   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**

   ```bash
   # Create .env file in backend directory
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

4. **Set up the Frontend**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. **Start the Backend** (Terminal 1)

   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the Frontend** (Terminal 2)

   ```bash
   cd frontend
   npm start
   ```

3. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📖 Usage

1. **Upload Resume**: Choose your resume file (multiple formats supported)
2. **Paste Job Description**: Copy and paste the job description you're targeting
3. **Analyze**: Click "Analyze Resume" to get AI-powered feedback
4. **Review Results**: Get your match score and detailed suggestions
5. **Export**: Copy results or save as a text file

## 🔧 Configuration

### Backend Configuration

The backend uses environment variables for configuration:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Frontend Configuration

To change the backend URL, modify the fetch URL in `frontend/src/App.js`:

```javascript
const response = await fetch("http://localhost:8000/analyze_resume/", {
  method: "POST",
  body: formData,
});
```

## 📁 Project Structure

```
ResumeLift/
├── backend/
│   ├── app/
│   │   └── main.py          # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── .env                # Environment variables
│   └── venv/               # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── App.css         # Styling
│   │   └── index.js        # Entry point
│   ├── public/
│   ├── package.json        # Node.js dependencies
│   └── README.md           # Create React App docs
└── README.md               # This file
```

## 🔍 API Endpoints

### POST `/analyze_resume/`

Analyzes a resume against a job description.

**Parameters:**

- `file`: Resume file (multipart/form-data)
- `job_description`: Job description text (form field)

**Response:**

```json
{
  "result": "Match Score: 85/100\n\nSuggestions:\n- Add specific technologies mentioned in job description\n- Include quantifiable achievements\n- ..."
}
```

## 🛡️ Security Notes

- Keep your OpenAI API key secure and never commit it to version control
- The `.env` file is gitignored by default
- Consider using environment-specific configurations for production

## 🚀 Deployment

### Backend Deployment

- Can be deployed to platforms like Heroku, Railway, or Render
- Ensure environment variables are set in your deployment platform
- Use `uvicorn app.main:app --host 0.0.0.0 --port $PORT` for production

### Frontend Deployment

- Build the production version: `npm run build`
- Deploy to platforms like Netlify, Vercel, or GitHub Pages
- Update the API URL to point to your deployed backend

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- FastAPI team for the excellent web framework
- React team for the frontend library
- All the open-source libraries that make this project possible

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

---

**Made with ❤️ for job seekers everywhere**
