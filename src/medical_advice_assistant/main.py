from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import easyocr
from contextlib import asynccontextmanager
import torch
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights
from PIL import Image
import io
import numpy as np


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the OCR model on startup
    app.state.ocr = easyocr.Reader(['en'])

    # Load the image analysis model on startup
    weights = EfficientNet_B0_Weights.DEFAULT
    app.state.image_analyzer = efficientnet_b0(weights=weights)
    app.state.image_analyzer.eval()
    app.state.image_transforms = weights.transforms()

    yield

    # Clean up the models on shutdown
    app.state.ocr = None
    app.state.image_analyzer = None


class TextQuery(BaseModel):
    text: str

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

def query_knowledge_base(query: str) -> str:
    """Placeholder for knowledge base retrieval."""
    return "Retrieved information about symptoms and conditions."

def query_llm(query: str, context: str, image_analysis_result: str | None = None) -> str:
    """Placeholder for the medical LLM."""
    if image_analysis_result:
        context = f"{context} Image analysis results: {image_analysis_result}."
    return f"Based on the context '{context}', the advice for '{query}' is to consult a doctor."

DISCLAIMER = "This is informational only. Consult a licensed medical professional for diagnosis or treatment."

@app.post("/advice")
def get_advice(query: TextQuery):
    knowledge_base_context = query_knowledge_base(query.text)
    llm_response = query_llm(query.text, knowledge_base_context)
    return {
        "advice": llm_response,
        "disclaimer": DISCLAIMER,
    }

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # Preprocess the image and add a batch dimension
    preprocessed_image = app.state.image_transforms(image).unsqueeze(0)

    # Perform inference
    with torch.no_grad():
        output = app.state.image_analyzer(preprocessed_image)

    # Get the prediction
    prediction = output.argmax(dim=1).item()

    # For now, just return a mock analysis.
    # In a real application, this would be a more meaningful result.
    mock_analysis = f"Image analysis complete. Highest-scoring class index: {prediction}"

    # Integrate with advice pipeline
    query = "analysis of the uploaded image"
    knowledge_base_context = query_knowledge_base(query)
    llm_response = query_llm(query, knowledge_base_context, image_analysis_result=mock_analysis)

    return {
        "filename": file.filename,
        "analysis": mock_analysis,
        "advice": llm_response,
        "disclaimer": DISCLAIMER,
    }

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()

    # easyocr can handle bytes directly
    ocr_result = app.state.ocr.readtext(contents)

    extracted_text = " ".join([res[1] for res in ocr_result])

    if not extracted_text:
        return {
            "filename": file.filename,
            "advice": "Could not extract any text from the document.",
            "disclaimer": DISCLAIMER,
        }

    knowledge_base_context = query_knowledge_base(extracted_text)
    llm_response = query_llm(extracted_text, knowledge_base_context)

    return {
        "filename": file.filename,
        "extracted_text": extracted_text,
        "advice": llm_response,
        "disclaimer": DISCLAIMER,
    }
