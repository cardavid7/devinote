from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.models.user import User, UserCreate
from fastapi import HTTPException, status

class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, user: UserCreate) -> User:
        if self.repo.get_by_email(user.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        
        user = User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=hash_password(user.password[:72])
        )
        
        return self.repo.create(user)
    
    def login(self, email : str, password : str) -> str:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password[:72], user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = create_access_token({"sub": str(user.id)})
        return token