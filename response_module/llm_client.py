"""
Handles LLM API communication with automatic fallback capability.
"""

import os
from dotenv import load_dotenv

load_dotenv()

def call_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Calls the OpenAI API if an API key is available.
    Returns None if API key is unconfigured or call fails, triggering fallback mode.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("LLM_MODEL", "gpt-4o-mini")

    if not api_key or api_key.strip() == "" or api_key == "your_openai_api_key_here":
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[LLM Client Warning] API call failed ({e}). Falling back to safe response engine.")
        return None