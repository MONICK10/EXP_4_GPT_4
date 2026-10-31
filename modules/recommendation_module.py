"""Recommendation Module - finds candidate items by semantic search, then the LLM picks the best ones."""
import os

import pandas as pd

from llm import ask_json
from semantic import SemanticIndex

PATH = os.path.join(os.path.dirname(__file__), "..", "data", "catalog.csv")


class Recommender:
    def __init__(self):
        self.df = pd.read_csv(PATH)
        text = self.df.title + ". " + self.df.domain + ". " + self.df.description
        self.index = SemanticIndex(text.tolist())

    def candidates(self, profile, pref, exclude=(), k=12):
        query = profile["search_text"] + " " + " ".join(pref["key_interests"] + pref["focus_areas"])
        scores = self.index.scores(query)
        df = self.df.assign(similarity=scores.round(3))
        if profile["category"] != "Any":
            df = df[df.category == profile["category"]]
        df = df[~df.item_id.isin(exclude)]
        return df.sort_values("similarity", ascending=False).head(k).to_dict("records")

    def recommend(self, prompt, candidates, n):
        data = ask_json(prompt, temperature=0.3, default={}) or {}
        valid = {c["item_id"]: c for c in candidates}
        picks, seen = [], set()
        for r in data.get("recommendations", []) if isinstance(data.get("recommendations"), list) else []:
            iid = str(r.get("item_id", "")).strip() if isinstance(r, dict) else str(r).strip()
            if iid in valid and iid not in seen:
                seen.add(iid)
                picks.append({**valid[iid], "llm_rank": len(picks) + 1,
                              "llm_reason": r.get("reason", "") if isinstance(r, dict) else ""})
        # if the LLM returned fewer items, fill with the most similar candidates
        for c in candidates:
            if len(picks) >= n:
                break
            if c["item_id"] not in seen:
                seen.add(c["item_id"])
                picks.append({**c, "llm_rank": len(picks) + 1, "llm_reason": "Added by similarity search"})
        return picks[:n]
