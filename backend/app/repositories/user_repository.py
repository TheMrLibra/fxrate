from sqlalchemy.orm import Session
from typing import Optional

from app.core.models import User
from app.domain.schemas.auth import UserCreate
from app.core.security import get_password_hash


class UserRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_username(self, username: str) -> User:
        return self.session.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> User:
        return self.session.query(User).filter(User.email == email).first()
    
    def get_by_id(self, user_id: int) -> User:
        return self.session.query(User).filter(User.id == user_id).first()
    
    def create(self, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user


