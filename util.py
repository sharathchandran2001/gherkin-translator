# main.py
from fastapi import FastAPI, HTTPException
import spacy
import nltk
import json

util = FastAPI()
nlp = spacy.load("en_core_web_sm")

# Load rule-based mappings from JSON
try:
    with open("gherkin_api_mapping.json", "r") as f:
        rule_mappings = json.load(f)
except FileNotFoundError:
    rule_mappings = {}

@app.post("/suggest_api")
async def suggest_api(gherkin_step: str):
    """Suggests an API endpoint for a given Gherkin step."""

    # 1. NLP Approach (Semantic Similarity):
    doc = nlp(gherkin_step)
    keywords = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "VERB"] and not token.is_stop]

    if "credit card" in keywords:
        return {"suggested_api": "url/getCreditCardDetails"}
    elif "account" in keywords:
        if "mortgage" in keywords:
            return {"suggested_api": "url/getMortgageAccountDetails"}
        else:
            return {"suggested_api": "url/getAccountDetails"}

    # 2. Rule-Based Approach (JSON Mapping):
    for keyword, api in rule_mappings.items():
        if keyword.lower() in gherkin_step.lower():
            return {"suggested_api": api}

    # 3. No Match Found:
    raise HTTPException(status_code=404, detail="No matching API found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
