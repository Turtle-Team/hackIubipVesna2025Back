import threading
from .utils import product_poller, notification

# Запуск поллера продуктов
poller = product_poller.ProductPoller()
threading.Thread(target=poller.start).start()

# Запуск монитора уведомлений
notification_thread = threading.Thread(target=notification.start_monitor, daemon=True)
notification_thread.start()

# Запуск Telegram бота в отдельном потоке
telegram_thread = threading.Thread(
    target=notification.telegram_sender.bot.polling,
    kwargs={'none_stop': True},
    daemon=True
)
telegram_thread.start()
