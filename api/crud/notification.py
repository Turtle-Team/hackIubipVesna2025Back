from sqlalchemy.orm import Session

from database.schemas.notification import NotificationSettings
from api.schemas.notification import NotificationSettingsCreate


def get_notification_settings(db: Session, user_id: int):
    return db.query(NotificationSettings).filter(NotificationSettings.user_id == user_id).first()


def create_notification_settings(db: Session, user_id: int, notification_settings: NotificationSettingsCreate):
    db_notification = NotificationSettings(
        user_id=user_id,
        email=notification_settings.email
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def update_notification_settings(db: Session, user_id: int, notification_settings: NotificationSettingsCreate):
    db_notification = get_notification_settings(db, user_id)
    if db_notification:
        db_notification.email = notification_settings.email
        db.commit()
        db.refresh(db_notification)
    return db_notification 