"""
Ex. No. 4 - Personalized Recommendation System using GPT-4 style LLM (Llama 3.2 via Ollama)
Monick S - URK23CS1167
Main Module: connects all modules.

Run:  python app.py    then open  http://localhost:5004
"""
from flask import Flask, jsonify, render_template, request

from llm import LLMError, status
from modules import (explanation_module, feedback_module, input_module, intent_module, preference_module,
                     profile_module, prompt_module, ranking_module, save_module)
from modules.recommendation_module import Recommender

app = Flask(__name__)
rec = Recommender()


@app.errorhandler(LLMError)
def llm_error(e):
    return jsonify(error=str(e)), 503


@app.errorhandler(ValueError)
def bad_input(e):
    return jsonify(error=str(e)), 400


def run_pipeline(profile, pref, feedback=""):
    """Candidates -> Prompt -> LLM picks -> Ranking -> Explanations"""
    cands = rec.candidates(profile, pref)
    prompt = prompt_module.build(profile, pref, cands, feedback)
    picks = rec.recommend(prompt, cands, profile["n_items"])
    ranked = ranking_module.rank(picks, profile, pref)
    expl = explanation_module.explain(ranked, profile)
    for r in ranked:
        r["explanation"] = expl[r["item_id"]]
    return {"candidates": cands, "prompt": prompt, "picks": picks, "ranked": ranked}


@app.get("/")
def home():
    return render_template("index.html", exp_no=4, title="PathFinder AI – Personalized Recommendations",
                           levels=input_module.LEVELS, categories=input_module.CATEGORIES,
                           n_items=len(rec.df), method=rec.index.method)


@app.get("/api/status")
def api_status():
    return jsonify(status())


@app.post("/api/analyze")
def api_analyze():
    """Input -> Profile -> Preference analysis -> Prompt"""
    profile = profile_module.build(input_module.collect(request.get_json()))
    pref = preference_module.analyze(profile)
    cands = rec.candidates(profile, pref)
    return jsonify(profile=profile, pref=pref, candidates=cands, prompt=prompt_module.build(profile, pref, cands))


@app.post("/api/recommend")
def api_recommend():
    d = request.get_json()
    picks = rec.recommend(d["prompt"], d["candidates"], d["profile"]["n_items"])
    ranked = ranking_module.rank(picks, d["profile"], d["pref"])
    return jsonify(picks=picks, ranked=ranked)


@app.post("/api/explain")
def api_explain():
    d = request.get_json()
    return jsonify(explanations=explanation_module.explain(d["ranked"], d["profile"]))


@app.post("/api/feedback")
def api_feedback():
    d = request.get_json()
    text = (d.get("text") or "").strip()
    if not text:
        raise ValueError("Type your feedback first.")
    intent = intent_module.detect(text)
    out = {"intent": intent}
    if intent["intent"] == "REFINE":
        profile, pref, changes = feedback_module.apply(d["profile"], d["pref"], text)
        out.update(profile=profile, pref=pref, changes=changes, **run_pipeline(profile, pref, text))
    elif intent["intent"] == "EXPLAIN":
        out["explanations"] = explanation_module.explain(d["ranked"], d["profile"])
    elif intent["intent"] == "SAVE":
        out["saved"] = save_module.save(d["profile"], d["ranked"])
    return jsonify(out)


@app.post("/api/save")
def api_save():
    d = request.get_json()
    return jsonify(save_module.save(d["profile"], d["ranked"]))


if __name__ == "__main__":
    app.run(port=5004, debug=False)
