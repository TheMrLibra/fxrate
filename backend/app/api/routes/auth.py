from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.domain.schemas.auth import LoginRequest
from app.core.security import get_current_active_user
from app.domain.schemas.auth import UserCreate, UserRead, Token
from app.services.auth_service import AuthService
from app.core.models import User
from app.api.dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    """Register a new user."""
    return service.register(user_data)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    """Login and get access token."""
    login_data = LoginRequest(username=form_data.username, password=form_data.password)
    return service.login(login_data)


@router.get("/me", response_model=UserRead)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
):
    """Get current user information."""
    return UserRead.model_validate(current_user)

