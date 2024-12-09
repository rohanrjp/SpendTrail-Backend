from pydantic import BaseModel

class user_sign_up(BaseModel):
    name:str
    email:str
    password:str
    avatar:str

class message(BaseModel):
    message:str    