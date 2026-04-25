from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from model import predict_url
from utils import extract_features
from gemini import analyze_text_with_gemini
import json
import re

app = FastAPI()

# -----------------------------
# Constants
# -----------------------------
LOW_ENTROPY = 4.0
HIGH_ENTROPY = 4.5

# -----------------------------
# Request Schemas
# -----------------------------
class URLRequest(BaseModel):
    url: Optional[str] = None

class TextRequest(BaseModel):
    text: Optional[str] = None

class CombinedRequest(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None

# -----------------------------
# Helper Functions
# -----------------------------
def get_confidence(score):
    if score > 70:
        return "High"
    elif score > 40:
        return "Medium"
    return "Low"

# -----------------------------
# Risk Breakdown
# -----------------------------
def calculate_risk_breakdown(features):
    domain_risk = 0
    structure_risk = 0
    security_risk = 0
    behavior_risk = 0

    if features["ip"] == 1:
        domain_risk += 30
    if features["subdomain"] > 3:
        domain_risk += 20

    if features["url_length"] > 60:
        structure_risk += 20
    if features["hyphen"] > 3:
        structure_risk += 10

    if features["credentials"] == 1:
        security_risk += 30
    if features["port"] == 1:
        security_risk += 15
    if features["https"] == 0:
        security_risk += 15

    if features["entropy"] > HIGH_ENTROPY:
        behavior_risk += 25
    elif features["entropy"] > LOW_ENTROPY:
        behavior_risk += 15

    if features["keywords"] == 1:
        behavior_risk += 20

    return {
        "domain_risk": domain_risk,
        "structure_risk": structure_risk,
        "security_risk": security_risk,
        "behavior_risk": behavior_risk
    }

# -----------------------------
# Explainability
# -----------------------------
def generate_reasons(features):
    reasons = []

    if features["ip"] == 1:
        reasons.append("IP address used instead of domain")

    if features["subdomain"] > 3:
        reasons.append("Too many subdomains (possible spoofing)")

    if features["url_length"] > 60:
        reasons.append("Unusually long URL")

    if features["entropy"] > HIGH_ENTROPY:
        reasons.append("Highly obfuscated URL (random structure detected)")
    elif features["entropy"] > LOW_ENTROPY:
        reasons.append("Moderately complex URL structure (possible obfuscation)")

    if features["keywords"] == 1:
        reasons.append("Suspicious keywords detected (login/verify/etc)")

    if features["credentials"] == 1:
        reasons.append("Contains embedded credentials (@ symbol)")

    if features["port"] == 1:
        reasons.append("Non-standard port used")

    if features["https"] == 0:
        reasons.append("Not using HTTPS (insecure connection)")

    return reasons

# -----------------------------
# URL Processing
# -----------------------------
def process_url(url):
    if not url:
        raise HTTPException(status_code=400, detail="Please provide a valid 'url'")

    features = extract_features(url)

    prediction, probability = predict_url(features)
    ml_score = int(probability * 100)

    risk_breakdown = calculate_risk_breakdown(features)
    rule_score = min(sum(risk_breakdown.values()), 100)

    risk_score = int((ml_score * 0.4) + (rule_score * 0.6))

    if features["keywords"] == 1 and features["entropy"] > HIGH_ENTROPY:
        risk_score += 10

    # Safety floor
    if features["keywords"] == 1 and features["https"] == 0:
        risk_score = max(risk_score, 45)

    risk_score = max(0, min(risk_score, 100))

    override_applied = False
    override_reason = None

    if (
        features["keywords"] == 1 and
        features["entropy"] > HIGH_ENTROPY and
        features["https"] == 0
    ):
        override_applied = True
        override_reason = "High-risk phishing pattern detected (keywords + strong obfuscation + insecure connection)"

    if risk_score > 70 or override_applied:
        verdict = "Scam"
    elif risk_score > 40:
        verdict = "Suspicious"
    else:
        verdict = "Safe"

    reasons = generate_reasons(features)

    if override_applied:
        reasons.append("Escalated to Scam due to combined high-risk indicators")

    return {
        "risk_score": risk_score,
        "verdict": verdict,
        "confidence": get_confidence(risk_score),
        "reasons": reasons,
        "override_reason": override_reason,
        "override_applied": override_applied,
        "risk_breakdown": risk_breakdown,
        "features": features
    }

# -----------------------------
# Text Processing
# -----------------------------
def process_text(text):
    if not text:
        raise HTTPException(status_code=400, detail="Please provide 'text' input")

    raw_response = analyze_text_with_gemini(text)

    try:
        match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            raise ValueError
    except:
        result = {
            "verdict": "Suspicious",
            "risk_score": 50,
            "reasons": ["AI response parsing failed"]
        }

    result["confidence"] = get_confidence(result["risk_score"])
    return result

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def home():
    return {"message": "AI Guardian Backend Running 🚀"}

@app.post("/analyze-url")
def analyze_url(request: URLRequest):
    return process_url(request.url)

@app.post("/analyze-text")
def analyze_text(request: TextRequest):
    return process_text(request.text)

@app.post("/analyze")
def analyze_combined(request: CombinedRequest):

    if not request.url and not request.text:
        raise HTTPException(status_code=400, detail="Provide at least URL or text")

    results = {}
    scores = []
    reasons = []

    if request.url:
        url_res = process_url(request.url)
        results["url_analysis"] = url_res
        scores.append(url_res["risk_score"])
        reasons.extend(url_res["reasons"])

    if request.text:
        text_res = process_text(request.text)
        results["text_analysis"] = text_res
        scores.append(text_res["risk_score"])
        reasons.extend(text_res["reasons"])

    final_score = int(sum(scores) / len(scores))

    if final_score > 70:
        final_verdict = "Scam"
    elif final_score > 40:
        final_verdict = "Suspicious"
    else:
        final_verdict = "Safe"

    return {
        "final_score": final_score,
        "final_verdict": final_verdict,
        "confidence": get_confidence(final_score),
        "combined_reasons": list(set(reasons)),
        "sources": results
    }