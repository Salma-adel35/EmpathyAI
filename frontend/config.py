import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:5000"
)

USE_MOCK_API = os.getenv(
    "USE_MOCK_API",
    "true"
).lower() == "true"