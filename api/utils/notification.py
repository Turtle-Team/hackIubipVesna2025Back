import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
from database.schemas.product import Product
from database.schemas.notification import NotificationSettings
from database.schemas.user import User
from datetime import datetime, timedelta
import time
from typing import Protocol, Dict, List
import pandas as pd
from sqlalchemy import func
import threading
from database import Session, Base
import setting

class NotificationSender(Protocol):
    def send_notification(self, email: str, category_name: str, price_changes: List[Dict]) -> None:
        ...

class EmailNotificationSender:
    def __init__(self, smtp_server: str, smtp_port: int, email: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    def send_notification(self, email: str, category_name: str, price_changes: List[Dict]) -> None:
        if not price_changes:
            return

        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = email
        msg['Subject'] = f"Снижение цен у товара {category_name}"

        body = f"""
        Уважаемый пользователь,
        
        У товара {category_name} обнаружены следующие снижения цен:
        
        """
        
        for change in price_changes:
            body += f"""
            Товар: {change['name']}
            Старая цена: {change['old_price']} руб.
            Новая цена: {change['new_price']} руб.
            Снижение: {change['price_difference']} руб. ({change['price_difference_percent']:.2f}%)
            Ссылка: {change['url']}
            
            """
        
        body += """
        С уважением,
        Система мониторинга цен
        """
        
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.email, self.password)
                server.send_message(msg)
        except smtplib.SMTPAuthenticationError as e:
            print(f"Ошибка аутентификации при отправке email: {e}")
            print("Проверьте настройки email в setting.py")
            print("Для Gmail нужно использовать пароль приложения, а не обычный пароль")
        except Exception as e:
            print(f"Ошибка при отправке email: {e}")

class PriceMonitor:
    def __init__(self, db: Session, notification_sender: NotificationSender):
        self.db = db
        self.notification_sender = notification_sender
        self.last_check = {}

    def get_price_changes(self, item_id: int) -> List[Dict]:
        products = self.db.query(Product).filter(Product.item_id == item_id).all()
        
        if not products:
            return []

        df = pd.DataFrame([{
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'url': p.url,
            'created_at': p.created_at
        } for p in products])

        df = df.sort_values('created_at')
        min_prices = df.groupby('id')['price'].min().reset_index()
        current_prices = df.groupby('id').last().reset_index()
        
        price_changes = pd.merge(
            current_prices[['id', 'name', 'price', 'url']],
            min_prices[['id', 'price']],
            on='id',
            suffixes=('_current', '_min')
        )
        
        price_changes = price_changes[price_changes['price_current'] < price_changes['price_min']]
        price_changes['price_difference'] = price_changes['price_min'] - price_changes['price_current']
        price_changes['price_difference_percent'] = (price_changes['price_difference'] / price_changes['price_min']) * 100
        
        return price_changes.to_dict('records')

    def check_price_changes(self):
        current_time = datetime.now()
        item_ids = self.db.query(Product.item_id).distinct().all()
        item_ids = [item[0] for item in item_ids]
        
        for item_id in item_ids:
            if item_id not in self.last_check:
                self.last_check[item_id] = current_time
                continue

            if current_time - self.last_check[item_id] < timedelta(minutes=15):
                continue

            price_changes = self.get_price_changes(item_id)
            
            if price_changes:
                first_product = self.db.query(Product).filter(Product.item_id == item_id).first()
                if first_product and first_product.monitored_product:
                    user = first_product.monitored_product.user
                    if user and user.notification_settings:
                        self.notification_sender.send_notification(
                            user.notification_settings.email,
                            first_product.name,
                            price_changes
                        )

            self.last_check[item_id] = current_time

def run_monitor(db: Session, notification_sender: NotificationSender):
    monitor = PriceMonitor(db, notification_sender)
    while True:
        monitor.check_price_changes()
        time.sleep(300)

# Создаем отправитель уведомлений
notification_sender = EmailNotificationSender(
    smtp_server=setting.SMTP_SERVER,
    smtp_port=setting.SMTP_PORT,
    email=setting.EMAIL_USER,
    password=setting.EMAIL_PASSWORD
)

def start_monitor():
    """Запускает мониторинг цен в отдельном процессе"""
    db = Session()
    try:
        run_monitor(db, notification_sender)
    finally:
        db.close()

# Запускаем монитор в отдельном потоке при импорте модуля
notification_thread = threading.Thread(target=start_monitor, daemon=True)
notification_thread.start()
