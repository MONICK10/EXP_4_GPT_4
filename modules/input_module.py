"""Input Module - collects the user's details from the form.

Example: Arun, 20, Computer Science, interests "AI, Python", Beginner, Course, goal "Learn AI", 5 items
"""
LEVELS = ["Beginner", "Intermediate", "Advanced"]
CATEGORIES = ["Any", "Course", "Project", "Book", "Certification"]


def collect(d):
    interests = [x.strip() for x in str(d.get("interests", "")).split(",") if x.strip()]
    if not interests:
        raise ValueError("Please enter at least one interest.")
    try:
        n = int(d.get("n_items") or 5)
    except ValueError:
        n = 5
    return {
        "name": (d.get("name") or "User").strip(),
        "age": str(d.get("age") or "").strip(),
        "background": (d.get("background") or "").strip(),
        "interests": interests,
        "skill_level": d.get("skill_level") if d.get("skill_level") in LEVELS else "Beginner",
        "category": d.get("category") if d.get("category") in CATEGORIES else "Any",
        "goal": (d.get("goal") or "").strip(),
        "preferences": (d.get("preferences") or "").strip(),
        "n_items": max(1, min(n, 10)),
    }
