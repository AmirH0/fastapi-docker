from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    display_name: str 
    
    
    
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    display_name: str 
    is_admin: bool = False

    class Config:
         from_attributes = True