import re
import math
from urllib.parse import urlparse


# -----------------------------
# Entropy Calculation
# -----------------------------
def calculate_entropy(url):
    prob = [float(url.count(c)) / len(url) for c in set(url)]
    return -sum([p * math.log2(p) for p in prob])


# -----------------------------
# Feature Helpers
# -----------------------------
def has_ip(url):
    return 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0


def has_suspicious_keywords(url):
    keywords = ["login", "verify", "secure", "account", "update", "bank", "free"]
    return 1 if any(word in url.lower() for word in keywords) else 0


def has_credentials(url):
    return 1 if "@" in url else 0


# -----------------------------
# Main Feature Extraction
# -----------------------------
def extract_features(url):
    parsed = urlparse(url)

    features = {
        "url_length": len(url),
        "https": 1 if parsed.scheme == "https" else 0,
        "dots": url.count("."),
        "ip": has_ip(url),
        "subdomain": parsed.netloc.count("."),
        "hyphen": url.count("-"),
        "at_symbol": 1 if "@" in url else 0,
        "domain_length": len(parsed.netloc),
        "digits": sum(c.isdigit() for c in url),
        "query_params": len(parsed.query.split("&")) if parsed.query else 0,
        "port": 1 if ":" in parsed.netloc else 0,
        "entropy": calculate_entropy(url),
        "keywords": has_suspicious_keywords(url),
        "credentials": has_credentials(url),
        "suspicious": 1 if "free" in url.lower() else 0
    }

    return features