from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

import database.db_models as db_models
import models.schemas as schemas
from database.db_connect import get_db
from services.auth import get_current_admin, get_password_hash


router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/", response_model=schemas.User)
@limiter.limit("100/second")
async def create_user(
    request: Request,
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_admin)
):
    db_user = db.query(db_models.User).filter(db_models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = db_models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[schemas.User])
@limiter.limit("100/second")
async def get_users(
    request: Request,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_admin)
):
    return db.query(db_models.User).all()