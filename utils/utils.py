from sqlalchemy.orm import Session
from database.models import User
from database.database import engine, SessionLocal


def user_exists(user_id: int) -> bool:
    db = SessionLocal()
    try:
        exists = db.query(User).filter(User.id == user_id).first() is not None
        return exists
    finally:
        db.close()

def add_user(user_id: int, first_name: str, last_name: str | None, username: str | None):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.id == user_id).first()
    
    if not existing_user:
        user = User(id=user_id, first_name=first_name, last_name=last_name, username=username)
        db.add(user)
        db.commit()
    
    db.close()

def set_user_state(user_id: int, state: str):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    
    if user:
        user.state = state
        db.commit()
    
    db.close()

def get_user_state(user_id: int) -> str | None:
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    
    return user.state if user else None

def set_user_phone_number(user_id: int, phone_number: str):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    user.phone_number = phone_number
    db.commit()
    db.close()

def check_user_phone_number_exists(user_id: int) -> bool:
    db = SessionLocal()
    try:
        exists = (
            db.query(User)
            .filter(User.id == user_id, User.phone_number.isnot(None), User.phone_number != '')
            .first() is not None
        )
        return exists
    finally:
        db.close()