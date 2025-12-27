# AI-Powered Personal Finance Tracker

An intelligent finance tracking system that allows users to record expenses manually or automatically from bills/receipts using OCR and Machine Learning.  
The system categorizes expenses, extracts structured data from receipts, provides monthly insights, visualizations, and predicts future spending patterns.

---

##  Features

###  Expense Entry (Two Modes)
- **Manual Entry**
  - Amount
  - Category
  - Subcategory
  - Date
- **Receipt / Bill Upload**
  - OCR-based text extraction
  - Strict final amount detection
  - Automatic category & subcategory classification

---

###  AI-Powered Receipt Processing
- Optical Character Recognition using **EasyOCR**
- Rule-based + keyword-priority final amount extraction
- Handles noisy real-world receipts (food, fuel, utilities, shopping)
- Ignores GST numbers, invoice IDs, phone numbers, and item prices

---

###  Intelligent Category Detection (ML)
- Text classification using **TF-IDF + LinearSVC**
- Categories:
  - Food
  - Transport
  - Shopping
  - Utilities
  - Entertainment
- Model explainability:
  - Extracts **top contributing words**
  - Uses them to infer **subcategory** (e.g., pizza, petrol, gas, broadband)

---

###  Monthly Expense Analytics
- PostgreSQL database for persistent storage
- Monthly aggregation of expenses
- Category-wise spending breakdown
- Visual dashboards (charts & summaries)

---

###  Future Expense Prediction
- Predicts next month’s spending based on historical data
- Uses time-series/statistical forecasting (baseline ML approach)
- Helps users plan and control expenses proactively

---

##  Tech Stack

### Frontend
- React
- Chart.js / Recharts

### Backend
- FastAPI
- Python

### Machine Learning
- EasyOCR (receipt text extraction)
- TF-IDF Vectorizer
- LinearSVC (text classification)
- Explainable ML (feature contribution analysis)

### Database
- PostgreSQL

---

##  Project Architecture

