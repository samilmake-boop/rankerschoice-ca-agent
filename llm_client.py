# llm_client.py
import os
import requests
import json
import time

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Try these models in order — first one that works will be used
GROQ_MODELS = [
    "llama-3.3-70b-versatile",        # current flagship (try first)
    "llama-3.1-8b-instant",           # older, might still work
    "llama-3.1-70b-versatile",        # older 70B
    "gemma2-9b-it",                   # Google's Gemma 2
    "mixtral-8x7b-32768",             # Mixtral fallback
]


def chat(system_prompt, user_input, temperature=0.3, json_mode=False, retries=2):
    """Call Groq with automatic model fallback."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    last_error = None
    for model in GROQ_MODELS:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            "temperature": temperature,
            "max_tokens": 2000,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        for attempt in range(retries):
            try:
                r = requests.post(GROQ_URL, headers=headers, json=payload, timeout=60)

                if r.status_code == 429:
                    # Rate limit — wait and retry
                    print(f"     (rate limit, waiting 30s...)")
                    time.sleep(30)
                    continue

                if r.status_code == 404:
                    # Model not found — try next model
                    print(f"     [model '{model}' not found, trying next...]")
                    last_error = f"Model {model} not found"
                    break

                if r.status_code != 200:
                    # Other error — show real message
                    try:
                        err_body = r.json()
                        err_msg = err_body.get("error", {}).get("message", r.text[:200])
                    except Exception:
                        err_msg = r.text[:200]
                    print(f"     [HTTP {r.status_code}: {err_msg}]")
                    last_error = f"HTTP {r.status_code}: {err_msg}"
                    break

                # Success!
                return r.json()["choices"][0]["message"]["content"]

            except requests.exceptions.Timeout:
                print(f"     [timeout, retry {attempt+1}/{retries}...]")
                time.sleep(5)
                continue
            except Exception as e:
                print(f"     [exception: {e}]")
                last_error = str(e)
                break

    raise Exception(f"All Groq models failed. Last error: {last_error}")


def test_connection():
    """Quick test to verify the API key works."""
    print("Testing Groq API...")
    try:
        result = chat(
            "You are a test assistant.",
            "Reply with: OK",
            temperature=0,
        )
        print(f"✅ Groq works! Response: {result[:50]}")
        return True
    except Exception as e:
        print(f"❌ Groq failed: {e}")
        return False


if __name__ == "__main__":
    test_connection()
