from fastapi.testclient import TestClient

from app.main import app

SAMPLE_PROFILE = {
    "name": "Test Patient",
    "age": 40,
    "gender": "female",
    "conditions": "hypertension",
    "medications": "",
    "allergies": "",
    "health_goals": "lower blood pressure",
}


def test_health():
    with TestClient(app) as client:
        data = client.get("/api/health").json()
        assert data["status"] == "ok"
        assert data["llm_provider"] in ("demo", "openai")


def test_chat_and_emergency():
    with TestClient(app) as client:
        profiles = client.get("/api/profiles").json()
        if not profiles:
            profiles = [client.post("/api/profiles", json=SAMPLE_PROFILE).json()]

        pid = profiles[0]["id"]
        chat = client.post(
            "/api/chat",
            json={"profile_id": pid, "message": "What diet helps blood pressure?"},
        )
        assert chat.status_code == 200
        body = chat.json()
        assert body["reply"]
        assert body["provider"] in ("demo", "openai")

        emergency = client.post(
            "/api/chat",
            json={"profile_id": pid, "message": "I have severe chest pain"},
        )
        assert "possible_emergency" in emergency.json()["safety_flags"]
        assert emergency.json()["provider"] == "safety"
