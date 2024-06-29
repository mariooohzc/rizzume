import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from main import app

client = TestClient(app)


@pytest.fixture
def docx_file():
    file_content = b"Sample DOCX content"
    file_obj = BytesIO(file_content)
    return (
        "feedback_file",
        file_obj,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@pytest.fixture
def pdf_file():
    file_content = b"Sample PDF content"
    file_obj = BytesIO(file_content)
    return ("feedback_file", file_obj, "application/pdf")


def test_submit_docx_file(docx_file):
    response = client.post("/feedback", files={"feedback_file": docx_file})
    assert response.status_code == 200


def test_submit_non_docx_file(pdf_file):
    response = client.post("/feedback", files={"feedback_file": pdf_file})
    assert response.status_code == 200
    assert "please submit Docx file" in response.text
