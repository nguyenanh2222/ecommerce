import secrets
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from starlette import status
from orm.models import Permission
from database import SessionLocal

router = APIRouter()
security = HTTPBasic()


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    session: Session = SessionLocal()
    query = session.query(Permission).filter(
        Permission.username.like(f"%{credentials.username}%"
                                 )).filter(
        Permission.password.like(f"{credentials.password}")
    ).scalar()
    print(credentials.username)
    if query is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},

        )
    return credentials.username


# @router.get(
#     "/permission"
# )
# def read_current_user(username: str = Depends(get_current_user)):
#     return {"username": username}
