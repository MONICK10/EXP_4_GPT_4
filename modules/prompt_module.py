"""Prompt Module - builds the structured prompt that is sent to the LLM.

It has: Role, User profile, Preference analysis, Candidate items, Task, Output format.
"""


def build(p, pref, candidates, feedback=""):
    items = "\n".join(f"{c['item_id']} | {c['title']} | {c['category']} | {c['level']} | {c['type']} | {c['description']}"
                      for c in candidates)
    fb = f"\nUser feedback to apply: {feedback}\n" if feedback else ""
    return (
        "ROLE: You are a personalised learning recommendation assistant.\n\n"
        f"USER PROFILE:\n- Name: {p['name']}\n- Age: {p['age']}\n- Background: {p['background']}\n"
        f"- Interests: {', '.join(p['interests'])}\n- Skill level: {p['skill_level']}\n"
        f"- Preferred category: {p['category']}\n- Goal: {p['goal']}\n- Preferences: {p['preferences']}\n\n"
        f"PREFERENCE ANALYSIS:\n- Key interests: {', '.join(pref['key_interests'])}\n"
        f"- Learning style: {pref['learning_style']}\n- Avoid: {', '.join(pref['avoid']) or 'none'}\n{fb}\n"
        f"CANDIDATE ITEMS (id | title | category | level | type | description):\n{items}\n\n"
        f"TASK: Choose the {p['n_items']} best items for this user from the candidates only, best first.\n"
        'OUTPUT FORMAT: JSON {"recommendations": [{"item_id": "...", "reason": "<one short sentence>"}]}'
    )
