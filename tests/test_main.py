from fastapi.testclient import TestClient
from src.main import app, DISCLAIMER

client = TestClient(app)

def test_get_advice():
    response = client.post("/advice", json={"text": "I have a headache."})
    assert response.status_code == 200
    json_response = response.json()
    assert "advice" in json_response
    assert "disclaimer" in json_response
    assert json_response["disclaimer"] == DISCLAIMER
    assert "headache" in json_response["advice"]
