from typing import Annotated
from app.models.auth_models import User
from fastapi import Depends
from app.services.auth_services import get_current_user

user_dependancy=Annotated[dict,Depends(get_current_user)]   