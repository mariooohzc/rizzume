import pytest
from httpx import AsyncClient
from bs4 import BeautifulSoup
from main import app


@pytest.mark.asyncio
async def test_jobsearch():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Test with an invalid search term
        response = await ac.post("/job-search", data={"search": "invalidsearchterm"})
        assert response.status_code == 200
        assert "No jobs found" in response.text

        # Test with empty search term
        response = await ac.post("/job-search", data={"search": ""})
        assert response.status_code == 200
        assert "Perhaps you searched for absolutely nothing?" in response.text

        # Test the error handling (simulate an error in web scraping)
        response = await ac.post("/job-search", data={"search": " "})
        assert response.status_code == 200
        assert "Perhaps you searched for absolutely nothing?" in response.text
