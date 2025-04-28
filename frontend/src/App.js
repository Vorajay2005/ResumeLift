import React, { useState, useRef } from "react";
import axios from "axios";

export default function App() {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("No file chosen");
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [uploadError, setUploadError] = useState("");
  const [copySuccess, setCopySuccess] = useState("");
  const [saveSuccess, setSaveSuccess] = useState("");

  // Color palette
  const colors = {
    primary: "#3498db",
    secondary: "#2ecc71",
    accent: "#f39c12",
    light: "#ecf0f1",
    dark: "#34495e",
    error: "#e74c3c",
    text: "#2c3e50",
    gradient1: "#4e54c8",
    gradient2: "#8f94fb",
    gradientLight1: "#f6f9fc",
    gradientLight2: "#eef2f7",
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
      setUploadError("");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadError("Please upload a resume file");
      return;
    }

    if (!jobDescription.trim()) {
      setUploadError("Please paste a job description");
      return;
    }

    setUploadError("");
    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDescription);

    try {
      setLoading(true);
      setSuccess(false);
      const response = await axios.post(
        "http://127.0.0.1:8000/analyze_resume/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setResult(response.data.result);
      setSuccess(true);
    } catch (error) {
      console.error(error);
      setUploadError("Error processing your resume. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Copy to Clipboard function
  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(result);
      setCopySuccess("Copied!");

      // Reset copy success message after 2 seconds
      setTimeout(() => {
        setCopySuccess("");
      }, 2000);
    } catch (err) {
      setCopySuccess("Failed to copy");
      console.error("Failed to copy text: ", err);
    }
  };

  // Save Report function
  const saveReport = () => {
    try {
      // Create a blob with the result text
      const blob = new Blob([result], { type: "text/plain" });

      // Create a link element
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);

      // Set the file name with date stamp
      const date = new Date();
      const dateString = `${date.getFullYear()}-${(date.getMonth() + 1)
        .toString()
        .padStart(2, "0")}-${date.getDate().toString().padStart(2, "0")}`;
      a.download = `resume-analysis-${dateString}.txt`;

      // Append to the DOM, click, and remove
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      setSaveSuccess("Saved!");

      // Reset save success message after 2 seconds
      setTimeout(() => {
        setSaveSuccess("");
      }, 2000);
    } catch (err) {
      setSaveSuccess("Failed to save");
      console.error("Failed to save file: ", err);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: `linear-gradient(135deg, ${colors.gradientLight1} 0%, ${colors.gradientLight2} 100%)`,
        padding: "40px 20px",
        fontFamily: "'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Background decorative elements */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "10px",
          background: `linear-gradient(90deg, ${colors.primary} 0%, ${colors.secondary} 100%)`,
          zIndex: 1,
        }}
      ></div>

      <div
        style={{
          position: "absolute",
          top: "15%",
          right: "-150px",
          width: "300px",
          height: "300px",
          borderRadius: "50%",
          background: `radial-gradient(circle, rgba(52,152,219,0.1) 0%, rgba(52,152,219,0) 70%)`,
          zIndex: 0,
        }}
      ></div>

      <div
        style={{
          position: "absolute",
          bottom: "10%",
          left: "-100px",
          width: "200px",
          height: "200px",
          borderRadius: "50%",
          background: `radial-gradient(circle, rgba(46,204,113,0.1) 0%, rgba(46,204,113,0) 70%)`,
          zIndex: 0,
        }}
      ></div>

      <div
        className="app-container"
        style={{
          maxWidth: "1000px",
          margin: "0 auto",
          padding: "40px",
          backgroundColor: "#fff",
          borderRadius: "12px",
          boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
          position: "relative",
          zIndex: 2,
        }}
      >
        <div
          style={{
            textAlign: "center",
            marginBottom: "40px",
            position: "relative",
          }}
        >
          <h1
            style={{
              fontSize: "42px",
              fontWeight: "700",
              color: colors.dark,
              margin: "0 0 16px 0",
            }}
          >
            ResumeLift<span style={{ color: colors.primary }}>.</span>
          </h1>
          <p
            style={{
              fontSize: "18px",
              color: "#7f8c8d",
              maxWidth: "600px",
              margin: "0 auto",
            }}
          >
            AI-powered resume analyzer that helps you match job descriptions and
            improve your chances
          </p>
        </div>

        <div
          style={{
            display: "flex",
            flexDirection: "row",
            gap: "30px",
            flexWrap: "wrap",
          }}
        >
          {/* Left column - Inputs */}
          <div style={{ flex: "1", minWidth: "300px" }}>
            <div className="upload-section" style={{ marginBottom: "30px" }}>
              <h3
                style={{
                  fontSize: "20px",
                  fontWeight: "600",
                  marginBottom: "12px",
                  color: colors.dark,
                  display: "flex",
                  alignItems: "center",
                }}
              >
                <span
                  style={{
                    display: "inline-block",
                    width: "24px",
                    height: "24px",
                    borderRadius: "50%",
                    background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.primary}dd 100%)`,
                    color: "white",
                    textAlign: "center",
                    lineHeight: "24px",
                    fontSize: "14px",
                    marginRight: "8px",
                  }}
                >
                  1
                </span>
                Upload Your Resume
              </h3>
              <div
                style={{
                  border: `2px dashed ${colors.primary}`,
                  borderRadius: "8px",
                  padding: "25px",
                  textAlign: "center",
                  backgroundColor: "#f9fcff",
                  transition: "all 0.3s ease",
                  boxShadow: "0 4px 6px rgba(52,152,219,0.1)",
                }}
              >
                <p style={{ marginBottom: "12px", fontSize: "14px" }}>
                  Supported formats: PDF, DOC, DOCX, TXT, PNG, JPG, JPEG
                </p>
                <label
                  htmlFor="resume-upload"
                  style={{
                    display: "inline-block",
                    padding: "12px 24px",
                    background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.primary}dd 100%)`,
                    color: "white",
                    borderRadius: "6px",
                    cursor: "pointer",
                    fontWeight: "600",
                    transition: "all 0.2s ease",
                    boxShadow: "0 4px 6px rgba(52,152,219,0.25)",
                  }}
                >
                  Choose File
                </label>
                <input
                  type="file"
                  id="resume-upload"
                  onChange={handleFileChange}
                  style={{ display: "none" }}
                  accept=".pdf,.doc,.docx,.txt,.png,.jpg,.jpeg"
                />
                <p
                  style={{
                    marginTop: "12px",
                    fontSize: "14px",
                    color:
                      fileName === "No file chosen" ? "#95a5a6" : colors.dark,
                  }}
                >
                  {fileName}
                </p>
              </div>
            </div>

            <div className="job-description-section">
              <h3
                style={{
                  fontSize: "20px",
                  fontWeight: "600",
                  marginBottom: "12px",
                  color: colors.dark,
                  display: "flex",
                  alignItems: "center",
                }}
              >
                <span
                  style={{
                    display: "inline-block",
                    width: "24px",
                    height: "24px",
                    borderRadius: "50%",
                    background: `linear-gradient(135deg, ${colors.accent} 0%, ${colors.accent}dd 100%)`,
                    color: "white",
                    textAlign: "center",
                    lineHeight: "24px",
                    fontSize: "14px",
                    marginRight: "8px",
                  }}
                >
                  2
                </span>
                Paste Job Description
              </h3>
              <div
                style={{
                  borderRadius: "8px",
                  overflow: "hidden",
                  boxShadow: "0 4px 6px rgba(0,0,0,0.05)",
                }}
              >
                <textarea
                  rows="12"
                  placeholder="Paste the job description you want to match..."
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  style={{
                    width: "100%",
                    padding: "16px",
                    fontSize: "15px",
                    border: "1px solid #e0e0e0",
                    borderRadius: "8px",
                    resize: "vertical",
                    fontFamily: "inherit",
                    backgroundColor: "#fff",
                    transition: "border 0.3s ease",
                    outline: "none",
                    boxSizing: "border-box",
                  }}
                />
              </div>
            </div>

            {uploadError && (
              <div
                style={{
                  color: colors.error,
                  padding: "12px 16px",
                  fontSize: "14px",
                  backgroundColor: "#fdf5f5",
                  borderRadius: "6px",
                  marginTop: "16px",
                  border: `1px solid ${colors.error}88`,
                }}
              >
                <strong>Error:</strong> {uploadError}
              </div>
            )}

            <div style={{ marginTop: "25px" }}>
              <button
                onClick={handleUpload}
                disabled={loading}
                style={{
                  padding: "14px 24px",
                  fontSize: "16px",
                  fontWeight: "600",
                  cursor: loading ? "not-allowed" : "pointer",
                  background: loading
                    ? "#95a5a6"
                    : `linear-gradient(135deg, ${colors.secondary} 0%, ${colors.secondary}dd 100%)`,
                  color: "white",
                  border: "none",
                  borderRadius: "8px",
                  transition: "all 0.3s ease",
                  width: "100%",
                  boxShadow: loading
                    ? "none"
                    : "0 4px 10px rgba(46,204,113,0.3)",
                }}
              >
                {loading ? "Analyzing..." : "Analyze Resume"}
              </button>
            </div>
          </div>

          {/* Right column - Results */}
          <div style={{ flex: "1", minWidth: "300px" }}>
            <div
              className="results-section"
              style={{
                backgroundColor: success ? "#f7fcf9" : "#f8f9fa",
                borderRadius: "12px",
                padding: "25px",
                height: "100%",
                boxSizing: "border-box",
                border: success
                  ? `1px solid ${colors.secondary}`
                  : "1px solid #e0e0e0",
                transition: "all 0.3s ease",
                boxShadow: "0 4px 6px rgba(0,0,0,0.05)",
              }}
            >
              <h3
                style={{
                  fontSize: "20px",
                  fontWeight: "600",
                  color: colors.dark,
                  marginTop: "0",
                  marginBottom: "20px",
                  display: "flex",
                  alignItems: "center",
                }}
              >
                <span
                  style={{
                    display: "inline-block",
                    width: "24px",
                    height: "24px",
                    borderRadius: "50%",
                    background: `linear-gradient(135deg, ${colors.secondary} 0%, ${colors.secondary}dd 100%)`,
                    color: "white",
                    textAlign: "center",
                    lineHeight: "24px",
                    fontSize: "14px",
                    marginRight: "8px",
                  }}
                >
                  3
                </span>
                Analysis Results
              </h3>

              {!success && !loading && (
                <div
                  style={{
                    textAlign: "center",
                    padding: "50px 0",
                    color: "#95a5a6",
                  }}
                >
                  <div
                    style={{
                      width: "80px",
                      height: "80px",
                      margin: "0 auto 20px",
                      borderRadius: "50%",
                      background: "#f0f0f0",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: "30px",
                    }}
                  >
                    📄
                  </div>
                  <p style={{ fontSize: "16px" }}>
                    Upload your resume and paste a job description to get
                    started
                  </p>
                </div>
              )}

              {loading && (
                <div style={{ textAlign: "center", padding: "50px 0" }}>
                  <div
                    style={{
                      width: "60px",
                      height: "60px",
                      margin: "0 auto 20px",
                      border: `4px solid ${colors.primary}20`,
                      borderTop: `4px solid ${colors.primary}`,
                      borderRadius: "50%",
                      animation: "spin 1s linear infinite",
                    }}
                  ></div>
                  <style>
                    {`
                      @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                      }
                    `}
                  </style>
                  <div style={{ color: colors.primary, fontSize: "16px" }}>
                    Analyzing your resume against the job description...
                  </div>
                </div>
              )}

              {success && (
                <div className="result-content">
                  <div
                    style={{
                      padding: "20px",
                      backgroundColor: "#fff",
                      borderRadius: "8px",
                      border: "1px solid #e0e0e0",
                      fontSize: "15px",
                      lineHeight: "1.6",
                      whiteSpace: "pre-wrap",
                      boxShadow: "0 2px 4px rgba(0,0,0,0.03)",
                    }}
                  >
                    {result}
                  </div>

                  <div
                    style={{
                      marginTop: "20px",
                      textAlign: "center",
                      display: "flex",
                      justifyContent: "center",
                      gap: "10px",
                    }}
                  >
                    <button
                      onClick={saveReport}
                      style={{
                        padding: "8px 16px",
                        background: "#f0f0f0",
                        border: "none",
                        borderRadius: "4px",
                        fontSize: "14px",
                        cursor: "pointer",
                        position: "relative",
                        transition: "all 0.2s ease",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }}
                    >
                      {saveSuccess ? saveSuccess : "Save Report"}
                      {saveSuccess && (
                        <span
                          style={{ marginLeft: "5px", color: colors.secondary }}
                        >
                          ✓
                        </span>
                      )}
                    </button>
                    <button
                      onClick={copyToClipboard}
                      style={{
                        padding: "8px 16px",
                        background: "#f0f0f0",
                        border: "none",
                        borderRadius: "4px",
                        fontSize: "14px",
                        cursor: "pointer",
                        position: "relative",
                        transition: "all 0.2s ease",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }}
                    >
                      {copySuccess ? copySuccess : "Copy to Clipboard"}
                      {copySuccess && (
                        <span
                          style={{ marginLeft: "5px", color: colors.secondary }}
                        >
                          ✓
                        </span>
                      )}
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        <div
          style={{
            marginTop: "50px",
            textAlign: "center",
            borderTop: "1px solid #eee",
            paddingTop: "20px",
            color: "#95a5a6",
            fontSize: "14px",
          }}
        >
          <p>ResumeLift • Elevate your resume, Accelerate your career </p>
        </div>
      </div>
    </div>
  );
}
