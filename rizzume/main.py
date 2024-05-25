from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# Templates directory
templates = Jinja2Templates(directory="templates")

class ResumeRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    skills: str


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

@app.get("/fill-up", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("fill_up_form.html", {"request": request})

