from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from uuid import UUID
from backend.services.auth_service import (
    register_user,
    authenticate_user,
    create_access_token,
    get_current_user
)
from database.config import get_db
from database.models import User

router = APIRouter(prefix="/auth")

# Pydantic schemas
class RegisterRequest(BaseModel):
    email: str = Field(..., example="user@example.com")
    password: str = Field(..., example="securepassword")

class LoginRequest(BaseModel):
    email: str = Field(..., example="user@example.com")
    password: str = Field(..., example="securepassword")

class UserResponse(BaseModel):
    id: UUID
    email: str

# Route: POST /register
@router.post("/register", operation_id="register", status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    user = await register_user(db, email=request.email, password=request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User registration failed"
        )
    return {"message": "User registered successfully"}

# Route: POST /login
@router.post("/login", operation_id="login", status_code=status.HTTP_200_OK)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = await authenticate_user(db, email=request.email, password=request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# Route: GET /me
@router.get("/me", operation_id="getCurrentUser", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResponse(id=current_user.id, email=current_user.email)