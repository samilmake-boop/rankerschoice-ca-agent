# exam_filter.py
import json
from llm_client import chat
from prompts import FILTER_PROMPT

def filter_article(article):
    if len(article["body"]) < 200:
        return False, {}
    
    user_input = FILTER_PROMPT.replace("{article_text}", article["body"][:3000])
    try:
        resp = chat("You are an exam-relevance AI judge.", user_input, 
                    temperature=0.2, json_mode=True)
        data = json.loads(resp)
        return data.get("is_relevant", False), data
    except Exception as e:
        print(f"Filter error: {e}")
        return False, {}
