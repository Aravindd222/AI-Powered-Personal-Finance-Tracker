from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from database import get_db
from models import User
from auth.auth_schemas import UserCreate, Token

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "SECRET"
ALGORITHM = "HS256"

@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    hashed = pwd_context.hash(data.password)
    user = User(
        email=data.email,
        hashed_password=hashed,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created"}



@router.post("/login", response_model=Token)
def login(data: UserCreate, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()
    if not user or not pwd_context.verify(data.password, user.hashed_password):
        return {"error": "Invalid credentials"}

    token = jwt.encode({"sub": str(user.id)}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
