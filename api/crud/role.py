from sqlalchemy.orm import Session

from database.schemas.role import Role

__all__ = ["create_role", "get_role", "delete_role", "update_role", "get_roles"]

def create_role(db: Session, name: str):
    db_role = Role(name=name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_roles(db: Session):
    return db.query(Role).all()


def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def update_role(db: Session, role_id: int, name: str):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role:
        db_role.name = name
        db.commit()
        db.refresh(db_role)
        return db_role
    return None


def delete_role(db: Session, role_id: int):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role:
        db.delete(db_role)
        db.commit()
        return db_role
    return None
