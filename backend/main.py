from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.model_utils import predict

CONFIDENCE_THRESHOLD = 0.60
MAX_SIZE = 5 * 1024 * 1024  # 5 MB

app = FastAPI(title="Plant Disease Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(status_code=400, detail="Upload a JPEG or PNG image.")

    data = await file.read()
    if len(data) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="Image too large (max 5 MB).")

    try:
        top = predict(data, top_k=3)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read the image.")

    best = top[0]
    confident = best["confidence"] >= CONFIDENCE_THRESHOLD
    plant, _, condition = best["class"].partition("___")

    return {
        "plant": plant.replace("_", " "),
        "condition": condition.replace("_", " "),
        "confidence": best["confidence"],
        "is_confident": confident,
        "message": None if confident else "Not sure about this one. Try a clearer, closer photo of a single leaf.",
        "top_3": top,
    }