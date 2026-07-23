import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:5000"
)

USER_ID = os.getenv(
    "USER_ID",
    "demo_user"
)