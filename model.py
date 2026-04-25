import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# Synthetic Dataset (100 samples)
# -----------------------------
data = []

# Safe URLs (label = 0)
for i in range(50):
    data.append([
        20, 1, 1, 0, 1, 0, 0, 10, 0, 0, 0, 3.2, 0, 0, 0
    ])

# Phishing URLs (label = 1)
for i in range(50):
    data.append([
        80, 0, 5, 1, 5, 3, 1, 30, 3, 1, 1, 4.5, 1, 1, 1
    ])

columns = [
    "url_length", "https", "dots", "ip", "subdomain",
    "hyphen", "at_symbol", "domain_length", "digits",
    "query_params", "port", "entropy", "keywords",
    "credentials", "suspicious"
]

df = pd.DataFrame(data, columns=columns)
df["label"] = [0]*50 + [1]*50

X = df.drop("label", axis=1)
y = df["label"]

# -----------------------------
# Train Model
# -----------------------------
model = RandomForestClassifier(n_estimators=100, max_depth=10)
model.fit(X, y)


# -----------------------------
# Prediction Function
# -----------------------------
def predict_url(features):
    feature_list = list(features.values())

    prediction = model.predict([feature_list])[0]
    probability = model.predict_proba([feature_list])[0][1]

    return prediction, probability