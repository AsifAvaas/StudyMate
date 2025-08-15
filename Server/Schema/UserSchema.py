from pydantic import BaseModel,EmailStr,field_validator
import re

class UserBase(BaseModel):
    username:str
    email: EmailStr
    password:str
    address:str
    @field_validator("password")
    def validate_password(cls,value):
        if len(value)<8:
            raise ValueError("Password must be 8 charecters long.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")
        return value

class LoginUserBase(BaseModel):
    credential:str
    password:str

class UpdateUserBase(BaseModel):
    username:str
    address:str

class UpdateUserPassword(BaseModel):
    old_password:str
    new_password:str    
    @field_validator("new_password")
    def validate_password(cls,value):
        if len(value)<8:
            raise ValueError("Password must be 8 charecters long.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")
        return value
