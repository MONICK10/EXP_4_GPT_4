"""Intent Module - understands what the user typed in the feedback box.

Example: "show me more practical stuff"   -> REFINE
         "why did you suggest item 2?"    -> EXPLAIN
         "save this list"                 -> SAVE
"""
from llm import ask_json

INTENTS = {"REFINE": "feedback to change or improve the recommendations",
           "EXPLAIN": "asks why something was recommended",
           "SAVE": "wants to save or download the recommendations",
           "NEW": "wants to start again with a new profile"}


def keyword_intent(t):
    t = t.lower()
    if "save" in t or "download" in t:
        return "SAVE"
    if "why" in t or "explain" in t:
        return "EXPLAIN"
    if "start over" in t or "new profile" in t or "reset" in t:
        return "NEW"
    return "REFINE"


def detect(text):
    opts = "\n".join(f"{k} - {v}" for k, v in INTENTS.items())
    d = ask_json(f"User message in a recommendation app: \"{text}\"\nPick one intent:\n{opts}\n"
                 'Return JSON: {"intent": "...", "reason": "<short reason>"}', default={}) or {}
    intent = str(d.get("intent", "")).upper()
    if intent not in INTENTS:
        return {"intent": keyword_intent(text), "reason": "Keyword fallback", "source": "rules"}
    return {"intent": intent, "reason": d.get("reason", ""), "source": "LLM"}
