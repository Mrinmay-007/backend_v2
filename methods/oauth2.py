#oauth2.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from methods import token

oauth2_scheme_student = OAuth2PasswordBearer(tokenUrl="login_student")
oauth2_scheme_faculty = OAuth2PasswordBearer(tokenUrl="login_faculty")
oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="login_admin")
# oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="login_admin")

def get_current_student(data: str = Depends(oauth2_scheme_student)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return token.verify_token(data, credentials_exception)

def get_current_faculty(data: str = Depends(oauth2_scheme_faculty)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return token.verify_token(data, credentials_exception)

def get_current_admin(data: str = Depends(oauth2_scheme_admin)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return token.verify_token(data, credentials_exception)
