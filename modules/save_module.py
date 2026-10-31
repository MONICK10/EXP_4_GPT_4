"""Save Module - saves the profile and the final recommendations to a JSON file."""
import json
import os
import re
from datetime import datetime

FOLDER = os.path.join(os.path.dirname(__file__), "..", "saved")


def save(profile, items):
    os.makedirs(FOLDER, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "_", profile.get("name", "user").lower()).strip("_")
    path = os.path.join(FOLDER, f"recommendations_{slug}_{datetime.now():%Y%m%d_%H%M%S}.json")
    data = {"saved_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"), "profile": profile,
            "recommendations": [{k: i.get(k) for k in ("rank", "item_id", "title", "category", "level", "type", "score",
                                                       "explanation")} for i in items]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return {"file": os.path.abspath(path), "count": len(items)}
