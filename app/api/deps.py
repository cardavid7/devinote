
from typing import Annotated, Iterator
from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.db import get_session
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

#def get_db() -> Session:
#    return next(get_session())
def get_db() -> Iterator[Session]:
    yield from get_session()

# db: Session = Depends(get_db) -> db: DBSession
DBSession = Annotated[Session, Depends(get_db)]


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DBSession) -> User:
    
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))

    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user

# current_user : User = Depends(get_current_user)
CurrentUser = Annotated[User, Depends(get_current_user)]