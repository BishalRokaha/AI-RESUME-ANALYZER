import streamlit as st                            # For Web Interface
from pdfminer.high_level import extract_text      # To Extract Text from Resume PDF
from sentence_transformers import SentenceTransformer      # To generate Embeddings of text
from sklearn.metrics.pairwise import cosine_similarity     # To get ATS Score of Resume and Job Description
from groq import Groq                             # API to use LLM
import re                                         # To perform Regular Expression Functions
from dotenv import load_dotenv                    # Loading API Key from .env file
import os


# Loading environment variables from .env
load_dotenv()

# Fetching the key from the environment
api_key = os.getenv("GROQ_API_KEY")


#  Session States to store values 
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if "resume" not in st.session_state:
    st.session_state.resume=""

if "job_desc" not in st.session_state:
    st.session_state.job_desc=""



# Title of the Project
st.title("AI Resume Analyzer 📝")



# <------- Defining Functions ------->

# Function to extract text from PDF
def extract_pdf_text(uploaded_file):
    try:
        extracted_text = extract_text(uploaded_file)
        return extracted_text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return "Could not extract text from the PDF file."


# Function to calculate similarity 
def calculate_similarity_bert(text1, text2):
    ats_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')      
    # Encode the texts directly to embeddings
    embeddings1 = ats_model.encode([text1])
    embeddings2 = ats_model.encode([text2])
    
    # Calculate cosine similarity without adding an extra list layer
    similarity = cosine_similarity(embeddings1, embeddings2)[0][0]
    return similarity


def get_report(resume,job_desc):
    client = Groq(api_key=api_key)

    # Change the prompt to get the results in your style
    prompt=f"""
    # Context:
    - You are an AI Resume Analyzer, you will be given Candidate's resume and Job Description of the role he is applying for.

    # Instruction:
    - Analyze candidate's resume based on the possible points that can be extracted from job description,and give your evaluation on each point with the criteria below:  
    - Consider all points like required skills, experience,etc that are needed for the job role.
    - Calculate the score to be given (out of 5) for every point based on evaluation at the beginning of each point with a detailed explanation.  
    - If the resume aligns with the job description point, mark it with ✅ and provide a detailed explanation.  
    - If the resume doesn't align with the job description point, mark it with ❌ and provide a reason for it.  
    - If a clear conclusion cannot be made, use a ⚠️ sign with a reason.  
    - The Final Heading should be "Suggestions to improve your resume:" and give where and what the candidate can improve to be selected for that job role.

    # Inputs:
    Candidate Resume: {resume}
    ---
    Job Description: {job_desc}

    # Output:
    - Each any every point should be given a score (example: 3/5 ). 
    - Mention the scores and  relevant emoji at the beginning of each point and then explain the reason.
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

def extract_scores(text):
    # Regular expression pattern to find scores in the format x/5, where x can be an integer or a float
    pattern = r'(\d+(?:\.\d+)?)/5'
    # Find all matches in the text
    matches = re.findall(pattern, text)
    # Convert matches to floats
    scores = [float(match) for match in matches]
    return scores




# <--------- Starting the Work Flow ---------> 

# Displays Form only if the form is not submitted
if not st.session_state.form_submitted:
    with st.form("my_form"):

        # Taking input a Resume (PDF) file 
        resume_file = st.file_uploader(label="Upload your Resume/CV in PDF format", type="pdf")

        # Taking input Job Description
        st.session_state.job_desc = st.text_area("Enter the Job Description of the role you are applying for:",placeholder="Job Description...")

        # Form Submission Button
        submitted = st.form_submit_button("Analyze")
        if submitted:

            #  Allowing only if Both Resume and Job Description are Submitted
            if st.session_state.job_desc and resume_file:
                st.info("Extracting Information")

                st.session_state.resume = extract_pdf_text(resume_file)      # Calling the function to extract text from Resume

                st.session_state.form_submitted = True
                st.rerun()                 # Refresh the page to close the form and give results

            # Donot allowing if not uploaded
            else:
                st.warning("Please Upload both Resume and Job Description to analyze")


if st.session_state.form_submitted:
    score_place = st.info("Generating Scores...")

    # Call the function to get ATS Score
    ats_score = calculate_similarity_bert(st.session_state.resume,st.session_state.job_desc)

    col1,col2 = st.columns(2,border=True)
    with col1:
        st.write("ATS Score:")
        st.subheader(f"{ats_score * 100:.2f}%")

    # Call the function to get the Analysis Report from LLM (Groq)
    report = get_report(st.session_state.resume,st.session_state.job_desc)

    # Calculate the Average Score from the LLM Report
    report_scores = extract_scores(report)                 # Example : [3/5, 4/5, 5/5,...]
    avg_score = sum(report_scores) / (5*len(report_scores))  # Example: 2.4


    with col2:
        st.write("AI Report:")
        st.subheader(f"{avg_score * 100:.2f}%")
    score_place.success("Scores generated successfully!")


    st.subheader("AI Generated Analysis Report:")

    # Displaying Report 
    st.markdown(f"""
            <div style='text-align: left; background-color: #000000; padding: 10px; border-radius: 10px; margin: 5px 0;'>
                {report}
            </div>
            """, unsafe_allow_html=True)
    
    # Download Button
    st.download_button(
        label="Download Report",
        data=report,
        file_name="report.txt",
        icon=":material/download:",
        )
    

# <-------------- End of the Work Flow --------------->