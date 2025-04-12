from sqlalchemy.orm import Session

from database.schemas.user import User

__all__ = ["create_user", "get_users", "delete_user", "update_user", "get_user"]

def create_user(db: Session, login: str, password: str, role_id: int):
    db_user = User(login=login, password=password, role_id=role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int | str):
    return db.query(User).filter(User.id == int(user_id)).first()


def update_user(db: Session, user_id: int, login: str, role_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    db_user.login = login
    db_user.role_id = role_id
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user
