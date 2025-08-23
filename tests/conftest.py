import pytest
from PIL import Image, ImageDraw, ImageFont
from starlette.testclient import TestClient
from medical_advice_assistant.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session")
def sample_image_path():
    """Creates a sample image for testing and returns the path."""
    text = "Take one tablet by mouth daily"
    filename = "tests/sample_prescription.png"
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 15)
    except IOError:
        font = ImageFont.load_default()

    img = Image.new('RGB', (400, 50), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill=(0, 0, 0), font=font)
    img.save(filename)
    return filename
