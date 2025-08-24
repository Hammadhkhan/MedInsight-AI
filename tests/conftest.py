import pytest
from PIL import Image, ImageDraw, ImageFont
from starlette.testclient import TestClient
from medical_advice_assistant.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

import os

@pytest.fixture(scope="session")
def sample_video_path():
    """Provides the path to the sample video file."""
    return "tests/sample_video.mp4"

@pytest.fixture(scope="session")
def sample_image_path():
    """Creates a sample image for testing and returns the path."""
    text = "Take one tablet by mouth daily"
    filename = "tests/sample_prescription.png"

    # Use the bundled font to ensure consistency.
    font_path = "tests/LiberationSans-Regular.ttf"
    font = ImageFont.truetype(font_path, size=30)

    # Create a larger image with a white background.
    img = Image.new('RGB', (600, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(img)

    # Draw the text on the image.
    d.text((20, 20), text, fill=(0, 0, 0), font=font)

    img.save(filename)
    return filename
