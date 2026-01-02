from pydantic import BaseModel, EmailStr, Field

#for EmailStr we must install email-validator package

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length =72)

class Token(BaseModel):
    access_token: str
    token_type: str
