# tests/test_api.py
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import create_app

client = TestClient(create_app())


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_tones():
    response = client.get("/api/v1/generate/tones")
    assert response.status_code == 200
    tones = response.json()["tones"]
    assert len(tones) == 4
    values = [t["value"] for t in tones]
    assert "professional" in values
    assert "casual" in values


def test_topic_too_short_rejected():
    response = client.post(
        "/api/v1/generate",
        json={"topic": "AI"},
    )
    assert response.status_code == 422


@patch("app.api.routes.generate.run_pipeline")
def test_generate_success(mock_pipeline):
    mock_pipeline.return_value = {
        "topic": "AI in Nigeria",
        "tone": "professional",
        "audience": "entrepreneurs",
        "outline": "1. Intro\n2. Main\n3. Conclusion",
        "blog_post": "AI is transforming Nigeria...",
        "summary": "AI is reshaping Nigerian business.",
        "captions": {
            "linkedin": "AI is here. #AI",
            "twitter": "AI changes everything. #Tech",
            "instagram": "Discover AI. #AI #Tech #Nigeria #Business #Growth",
        },
        "email": {
            "subject": "AI Is Here",
            "preview": "Learn how AI helps",
            "body": "Dear reader, AI is transforming business.",
            "cta": "Read More",
        },
    }

    response = client.post(
        "/api/v1/generate",
        json={
            "topic": "How AI is helping businesses in Nigeria",
            "tone": "professional",
            "audience": "Nigerian entrepreneurs",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["blog_post"] == "AI is transforming Nigeria..."
    assert data["captions"]["linkedin"] == "AI is here. #AI"
    assert data["email"]["subject"] == "AI Is Here"