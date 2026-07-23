import requests

from config import BACKEND_URL


def send_message(
    message: str,
    user_id: str
):

    response = requests.post(

        f"{BACKEND_URL}/chat",

        json={

            "user_id": user_id,

            "message": message

        },

        timeout=120

    )

    response.raise_for_status()

    return response.json()