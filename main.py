from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from typing import Annotated
from fastapi import FastAPI, Depends, Request, HTTPException
import resumeFunction as resfn
import requests

import subprocess
import pdflatex


# AI feeback generator libraries
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


# Feature 1: Input Data to generate Resume


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate-resume/", response_class=HTMLResponse)
async def generate_resume(request: Request):
    form_data = await request.form()

    with open("templates/resume_template1.tex", "a") as f:
        # heading
        f.write(
            resfn.heading(
                form_data.getlist("full_name")[0],
                form_data.getlist("phone")[0],
                form_data.getlist("email")[0],
                form_data.getlist("linkedin")[0],
                form_data.getlist("titles"),
            )
        )

        # f.write(resfn.education())
    # with open("templates/resume_template.tex", "r") as f:
    #     latex_code = f.read()
    #     url = "https://latexonline.cc/compile"

    # # Parameters for the request
    # params = {"code": latex_code, "output": "pdf", "command": "pdflatex"}

    # # Send the request to compile the LaTeX code
    # response = requests.post(url, data=params)

    # # Save the response content as a PDF file
    # pdf_output_path = "output.pdf"
    # with open(pdf_output_path, "wb") as f:
    # f.write(response.content)

    # Path to your LaTeX file
    latex_file_path = "templates/resume_template.tex"

    # Compile the LaTeX file to PDF
    result = subprocess.run(
        ["pdflatex", latex_file_path], capture_output=True, text=True
    )
    # Check if the compilation was successful
    if result.returncode == 0:
        print("PDF generated successfully.")
    else:
        print("Failed to generate PDF.")
        print(result.stdout)
        print(result.stderr)

    return "done"


# Feature 7: Upload of resume for AI feedback


@app.get("/docx-submit", response_class=HTMLResponse)
def submit_docx(request: Request):
    return templates.TemplateResponse("docx_upload4AI.html", {"request": request})


@app.post("/feedback", response_class=HTMLResponse)
async def feedback(request: Request, feedback_file: UploadFile = File(...)):
    try:
        doc = Document(BytesIO(await feedback_file.read()))
        text_lines = [para.text for para in doc.paragraphs]
        full_text = "\n".join(text_lines)

        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Is the resume good? if it is good, please say so. Else, give advice on how to improve the resume: {full_text}",
                }
            ],
            model="llama3-70b-8192",
        )

        result = chat_completion.choices[0].message.content
        result_l = result.split("\n")

        return templates.TemplateResponse(
            "docx_upload4AI.html", {"request": request, "result_l": result_l}
        )
    except:
        return "Please upload a docx file"
