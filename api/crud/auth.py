from sqlalchemy.orm import Session
from database.schemas import User

def get_user_by_login(db: Session, login: str):
    return db.query(User).filter(User.login == login).first()
