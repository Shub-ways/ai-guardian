# 🛡️ AI Guardian – AI-Powered Fraud Detection System

AI Guardian is a multi-modal AI system that detects phishing links and scam messages using Machine Learning, rule-based security logic, and Google Gemini.

---

## 🚀 Features

* 🔍 URL Phishing Detection (ML + Rule-Based Engine)
* 💬 Scam Message Detection (Google Gemini)
* 🧠 Unified AI Decision System (`/analyze`)
* 📊 Risk Score + Confidence Level
* 🧾 Explainable AI (Reasons + Breakdown)
* ⚠️ False Negative Prevention (Override Logic)

---

## 🧠 Tech Stack

* FastAPI (Backend)
* Scikit-learn (Random Forest)
* Google Gemini 1.5 Flash (LLM)
* Python

---

## 📡 API Endpoints

| Endpoint        | Description                     |
| --------------- | ------------------------------- |
| `/analyze-url`  | Analyze phishing URLs           |
| `/analyze-text` | Analyze scam messages           |
| `/analyze`      | Unified analysis (BEST FEATURE) |

---

## 🧪 Example

```json
{
  "url": "http://secure-login-update.xyz",
  "text": "Verify your account immediately"
}
```

---

## 🎯 Output

* Risk Score
* Verdict (Safe / Suspicious / Scam)
* Confidence
* Reasons (Explainable AI)

---

## 🎥 Demo Video

(Add your demo video link here)

---

## 🔗 Live API

(Add your deployment link or /docs link)

---

## ⚠️ Security

API keys are securely stored using environment variables (.env) and are not exposed in the codebase.

---

## 👨‍💻 Author

Shubham Kumar

---

## 💡 Vision

To protect users from digital fraud using real-time, explainable AI systems.
