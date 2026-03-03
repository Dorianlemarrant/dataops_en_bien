import enum
import joblib
from fastapi import FastAPI
from main import predict as predict_name
import requests
import os


app = FastAPI()
model = joblib.load("model.joblib")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:0.8b")


class Model(enum.Enum):
    ML = "ml"
    LLM = "llm"


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/api/predict")
async def predict(name: str, model_type: Model = Model.ML):
    if model_type == Model.ML:
        return {
            "name": name,
            "sex": "M" if int(predict_name(model, name)[0]) == 1 else "F",
        }
    elif model_type == Model.LLM:
        system_prompt = """
You are a name identification expert, you role is to return the sex a of a given name.

Example: 
- if you get "Alain" you should return "M"
- if you get "Anais" you should return "F".
"""
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": f"User name: {name}",
                    },
                ],
                "stream": False,
                "think": False,
                "format": {
                    "type": "object",
                    "properties": {
                        "sex": {"type": "string", "enum": ["M", "F"]},
                    },
                    "required": ["sex"],
                },
            },
        )
        return {
            "name": name,
            "sex": response.json()["message"]["content"],
        }
