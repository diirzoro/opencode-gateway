from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..services.accounts import user_payload
from .dependencies import require_admin
router = APIRouter(prefix="/api/admin", tags=["admin"])
@router.get("/users")
def users(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return [user_payload(u) for u in db.scalars(select(User).order_by(User.created_at.desc()))]
