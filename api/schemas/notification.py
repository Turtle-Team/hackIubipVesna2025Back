from pydantic import BaseModel, EmailStr


class NotificationSettingsBase(BaseModel):
    email: EmailStr


class NotificationSettingsCreate(NotificationSettingsBase):
    pass


class NotificationSettings(NotificationSettingsBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True 