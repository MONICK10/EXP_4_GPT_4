"""Profile Module - turns the raw input into a clean user profile and one-line summary.

Example summary: "Arun (20), Computer Science, Beginner, interested in AI, Python; goal: Learn AI"
"""


def build(u):
    summary = (f"{u['name']}{' (' + u['age'] + ')' if u['age'] else ''}, {u['background'] or 'learner'}, "
               f"{u['skill_level']} level, interested in {', '.join(u['interests'])}"
               f"{'; goal: ' + u['goal'] if u['goal'] else ''}")
    return {**u, "summary": summary, "search_text": " ".join(u["interests"]) + " " + u["goal"] + " " + u["preferences"]}
