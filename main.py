from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import re

# web scraping
from bs4 import BeautifulSoup
import requests


# AI feeback generator libraries
from docx import Document
from io import BytesIO
from groq import Groq

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# web scraping feature part 1
@app.get("/job", response_class=HTMLResponse)
async def jobs(request: Request):
    return templates.TemplateResponse("job_search.html", {"request": request})


# web scraping feature part 2
@app.post("/job-search", response_class=HTMLResponse)
async def jobsearch(request: Request, search: str = Form(None)):
    if not search or not search.strip():
        # Return a warning message if the search term is empty
        return templates.TemplateResponse(
            "job_search.html",
            {
                "request": request,
                "results": [
                    (
                        "Perhaps you searched for absolutely nothing? Please enter a valid search term.",
                        "",
                        "",
                    )
                ],
            },
        )

    # search for jobs using search result
    try:
        search_result = "-".join(search.split())
        url = "https://www.jobstreet.com.sg/" + search_result + "-jobs"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        a_tags = soup.findAll("a")
        href_values = [a_tag.get("href") for a_tag in a_tags]
        href_filtered = [
            i for i in href_values if i.startswith("/job/") and i.endswith("standalone")
        ]

        inner_url_list, company_list, job_title_list = list(), list(), list()

        for i in href_filtered:
            inner_url = "https://" + "jobstreet.com.sg" + i
            soup2 = BeautifulSoup(requests.get(inner_url).content, "html.parser")
            x = soup2.findAll("a")
            company = [
                coy.get_text() for coy in x if coy.get("href").startswith("/companies")
            ]
            if company[2] != "Explore companies":
                y = soup2.findAll("h1")
                job_title = [
                    title.get_text()
                    for title in y
                    if title.get("data-automation") == "job-detail-title"
                ]
                inner_url_list.append(inner_url)
                company_list.append(company[2])
                job_title_list.append(job_title[0])
            if len(job_title_list) == 10:
                break

        if len(job_title_list) == 0:
            return templates.TemplateResponse(
                "job_search.html",
                {
                    "request": request,
                    "results": [
                        (
                            "No jobs found, please key in another job",
                            "",
                            "",
                        )
                    ],
                },
            )

        results = list(zip(job_title_list, company_list, inner_url_list))
    except:
        return "Error with web scraping"

    return templates.TemplateResponse(
        "job_search.html", {"request": request, "results": results}
    )


# Feature 7: Upload of resume for AI feedback


@app.get("/", response_class=HTMLResponse)
def submit_docx(request: Request):
    return templates.TemplateResponse("docx_upload4AI.html", {"request": request})


# creating function to read contents in docx file
def filteringFile(feedback_file):
    if (not feedback_file.filename.endswith("docx")) and (
        not feedback_file.filename.endswith("doc")
    ):
        return -1
    return feedback_file


# feature for AI Feedback generation
@app.post("/feedback", response_class=HTMLResponse)
async def feedback(request: Request, feedback_file: UploadFile = File(...)):
    feedback_file = filteringFile(feedback_file)

    if feedback_file == -1:
        return "please submit Docx file"

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


# except:
#     return "Please upload a docx file"
