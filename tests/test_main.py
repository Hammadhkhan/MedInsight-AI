from medical_advice_assistant.main import DISCLAIMER

def test_get_advice(client):
    response = client.post("/advice", json={"text": "I have a headache."})
    assert response.status_code == 200
    json_response = response.json()
    assert "advice" in json_response
    assert "disclaimer" in json_response
    assert json_response["disclaimer"] == DISCLAIMER
    assert "headache" in json_response["advice"]

def test_upload_document(client, sample_image_path):
    with open(sample_image_path, "rb") as f:
        response = client.post("/upload-document", files={"file": ("sample_prescription.png", f, "image/png")})

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["filename"] == "sample_prescription.png"
    assert "extracted_text" in json_response
    assert "advice" in json_response
    assert "disclaimer" in json_response
    assert "Take one tablet by mouth daily" in json_response["extracted_text"]

def test_analyze_image(client, sample_image_path):
    with open(sample_image_path, "rb") as f:
        response = client.post("/analyze-image", files={"file": ("sample_image.png", f, "image/png")})

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["filename"] == "sample_image.png"
    assert "analysis" in json_response
    assert "advice" in json_response
    assert "disclaimer" in json_response
    assert "Image analysis complete" in json_response["analysis"]
