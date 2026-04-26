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

(https://drive.google.com/file/d/1TltZH6wGOWzaINEws1TM2zBwZT-xAG9T/view?usp=sharing)<img width="1602" height="81" alt="image" src="https://github.com/user-attachments/assets/050b99af-3480-4270-b8ae-c3c0818e47e3" />


---

## 🔗 Live API

(https://ai-guardian-g5bz.onrender.com/docs)<img width="774" height="81" alt="image" src="https://github.com/user-attachments/assets/d08eab2f-5948-44cc-829a-379b6cab4b74" />


---

## ⚠️ Security

API keys are securely stored using environment variables (.env) and are not exposed in the codebase.

---

## 👨‍💻 Author

Shubham Kumar

---

## 💡 Vision

To protect users from digital fraud using real-time, explainable AI systems.
