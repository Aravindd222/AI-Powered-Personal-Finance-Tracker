import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load dataset
df = pd.read_csv("category_dataset.csv")

X = df["text"]
y = df["category"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# TF-IDF
tfidf = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 3),
    stop_words="english",
    min_df=2,
    max_df=0.9
)

X_train_vec = tfidf.fit_transform(X_train)
X_test_vec = tfidf.transform(X_test)

# Classifier
model = LogisticRegression(max_iter=2000, class_weight="balanced")
#model = LinearSVC(class_weight="balanced")
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)

print("Classification Report:\n")
print(classification_report(y_test, y_pred))

# Save models
joblib.dump(tfidf, "tfidf.pkl")
joblib.dump(model, "category_model.pkl")

print("✅ Category model trained and saved")
