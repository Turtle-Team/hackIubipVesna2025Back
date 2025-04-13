import threading

from .utils import product_poller, notification

poller = product_poller.ProductPoller()
threading.Thread(target=poller.start).start()

notification_thread = threading.Thread(target=notification.start_monitor, daemon=True)
notification_thread.start()
