import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH", "model/model_pipeline.joblib")
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 10))