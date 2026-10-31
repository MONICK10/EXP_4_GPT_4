"""Preference Module - the LLM reads the free-text preferences and pulls out what matters.

Example: "I prefer practical courses, not theory" -> learning_style = "Practical"
"""
from llm import as_list, ask_json


def analyze(p):
    prompt = (f"Analyse this learner profile.\nBackground: {p['background']}\nInterests: {', '.join(p['interests'])}\n"
              f"Skill level: {p['skill_level']}\nGoal: {p['goal']}\nPreferences (free text): {p['preferences']}\n\n"
              'Return JSON: {"key_interests": ["..."], "learning_style": "Practical|Theory|Mixed", '
              '"focus_areas": ["..."], "avoid": ["..."], "summary": "<one sentence>"}')
    d = ask_json(prompt, default={}) or {}
    style = str(d.get("learning_style", "")).title()
    if style not in ("Practical", "Theory", "Mixed"):
        t = p["preferences"].lower()
        style = "Practical" if ("practical" in t or "hands" in t or "project" in t) else "Theory" if "theory" in t else "Mixed"
    return {"key_interests": as_list(d.get("key_interests")) or p["interests"],
            "learning_style": style,
            "focus_areas": as_list(d.get("focus_areas")),
            "avoid": as_list(d.get("avoid")),
            "summary": d.get("summary", "")}
