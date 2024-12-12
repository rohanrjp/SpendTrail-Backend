from fastapi import HTTPException,status

Inavlid_credentials_exception=HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"}
)
