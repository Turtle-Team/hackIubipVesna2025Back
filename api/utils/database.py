from database import Session


# Функция для получения сессии базы данных
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

