# from ocr_engine import extract_ocr_blocks
# from parser_ml import extract_amount_strict, detect_category_ml,extract_date

# IMAGE = "snookers.png"

# blocks = extract_ocr_blocks(IMAGE)

# amount = extract_amount_strict(blocks)
# category = detect_category_ml(blocks)

# print("FINAL AMOUNT:", amount)
# print("CATEGORY:", category["category"])
# print("SUB CATEGORY:", category["subcategory"])
# print("DATE:", extract_date(blocks))

# main.py
from fastapi import FastAPI
from database import Base, engine

from auth.auth_router import router as auth_router
from expenses.expenses_router import router as expenses_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Finance Tracker")

app.include_router(auth_router)
app.include_router(expenses_router)
