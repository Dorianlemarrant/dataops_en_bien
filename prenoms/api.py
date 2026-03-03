import joblib
from fastapi import FastAPI
from main import predict as predict_name


app = FastAPI()
model = joblib.load("model.joblib")


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/api/predict")
async def predict(name: str):
    return {"name": name, "sex": "M" if int(predict_name(model, name)[0]) == 1 else "F"}
