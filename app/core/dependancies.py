from fastapi import Depends
from app.core.db import Session_Local
from sqlalchemy.orm import Session
from typing import Annotated

def get_db():
    db=Session_Local()
    try:
        yield db 
    finally:
        db.close()  

db_dependancy=Annotated[Session,Depends(get_db)]        