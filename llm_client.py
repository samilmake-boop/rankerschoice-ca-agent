# llm_client.py
# 100% FREE LLM via OpenRouter — no credit card needed
# Uses Llama 3.3 70B (free tier) with automatic fallback to other free models

import os
import requests
import time

OPENROUTER_API_KEY = os.environ["GROQ_API_KEY"]  # reuse the same secret name
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Free models — try in priority order (best first)
FREE_MODELS = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "qwen/qwen-2.5-72b-instruct:free",
    "mistralai/mistral-small-24b-instruct-2501:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "google/gemini-flash-1.5:free",
    "deepseek/deepseek-r1:free",
]


def chat(system_prompt, user_input, temperature=0.3, json_mode=False, retries=2):
    """Call OpenRouter with auto-fallback across free models."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ranekrschoice.com",
        "X-Title": "RankersChoice CA Agent",
    }

    last_error = None
    for model in FREE_MODELS:
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
                r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=90)

                if r.status_code == 429:
                    # Free model rate-limited — wait briefly then try next model
                    print(f"     [rate limited on {model.split('/')[-1]}, trying next...]")
                    break  # break inner loop, try next model

                if r.status_code != 200:
                    try:
                        err_body = r.json()
                        err_msg = err_body.get("error", {}).get("message", r.text[:200])
                    except Exception:
                        err_msg = r.text[:200]
                    print(f"     [{model.split('/')[-1]}: HTTP {r.status_code}]")
                    last_error = f"HTTP {r.status_code}: {err_msg}"
                    break  # try next model

                # Success!
                return r.json()["choices"][0]["message"]["content"]

            except requests.exceptions.Timeout:
                print(f"     [timeout on {model.split('/')[-1]}, retry {attempt+1}/{retries}...]")
                time.sleep(5)
                continue
            except Exception as e:
                print(f"     [exception on {model.split('/')[-1]}: {e}]")
                last_error = str(e)
                break  # try next model

    raise Exception(f"All free models failed. Last error: {last_error}")


def test_connection():
    """Test OpenRouter API connection."""
    print("=" * 50)
    print("OPENROUTER API CONNECTION TEST")
    print("Testing all free models...")
    print("=" * 50)
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://ranekrschoice.com",
        "X-Title": "RankersChoice CA Agent",
    }
    
    for model in FREE_MODELS:
        short_name = model.split("/")[-1]
        print(f"\n  Testing: {short_name}")
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Reply with: OK"}],
            "max_tokens": 10,
        }
        try:
            r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
            if r.status_code == 200:
                resp = r.json()["choices"][0]["message"]["content"]
                print(f"    ✅ Works! Response: {resp[:30]}")
            else:
                print(f"    ❌ HTTP {r.status_code}")
        except Exception as e:
            print(f"    ❌ Error: {e}")


if __name__ == "__main__":
    test_connection()
