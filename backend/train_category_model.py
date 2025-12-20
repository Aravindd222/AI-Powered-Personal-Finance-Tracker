import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# Load dataset
df = pd.read_csv("category_dataset.csv")

X = df["text"]
y = df["category"]

# TF-IDF
tfidf = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    stop_words="english"
)

X_vec = tfidf.fit_transform(X)

# Classifier
model = LinearSVC()
model.fit(X_vec, y)

# Save models
joblib.dump(tfidf, "tfidf.pkl")
joblib.dump(model, "category_model.pkl")

print("✅ Category model trained and saved")
