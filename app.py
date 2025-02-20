from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import Optional
from rapidfuzz import process, fuzz

app = FastAPI()

# Load the rule-based mapping from JSON file.
with open("mapping.json", "r") as f:
    rule_based_mapping = json.load(f)

    class GherkinStep(BaseModel):
        step: str

        def match_api_endpoint(step: str, threshold: float = 70) -> Optional[str]:
            """
                Uses RapidFuzz to find the best matching keyword in the rule-based mapping.
                    Returns the corresponding API endpoint if the best match score exceeds the threshold.
                        """
                            # Get best match among mapping keys using fuzzy matching
                                best_match = process.extractOne(
                                        step, list(rule_based_mapping.keys()), scorer=fuzz.ratio
                                            )
                                                if best_match:
                                                        keyword, score, _ = best_match
                                                                if score >= threshold:
                                                                            return rule_based_mapping.get(keyword)
                                                                                return None

                                                                                @app.post("/translate")
                                                                                def translate_gherkin(step: GherkinStep):
                                                                                    """
                                                                                        Receives a Gherkin step and attempts to match it to an API endpoint using fuzzy matching.
                                                                                            If a match is found, returns the endpoint and HTTP method.
                                                                                                Otherwise, returns a message along with the full rule-based mapping.
                                                                                                    """
                                                                                                        matched_endpoint = match_api_endpoint(step.step)
                                                                                                            if matched_endpoint:
                                                                                                                    return {
                                                                                                                                "api_endpoint": matched_endpoint,
                                                                                                                                            "method": "GET"
                                                                                                                                                    }
                                                                                                                                                        else:
                                                                                                                                                                return {
                                                                                                                                                                            "message": "No direct match found. Using fallback rule-based mapping.",
                                                                                                                                                                                        "mapping": rule_based_mapping
                                                                                                                                                                                                }

                                                                                                                                                                                                # For running: uvicorn app:app --reload
                                                                                                                                                                                                