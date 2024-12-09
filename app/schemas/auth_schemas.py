from pydantic import BaseModel

class user_sign_up(BaseModel):
    name:str
    email:str
    password:str
    avatar:str

class message(BaseModel):
    message:str

class user_log_in(BaseModel):
    email:str
    password:str
    
class Token(BaseModel):
    access_token:str 
    token_type:str           