"""Explanation Module - explains in simple words why each item suits this user."""
from llm import ask_json


def explain(items, profile):
    listing = "\n".join(f"{i['item_id']}: {i['title']} ({i['level']}, {i['type']}) - {i['description']}" for i in items)
    prompt = (f"User: {profile['summary']}. Preferences: {profile['preferences']}\n\nRecommended items:\n{listing}\n\n"
              "For each item, explain in 1-2 simple sentences why it is a good fit for this user.\n"
              'Return JSON: {"explanations": {"<item_id>": "<explanation>"}}')
    d = ask_json(prompt, default={}) or {}
    ex = d.get("explanations") if isinstance(d.get("explanations"), dict) else {}
    return {i["item_id"]: ex.get(i["item_id"]) or i.get("llm_reason") or "Matches your interests and level."
            for i in items}
