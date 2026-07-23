import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


client = None

if GEMINI_API_KEY:

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


def call_llm(
    system_prompt: str,
    user_prompt: str
) -> str | None:

    """
    Generate a complete response using Google Gemini.
    """

    if not GEMINI_API_KEY:

        print(
            "GEMINI_API_KEY is not set."
        )

        return None


    try:

        response = client.models.generate_content(

            model="gemini-3.5-flash",

            contents=user_prompt,

            config={

                "system_instruction": system_prompt,

                "max_output_tokens": 512,

                "thinking_config": {

                    "thinking_budget": 0

                }

            }

        )


        if not response:

            print(
                "Gemini returned no response."
            )

            return None


        if response.text:

            return response.text.strip()


        print(
            "Gemini returned an empty response."
        )

        return None


    except Exception as error:

        print(
            f"LLM call failed: {error}"
        )

        return None