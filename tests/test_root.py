import pytest


class TestRootAPI:
    """Test cases for root API endpoint"""

    def test_root_redirect(self, client):
        """Test that root endpoint redirects to index.html"""
        response = client.get("/", follow_redirects=False)

        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"