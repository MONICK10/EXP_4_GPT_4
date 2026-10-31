"""Ranking Module - gives each item a suitability score (%) and sorts them.

Score = 50% semantic similarity + 20% level match + 15% learning-style match + 15% LLM rank
Example: similarity 0.62, level match, style match, LLM rank 1 of 5  ->  about 86%
"""
LEVEL_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}


def rank(items, profile, pref):
    n = max(len(items), 1)
    top_sim = max((i["similarity"] for i in items), default=1) or 1
    ranked = []
    for it in items:
        sim = it["similarity"] / top_sim                      # 0..1, best candidate = 1
        gap = abs(LEVEL_ORDER[it["level"]] - LEVEL_ORDER[profile["skill_level"]])
        level = 1.0 if gap == 0 else 0.5 if gap == 1 else 0.0
        style = 1.0 if it["type"] == pref["learning_style"] or it["type"] == "Mixed" else 0.4
        llm = 1 - (it["llm_rank"] - 1) / n
        score = 100 * (0.50 * sim + 0.20 * level + 0.15 * style + 0.15 * llm)
        # penalty if the item matches something the user wants to avoid
        text = f"{it['title']} {it['domain']} {it['category']}".lower()
        if any(a.lower() in text or (a.lower().rstrip("s") in text and len(a) > 3) for a in pref.get("avoid", [])):
            score -= 25
        ranked.append({**it, "score": max(0, round(score)), "parts": {"similarity": round(sim, 2), "level": level,
                                                               "style": style, "llm": round(llm, 2)}})
    ranked.sort(key=lambda x: -x["score"])
    for i, it in enumerate(ranked, 1):
        it["rank"] = i
    return ranked
