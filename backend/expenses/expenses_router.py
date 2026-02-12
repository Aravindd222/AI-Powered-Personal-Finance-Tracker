# expenses/expenses_router.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy.sql import func

from database import get_db
from models import Expense
from expenses.expenses_schema import ManualExpenseCreate, ExpenseResponse
from auth.auth_router import get_current_user

from ocr_engine import extract_ocr_blocks
from parser_ml import extract_amount_strict, detect_category_ml,extract_date

router = APIRouter(prefix="/expenses", tags=["Expenses"])

#expenses endpoints 

@router.post("/manual", response_model=ExpenseResponse)
def add_manual_expense(
    data: ManualExpenseCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    expense = Expense(
        user_id=user.id,
        amount=data.amount,
        category=data.category,
        date=data.date,
        source="manual"
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


@router.post("/ocr", response_model=ExpenseResponse)
def add_ocr_expense(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    image_bytes = file.file.read()
    blocks = extract_ocr_blocks(image_bytes)
    print("OCR BLOCKS:", blocks)

    amount_data = extract_amount_strict(blocks)
    if not amount_data["amount"]:
        raise HTTPException(status_code=400, detail="Amount not detected")

    category_data = detect_category_ml(blocks)
    date = extract_date(blocks)
    print("DETECTED DATE:", date)

    if not date:
        raise HTTPException(status_code=400, detail="Date not detected")

    expense = Expense(
        user_id=user.id,
        amount=amount_data["amount"],
        category=category_data["category"],
        subcategory=category_data["subcategory"],
        date=date,
        source="ocr",
        raw_text=" ".join(b["text"] for b in blocks),
        confidence=0.95
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense

@router.get("/monthly-summary")
def monthly_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = db.query(
        Expense.category,
        func.sum(Expense.amount).label("total")
    ).filter(Expense.user_id == user.id).group_by(Expense.category).all()

    return {"data": [{"category": r.category, "total": float(r.total)} for r in rows]}


