# frontend/api_client.py
import requests
from config import API_BASE_URL

TIMEOUT = 120  # generous — five LLM calls take time


def generate_content(topic: str, tone: str, audience: str) -> dict:
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/generate",
            json={"topic": topic, "tone": tone, "audience": audience},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. The pipeline takes ~20 seconds — please try again."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to the API. Is it running?"}
    except requests.exceptions.HTTPError as e:
        detail = e.response.json().get("detail", str(e))
        return {"success": False, "error": detail}


def get_tones() -> dict:
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/generate/tones", timeout=10)
        response.raise_for_status()
        return {"success": True, "data": response.json()["tones"]}
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_health() -> bool:
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False