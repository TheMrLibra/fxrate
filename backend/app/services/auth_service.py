from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.domain.schemas.auth import UserCreate, UserRead, LoginRequest, Token
from app.core.security import (
    authenticate_user,
    create_access_token,
    get_user_by_username,
    get_user_by_email
)
from app.core.config import settings


class AuthService:
    def __init__(self, repository: UserRepository, db: Session):
        self.repository = repository
        self.db = db
    
    def register(self, user_data: UserCreate) -> UserRead:
        """Register a new user."""
        # Check if username already exists
        if self.repository.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        if self.repository.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        user = self.repository.create(user_data)
        return UserRead.model_validate(user)
    
    def login(self, login_data: LoginRequest) -> Token:
        """Authenticate user and return JWT token."""
        user = authenticate_user(self.db, login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")

