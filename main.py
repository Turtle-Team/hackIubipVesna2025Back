import api
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.utils.notification import EmailNotificationSender, start_monitor
import threading
import setting

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api.router)

# Запускаем монитор уведомлений в отдельном потоке
notification_thread = threading.Thread(target=start_monitor, daemon=True)
notification_thread.start()

# Тестовый модуль
if __name__ == "__main__":
    # Создаем тестовые данные
    test_price_changes = [
        {
            'name': 'Тестовый товар 1',
            'old_price': 1000.0,
            'new_price': 800.0,
            'price_difference': 200.0,
            'price_difference_percent': 20.0,
            'url': 'https://example.com/product1'
        },
        {
            'name': 'Тестовый товар 2',
            'old_price': 2000.0,
            'new_price': 1500.0,
            'price_difference': 500.0,
            'price_difference_percent': 25.0,
            'url': 'https://example.com/product2'
        }
    ]
    
    # Создаем отправитель уведомлений
    test_sender = EmailNotificationSender(
        smtp_server=setting.SMTP_SERVER,
        smtp_port=setting.SMTP_PORT,
        email=setting.EMAIL_USER,
        password=setting.EMAIL_PASSWORD
    )
    
    # Отправляем тестовое уведомление
    test_sender.send_notification(
        email='bugshackaton@gmail.com',
        category_name='Тестовая категория',
        price_changes=test_price_changes
    )
    
    print("Тестовое уведомление отправлено!")
    
    # Запускаем сервер
    uvicorn.run(app, port=9667)