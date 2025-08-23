from fastapi import FastAPI
from pydantic import BaseModel

class TextQuery(BaseModel):
    text: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

def query_knowledge_base(query: str) -> str:
    """Placeholder for knowledge base retrieval."""
    return "Retrieved information about symptoms and conditions."

def query_llm(query: str, context: str) -> str:
    """Placeholder for the medical LLM."""
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
