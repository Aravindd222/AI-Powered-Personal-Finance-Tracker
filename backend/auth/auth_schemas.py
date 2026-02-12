from pydantic import BaseModel, EmailStr

#for EmailStr we must install email-validator package

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
'''
class Token(BaseModel):
    access_token: str
    token_type: str
'''
#new
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
#new