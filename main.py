from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

# Initialize FastAPI application
app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend's domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/fetch_captions")
async def fetch_captions(request: Request):
    # Parse JSON body
    body = await request.json()
    video_id = body.get("video_id")
    
    # Validate video_id
    if not video_id:
        raise HTTPException(status_code=400, detail="Missing 'video_id' parameter")
    
    try:
        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        return {"transcript": transcript}
    except TranscriptsDisabled:
        raise HTTPException(status_code=400, detail="Transcripts are disabled for this video.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))











# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# from PyPDF2 import PdfReader
# import google.generativeai as genai

# app = FastAPI()

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Configure the Generative AI API
# genai.configure(api_key=("AIzaSyBn02bvpLahIkwU-7EFOWpW6RxZF0Aa2I8"))


# # Prompt template
# input_prompt = """
# You are an AI-powered resume analyzer. Analyze the following resume and compare it with the provided job description. 
# Generate the following:
# 1. Analysis and suggestions for improvement in the resume.
# 2. An updated version of the resume that aligns better with the job description.

# Resume:
# {text}

# Job Description:
# {jd}
# """

# def input_pdf_text(file):
#     """
#     Extract text from uploaded PDF file.
#     """
#     try:
#         pdf = PdfReader(file)
#         text = ""
#         for page in pdf.pages:
#             text += page.extract_text()
#         return text
#     except Exception as e:
#         return f"Error extracting text: {e}"

# def get_gemini_response(input):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content(input)
#     return response

# @app.post("/analyze-resumes/")
# async def analyze_resumes(
#     jd: UploadFile = File(...),
#     resume: UploadFile = File(...)
# ):
#     """
#     Analyze the resume against the job description and return suggestions and an updated resume.
#     """
#     # Extract text from uploaded PDFs
#     jd_text = input_pdf_text(jd.file)
#     resume_text = input_pdf_text(resume.file)

#     # Generate response using the AI model
#     prompt = input_prompt.format(text=resume_text, jd=jd_text)
#     response = get_gemini_response(prompt)

#     # Process the response
#     try:
#         candidate_content = response.candidates[0].content.parts[0].text
#         # Split based on sections if model returns unified text
#         sections = candidate_content.split("--- Updated Resume ---")
#         analysis_content = sections[0].strip() if len(sections) > 0 else "Analysis not found."
#         updated_resume_content = sections[1].strip() if len(sections) > 1 else "Updated resume not found."
#     except (IndexError, AttributeError, KeyError) as e:
#         analysis_content = f"Error in processing analysis: {e}"
#         updated_resume_content = f"Error in processing updated resume: {e}"

#     return {
#         "analysis": analysis_content,
#         "updated_resume": updated_resume_content,
#     }
