import api
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.utils.notification import EmailNotificationSender, start_monitor
import threading

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
    uvicorn.run(app, port=9667)