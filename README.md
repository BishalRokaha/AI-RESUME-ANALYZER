# 📝 AI Resume Analyzer

A powerful AI-powered Streamlit web application that analyzes your resume against a given job description. It evaluates alignment using **BERT-based similarity** and generates an **LLM-driven analysis report** to help you improve your chances of getting shortlisted.

---

## 🔍 Features

- 📄 Extracts content from PDF resumes
- 🧠 Computes semantic similarity between resume and job description using **BERT (SBERT - all-mpnet-base-v2)**
- 🤖 Generates intelligent analysis reports using **Groq’s LLaMA 3.3 70B Versatile Model**
- 📊 Scores each relevant point (skills, experience, etc.) from 0 to 5
- ✅ Marks aligned points, ❌ mismatches, ⚠️ ambiguous points with reasons
- 📈 Provides ATS similarity score and overall AI evaluation
- 💾 Option to download the generated report

---

## 🚀 Tech Stack

| Tech              | Usage                          |
|------------------|---------------------------------|
| **Python**       | Core application logic          |
| **Streamlit**    | Web UI                          |
| **PDFMiner**     | Extract text from PDF resumes   |
| **SentenceTransformers** | BERT embeddings for similarity |
| **scikit-learn** | Cosine similarity computation   |
| **Groq API**     | Generate LLM-based analysis     |
| **dotenv**       | Manage API key securely         |

---

## 🛠️ Installation & Setup

### 1️⃣ **Clone the Repository**

```bash
git clone https://github.com/BishalRokaha/AI-RESUME-ANALYZER.git
```
```
cd AI-RESUME-ANALYZER
```
### 2️⃣ Set Up a Virtual Environment
```
python -m venv myenv
```
```
./myenv/Scripts/activate
```
### 3️⃣ Install Dependencies
Make sure you have pip updated, then install all required packages:
```
pip install -r requirements.txt
```
### 4️⃣ Set Up Your .env File
Create a .env file in the root directory and add your Groq API key from [Groq](https://groq.com/) 

```
GROQ_API_KEY=your_groq_api_key_here
```
### 5️⃣ Run the Streamlit App
Launch the app locally using Streamlit:
```
streamlit run main.py
```
### 6️⃣ Open in Browser
Once the app starts, it will automatically open in our default web browser at:
```
http://localhost:8501
```
---
✅ Now We’re all set!
Upload a resume, paste a job description, and let the AI analyze our resume for job-fit and provide suggestions. 

## Contributing
Contributions are truly welcome! If you find any issues or have suggestions for improvements, please open an issue or fork the repository and submit a pull request. Don't forget to give this project a star. Thank you very much!

## Contact
For any questions, feedback, or collaboration requests, please reach out to me via:
- **Email**: bissurokaha@gmail.com
- **GitHub**: [BishalRokaha](https://github.com/BishalRokaha)
- **LinkedIn**: [Bishal Rokaha](https://www.linkedin.com/in/bishal-rokaha-78a549251/)
