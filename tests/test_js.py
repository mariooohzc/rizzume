import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from bs4 import BeautifulSoup
from main import app  # Assuming your FastAPI app is defined in main.py

client = TestClient(app)


@pytest.fixture
def invalid_search_term():
    return {"search": "invalidsearchterm"}


@pytest.fixture
def empty_search_term():
    return {"search": ""}


@pytest.fixture
def whitespace_search_term():
    return {"search": " "}


@pytest.mark.asyncio
async def test_jobsearch_invalid_search_term(invalid_search_term):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/job-search", data=invalid_search_term)
        assert response.status_code == 200
        assert "No jobs found, please key in another job" in response.text


@pytest.mark.asyncio
async def test_jobsearch_empty_search_term(empty_search_term):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/job-search", data=empty_search_term)
        assert response.status_code == 200
        assert (
            "Perhaps you searched for absolutely nothing? Please enter a valid search term."
            in response.text
        )


@pytest.mark.asyncio
async def test_jobsearch_whitespace_search_term(whitespace_search_term):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/job-search", data=whitespace_search_term)
        assert response.status_code == 200
        assert (
            "Perhaps you searched for absolutely nothing? Please enter a valid search term."
            in response.text
        )
