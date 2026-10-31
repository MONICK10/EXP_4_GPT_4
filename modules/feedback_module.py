"""Feedback Module - updates the profile using the user's feedback, so the next list is better.

Example: "I am more interested in AI than Web Development"
         -> add interest "Artificial Intelligence", avoid "Web Development"
"""
from llm import as_list, ask_json


def apply(profile, pref, feedback):
    prompt = (f"Current interests: {', '.join(profile['interests'])}. Learning style: {pref['learning_style']}.\n"
              f"User feedback on recommendations: \"{feedback}\"\n"
              'Return JSON: {"add_interests": ["..."], "avoid": ["..."], "learning_style": "Practical|Theory|Mixed|unchanged", '
              '"skill_level": "Beginner|Intermediate|Advanced|unchanged", "change_summary": "<one sentence>"}')
    d = ask_json(prompt, default={}) or {}
    new_profile = dict(profile)
    new_pref = dict(pref)
    add = as_list(d.get("add_interests"))
    avoid = as_list(d.get("avoid"))
    new_profile["interests"] = list(dict.fromkeys(add + profile["interests"]))
    new_profile["preferences"] = (profile["preferences"] + " " + feedback).strip()
    new_profile["search_text"] = " ".join(add * 2 + new_profile["interests"]) + " " + profile["goal"] + " " + feedback
    if str(d.get("skill_level", "")).title() in ("Beginner", "Intermediate", "Advanced"):
        new_profile["skill_level"] = str(d["skill_level"]).title()
    if str(d.get("learning_style", "")).title() in ("Practical", "Theory", "Mixed"):
        new_pref["learning_style"] = str(d["learning_style"]).title()
    new_pref["key_interests"] = list(dict.fromkeys(add + pref["key_interests"]))
    new_pref["avoid"] = list(dict.fromkeys(pref["avoid"] + avoid))
    changes = {"added_interests": add, "avoid": avoid, "summary": d.get("change_summary", "")}
    return new_profile, new_pref, changes
