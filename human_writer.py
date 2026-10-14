# human_writer.py
from llm_client import chat
from prompts import WRITER_PROMPT

def write_human_style(filtered_data, original_title):
    facts = "\n".join(f"- {f}" for f in filtered_data.get("key_facts", []))
    user_input = WRITER_PROMPT.replace("{key_facts}", facts or original_title)
    
    return chat("You are a human news editor for competitive exam aspirants.",
                user_input, temperature=0.7)
