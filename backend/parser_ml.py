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
    "total"

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
    "total due",

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


def normalize_money(token: str):
    token = token.strip()

    # convert comma decimal to dot decimal
    if re.fullmatch(r"\d+,\d{2}", token):
        token = token.replace(",", ".")

    # remove thousand separators like 1,000
    if re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d{1,2})?", token):
        token = token.replace(",", "")

    return token

def _is_valid_money(token: str) -> bool:
    """
    Strict money validation:
    - numeric only
    - optional decimal
    - realistic range
    """
    token = normalize_money(token)

    if not re.fullmatch(r"\d+(\.\d{1,2})?", token):
        return False

    value = float(token)

    # realistic bill range (adjust if needed)
    if value < 1 or value > 100000:
        return False

    return True
def extract_amount_strict(ocr_blocks):
    """
    Extracts final payable amount from OCR blocks.
    Strategy:
    1. First look for strong priority keywords (Amount Paid, Net Payable, etc.)
    2. If not found, detect summary section and take the largest valid amount there
    3. Ignore line-item totals in middle columns
    """

    PRIORITY_KEYWORDS = [
        "amount paid",
        "net payable",
        "grand total",
        "final total",
        "amount due",
        "balance due",
        "total due"
    ]

    SUMMARY_START_KEYWORDS = [
        "total qty",
        "payment mode",
        "discount",
        "tax",
        "advance"
    ]

    def extract_money_from_block(block):
        values = []
        tokens = block["text"].split()

        for t in tokens:
            normalized = normalize_money(t)
            if _is_valid_money(normalized):
                values.append(float(normalized))

        return values

    # --------------------------------------------------
    # STEP 1 — PRIORITY KEYWORDS (Most Reliable)
    # --------------------------------------------------
    for i, block in enumerate(ocr_blocks):
        text = block["text"].lower()

        if any(k in text for k in PRIORITY_KEYWORDS):

            # Check same line
            values = extract_money_from_block(block)
            if values:
                return {"amount": max(values)}

            # Check next line
            if i + 1 < len(ocr_blocks):
                next_values = extract_money_from_block(ocr_blocks[i + 1])
                if next_values:
                    return {"amount": max(next_values)}

    # --------------------------------------------------
    # STEP 2 — SUMMARY SECTION DETECTION
    # --------------------------------------------------
    summary_mode = False
    summary_values = []

    for block in ocr_blocks:
        text = block["text"].lower()

        # Detect start of summary zone
        if any(k in text for k in SUMMARY_START_KEYWORDS):
            summary_mode = True

        if summary_mode:
            values = extract_money_from_block(block)
            summary_values.extend(values)

    if summary_values:
        return {"amount": max(summary_values)}

    # --------------------------------------------------
    # STEP 3 — SAFE FALLBACK (If nothing detected)
    # --------------------------------------------------
    all_values = []
    for block in ocr_blocks:
        values = extract_money_from_block(block)
        all_values.extend(values)

    if all_values:
        return {"amount": max(all_values)}

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

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)  # remove numbers
    text = re.sub(r'[^\w\s]', '', text)  # remove symbols
    return text

def rule_based_category(text):
    text = text.lower()

    # Merchant-based rules
    if any(word in text for word in ["zomato", "swiggy", "restaurant", "hotel", "cafe", "pizza", "burger"]):
        return {"category": "Food", "subcategory": "Dining"}

    if any(word in text for word in ["supermarket", "mart", "grocery", "store", "hypermarket"]):
        return {"category": "Groceries", "subcategory": "Supermarket"}

    if any(word in text for word in ["uber", "ola", "petrol", "diesel", "bus", "train", "metro"]):
        return {"category": "Transport", "subcategory": "Travel"}

    if any(word in text for word in ["electricity", "water bill", "gas", "wifi", "broadband", "recharge"]):
        return {"category": "Utilities", "subcategory": "Bills"}

    if any(word in text for word in ["amazon", "flipkart", "mall", "clothing", "electronics"]):
        return {"category": "Shopping", "subcategory": "Retail"}

    if any(word in text for word in ["netflix", "spotify", "movie", "cinema", "concert"]):
        return {"category": "Entertainment", "subcategory": "Subscription"}
    
    if any(word in text for word in ["salon", "grooming", "massage", "barber", "spa"]):
        return {"category": "Services", "subcategory": "Salon"}

    return None

def detect_category_ml(ocr_blocks):
    text = " ".join(b["text"] for b in ocr_blocks).lower()
    cleaned = clean_text(text)

    #step 1 - try rule based
    rule_result = rule_based_category(cleaned)
    if rule_result:
        return rule_result
    
    #step 2 - ML model
    X = tfidf.transform([cleaned])
    category = category_model.predict(X)[0]

    # ML-INFLUENTIAL WORDS
    keywords = get_top_contributing_words(text)

    # SUBCATEGORY = strongest keyword just for demonstration
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

    # Clean OCR noise
    text = text.replace("O", "0")
    text = text.replace("o", "0")

    pattern = r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b"
    match = re.search(pattern, text)

    if not match:
        return None

    raw_date = match.group()

    # Normalize all separators to /
    normalized = re.sub(r"[.-]", "/", raw_date)

    try:
        parsed = datetime.strptime(normalized, "%d/%m/%Y")
        return parsed.date().isoformat()
    except ValueError:
        try:
            parsed = datetime.strptime(normalized, "%d/%m/%y")
            return parsed.date().isoformat()
        except ValueError:
            return None

