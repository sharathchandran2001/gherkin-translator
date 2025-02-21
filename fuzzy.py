from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import Optional, Dict, Any
from rapidfuzz import process, fuzz

app = FastAPI()

# Load the rule-based mapping from JSON file.
with open("mapping.json", "r") as f:
    rule_based_mapping = json.load(f)

    class GherkinStep(BaseModel):
        step: str

        def match_api_endpoint(step: str, threshold: float = 70) -> Optional[Dict[str, Any]]:
            """
                Uses RapidFuzz to find the best matching keyword in the rule-based mapping.
                    Returns a dictionary with the matched keyword, API endpoint, and score.
                        If no match is found, returns None.
                            """
                                best_match = process.extractOne(step, list(rule_based_mapping.keys()), scorer=fuzz.ratio)
                                    if best_match:
                                            keyword, score, _ = best_match
                                                    return {"keyword": keyword, "api_endpoint": rule_based_mapping.get(keyword), "score": score}
                                                        return None

                                                        @app.post("/translate")
                                                        def translate_gherkin(step: GherkinStep):
                                                            """
                                                                Receives a Gherkin step and attempts to match it to an API endpoint using fuzzy matching.
                                                                    If the best match score is above the threshold, returns that match.
                                                                        Otherwise, returns the closest matching key and value as a fallback.
                                                                            """
                                                                                result = match_api_endpoint(step.step)
                                                                                    if result:
                                                                                            if result["score"] < 70:
                                                                                                        return {
                                                                                                                        "message": "No high-confidence match found; returning closest match as fallback.",
                                                                                                                                        "fallback": result
                                                                                                                                                    }
                                                                                                                                                            else:
                                                                                                                                                                        return result
                                                                                                                                                                            else:
                                                                                                                                                                                    raise HTTPException(status_code=404, detail="No match found and fallback mapping is empty.")

                                                                                                                                                                                    # To run the application, use: uvicorn app:app --reload
                                                                                                                                                                                    