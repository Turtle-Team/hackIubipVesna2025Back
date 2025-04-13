from pydantic import BaseModel


class NotificationSettingsBase(BaseModel):
    email: str


class NotificationSettingsCreate(NotificationSettingsBase):
    pass


class NotificationSettings(NotificationSettingsBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True 