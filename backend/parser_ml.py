import re
import joblib

import numpy as np
from datetime import datetime

tfidf = joblib.load("tfidf.pkl")
category_model = joblib.load("category_model.pkl")


PRIMARY_KEYWORDS = [
    # strongest indicators
    "final amount",
    "net payable",
    "total payable",
    "amount payable",

    # final totals
    "grand total",
    "final total",
    "net total",
    "overall total",

    # invoices
    "invoice total",
    "invoice amount",

    # settlement
    "amount due",
    "balance due",
    "outstanding balance",

    # explicit totals
    "bill total",
    "total amount"
]

SECONDARY_KEYWORDS = [
    # generic amount words
    "amount",
    "gross amount",
    "net amount",
    "bill amount",
    "total value",
    "bill value",
    "net value",

    # payments (often misleading)
    "payment",
    "payment amount",
    "payment due",
    "paid",
    "amount paid",
    "total paid",

    # balances (ambiguous)
    "balance",
    "outstanding",

    # POS / payment modes (NOT totals)
    "cash",
    "cash paid",
    "cash amount",
    "card",
    "card payment",
    "credit",
    "credit card",
    "debit",
    "debit card",
    "upi",
    "upi payment",
    "online payment",

    # abbreviations
    "amt",
    "tot amt",
    "bal",
    "net amt",
    "pay amt",

    # currency variants
    "total rs",
    "amount rs",
    "rs total",
    "rs amount",
    "inr total",
    "inr amount"
]



def _is_valid_money(token: str) -> bool:
    """
    Strict money validation:
    - numeric only
    - optional decimal
    - realistic range
    """
    token = token.replace(",", "").strip()

    if not re.fullmatch(r"\d+(\.\d{1,2})?", token):
        return False

    value = float(token)

    # realistic bill range (adjust if needed)
    if value < 1 or value > 100000:
        return False

    return True

def extract_amount_strict(ocr_blocks):
    primary_candidates = []
    secondary_candidates = []

    n = len(ocr_blocks)

    for i, block in enumerate(ocr_blocks):
        text = block["text"].lower()
        tokens = block["text"].replace(",", "").split()

        # ---------- PRIMARY KEYWORDS ----------
        if any(k in text for k in PRIMARY_KEYWORDS):

            # SAME LINE
            for t in tokens:
                if _is_valid_money(t):
                    primary_candidates.append(float(t))

            # NEXT LINE (CRITICAL FIX)
            if i + 1 < n:
                next_tokens = ocr_blocks[i + 1]["text"].replace(",", "").split()
                for t in next_tokens:
                    if _is_valid_money(t):
                        primary_candidates.append(float(t))

        # ---------- SECONDARY KEYWORDS ----------
        elif any(k in text for k in SECONDARY_KEYWORDS):

            # SAME LINE
            for t in tokens:
                if _is_valid_money(t):
                    secondary_candidates.append(float(t))

            # NEXT LINE
            if i + 1 < n:
                next_tokens = ocr_blocks[i + 1]["text"].replace(",", "").split()
                for t in next_tokens:
                    if _is_valid_money(t):
                        secondary_candidates.append(float(t))

    # ---------- FINAL DECISION ----------
    if primary_candidates:
        return {"amount": max(primary_candidates)}

    if secondary_candidates:
        return {"amount": max(secondary_candidates)}

    return {"amount": None}





category_model = joblib.load("category_model.pkl")
tfidf = joblib.load("tfidf.pkl")



def get_top_contributing_words(text, top_n=5):
    """
    Returns the most influential words used by the ML model
    for the predicted category.
    """
    X = tfidf.transform([text])
    feature_names = tfidf.get_feature_names_out()

    # Get predicted class index
    class_index = category_model.predict(X)[0]
    class_id = list(category_model.classes_).index(class_index)

    # Get weights for that class
    coef = category_model.coef_[class_id]

    # Contribution = tfidf_value * weight
    contributions = X.toarray()[0] * coef

    top_indices = np.argsort(contributions)[-top_n:][::-1]

    keywords = [feature_names[i] for i in top_indices if contributions[i] > 0]

    return keywords


def detect_category_ml(ocr_blocks):
    text = " ".join(b["text"] for b in ocr_blocks).lower()

    X = tfidf.transform([text])
    category = category_model.predict(X)[0]

        # ML-INFLUENTIAL WORDS
    keywords = get_top_contributing_words(text)

    # SUBCATEGORY = strongest keyword
    subcategory = keywords[0] if keywords else "unknown"

    return {
        "category": category,
        "subcategory": subcategory,
        "keywords": keywords
    }


DATE_PATTERNS = [
    r"\b\d{2}/\d{2}/\d{2}\b",       # 20/12/25
    r"\b\d{2}/\d{2}/\d{4}\b",       # 20/12/2025
    r"\b\d{2}-\d{2}-\d{4}\b",       # 20-12-2025
    r"\b\d{2}\.\d{2}\.\d{4}\b",     # 20.12.2025
    r"\b\d{1,2}-[A-Za-z]{3}-\d{4}\b",     # 12-Apr-2025
    r"\b\d{1,2}-[A-Za-z]{3}-\d{2}\b",     # 12-Apr-25
    r"\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}\b",  # 12 March 2020
    r"\b[A-Za-z]{3,9}\s+\d{1,2},\s*\d{4}\b"  # April 12, 2025
]

def extract_date(ocr_blocks):
    text = " ".join(b["text"] for b in ocr_blocks)

    for pattern in DATE_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            continue

        raw_date = match.group()

        formats = [
            "%d/%m/%y",
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%d.%m.%Y",

            "%d-%b-%Y",   # 12-Apr-2025
            "%d-%b-%y",   # 12-Apr-25
            "%d %B %Y",   # 12 March 2020
            "%B %d, %Y",  # April 12, 2025
            "%b %d, %Y",  # Apr 12, 2025
        ]

        for fmt in formats:
            try:
                parsed = datetime.strptime(raw_date, fmt)
                return parsed.date().isoformat()  # YYYY-MM-DD
            except ValueError:
                pass

    return None
