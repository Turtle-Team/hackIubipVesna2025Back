from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from api.crud import notification as notification_crud
from api.schemas.notification import NotificationSettingsCreate, NotificationSettings
from api.security import get_current_user
from database.schemas.user import User

router = APIRouter()


@router.post("/", response_model=NotificationSettings)
def create_notification_settings(
    notification_settings: NotificationSettingsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_notification = notification_crud.get_notification_settings(db, current_user.id)
    if db_notification:
        raise HTTPException(status_code=400, detail="Notification settings already exist")
    return notification_crud.create_notification_settings(db, current_user.id, notification_settings)


@router.get("/", response_model=NotificationSettings)
def read_notification_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_notification = notification_crud.get_notification_settings(db, current_user.id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification settings not found")
    return db_notification


@router.put("/", response_model=NotificationSettings)
def update_notification_settings(
    notification_settings: NotificationSettingsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_notification = notification_crud.update_notification_settings(db, current_user.id, notification_settings)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification settings not found")
    return db_notification 