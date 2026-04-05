from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, Token
from auth import hash_password, create_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=UserResponse)

def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    else:
        hashed_password = hash_password(user.password)
        new_user = User(username=user.username, password=hashed_password, is_admin=False)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserResponse(id=new_user.id, username=new_user.username, is_admin=new_user.is_admin)