from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import re


#AI feeback generator libraries
from docx import Document
from io import BytesIO
from groq import Groq

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class ResumeRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    skills: str


#Feature 1: Input Data to generate Resume

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate-resume/", response_class=HTMLResponse)
async def generate_resume(request: Request, full_name: str = Form(...), email: str = Form(...), phone: str = Form(...), skills: str = Form(...)):
    resume_request = ResumeRequest(full_name=full_name, email=email, phone=phone, skills=skills)
    resume_template = f"""
    <html>
    <head>
        <title>Generated Resume</title>
    </head>
    <body>
        <h1>Resume for {resume_request.full_name}</h1>
        <p>Email: {resume_request.email}</p>
        <p>Phone: {resume_request.phone}</p>
        <p>Skills: {resume_request.skills}</p>
    </body>
    </html>
    """
    return HTMLResponse(content=resume_template)



#Feature 7: Upload of resume for AI feedback

@app.get("/docx-submit", response_class=HTMLResponse)
def submit_docx(request: Request):
    return templates.TemplateResponse("docx_upload4AI.html", {"request": request})


@app.post("/feedback", response_class = HTMLResponse)
async def feedback(request: Request, feedback_file: UploadFile = File(...)):
    try:
        doc = Document(BytesIO(await feedback_file.read()))
        text_lines = [para.text for para in doc.paragraphs]
        full_text = "\n".join(text_lines)

        client = Groq(api_key= os.environ.get("GROQ_API_KEY"))

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Is the resume good? if it is good, please say so. Else, give advice on how to improve the resume: {full_text}",
                }
            ],
            model="llama3-8b-8192",
        )

        result = chat_completion.choices[0].message.content
        result_l = result.split("\n")

        return templates.TemplateResponse("docx_upload4AI.html", {"request":request, "result_l": result_l})
    except:
        return "Please upload a docx file"





