from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import logging
import time
from functools import lru_cache

# Import from your modules
from app.config import MODEL_PATH, SECRET_KEY, RATE_LIMIT
from app.auth import verify_token

# Logging
logging.basicConfig(level=logging.INFO)

# Load model
model = joblib.load(MODEL_PATH)

# App
app = FastAPI(title="Email Classification API", version="3.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# RATE LIMITING
# ==========================================
request_log = {}

def rate_limiter(request: Request):
    ip = request.client.host
    current_time = time.time()

    if ip not in request_log:
        request_log[ip] = []

    request_log[ip] = [t for t in request_log[ip] if current_time - t < 60]

    if len(request_log[ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    request_log[ip].append(current_time)

# ==========================================
# REQUEST SCHEMA
# ==========================================
class EmailRequest(BaseModel):
    text: str

# ==========================================
# CACHE
# ==========================================
@lru_cache(maxsize=1000)
def cached_predict(text: str):
    return model.predict([text])[0]

# ==========================================
# ROUTES
# ==========================================
@app.get("/")
def home():
    return {"message": "API Running 🚀", "version": "3.0"}

@app.post("/token")
def generate_token():
    import jwt
    token = jwt.encode({"user": "test"}, SECRET_KEY, algorithm="HS256")
    return {"token": token}

@app.post("/predict")
def predict(
    data: EmailRequest,
    request: Request,
    user=Depends(verify_token)
):
    rate_limiter(request)

    text = data.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Empty text")

    logging.info(f"User: {user} | Input: {text}")

    prediction = cached_predict(text)

    return {"prediction": prediction}