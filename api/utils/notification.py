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
import threading
from database import Session
import setting
import telebot
from telebot.types import Message
from setting import TELEGRAM_BOT_TOKEN

class NotificationSender(Protocol):
    def send_notification(self, email: str, category_name: str, price_changes: List[Dict]) -> None:
        ...

class EmailNotificationSender:
    def __init__(self):
        self.smtp_server = setting.SMTP_SERVER
        self.smtp_port = setting.SMTP_PORT
        self.email = setting.EMAIL_USER
        self.password = setting.EMAIL_PASSWORD

    def send_notification(self, user_id: str, message: str) -> bool:
        db = Session()
        try:
            notification_settings = db.query(NotificationSettings).filter(
                NotificationSettings.user_id == user_id
            ).first()

            if not notification_settings or not notification_settings.email:
                return False

            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = notification_settings.email
            msg['Subject'] = "Уведомление о ценах"
            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Ошибка отправки email уведомления: {e}")
            return False
        finally:
            db.close()

class TelegramNotificationSender:
    def __init__(self):
        self.bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
        self.setup_handlers()

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message: Message):
            self.bot.reply_to(message, 
                "Привет! Я бот для уведомлений о ценах.\n"
                "Используйте команду /link для привязки аккаунта.")

        @self.bot.message_handler(commands=['link'])
        def handle_link(message: Message):
            if len(message.text.split()) < 2:
                self.bot.reply_to(message, "Пожалуйста, укажите ваш логин: /link <login>")
                return
            
            login = message.text.split()[1]
            db = Session()
            try:
                user = db.query(User).filter(User.login == login).first()
                if not user:
                    self.bot.reply_to(message, "Пользователь с таким логином не найден")
                    return

                notification_settings = db.query(NotificationSettings).filter(
                    NotificationSettings.user_id == user.id
                ).first()

                if not notification_settings:
                    notification_settings = NotificationSettings(
                        user_id=user.id,
                        telegram_id=str(message.chat.id)
                    )
                    db.add(notification_settings)
                else:
                    notification_settings.telegram_id = str(message.chat.id)

                db.commit()
                self.bot.reply_to(message, f"Аккаунт успешно привязан! Логин: {login}")
            except Exception as e:
                db.rollback()
                self.bot.reply_to(message, f"Произошла ошибка: {str(e)}")
            finally:
                db.close()

    def send_notification(self, user_id: str, message: str) -> bool:
        db = Session()
        try:
            notification_settings = db.query(NotificationSettings).filter(
                NotificationSettings.user_id == user_id
            ).first()

            if not notification_settings or not notification_settings.telegram_id:
                return False
                
            self.bot.send_message(notification_settings.telegram_id, message)
            return True
        except Exception as e:
            print(f"Ошибка отправки Telegram уведомления: {e}")
            return False
        finally:
            db.close()

class PriceMonitor:
    def __init__(self, db: Session, notification_senders: List[NotificationSender]):
        self.db = db
        self.notification_senders = notification_senders
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
            if item_id in self.last_check:
                if current_time - self.last_check[item_id] < timedelta(minutes=15):
                    continue

            price_changes = self.get_price_changes(item_id)
            
            if price_changes:
                first_product = self.db.query(Product).filter(Product.item_id == item_id).first()
                if first_product and first_product.monitored_product:
                    user = first_product.monitored_product.user
                    if user and user.notification_settings:
                        message = f"Изменение цен для товара {first_product.name}:\n\n"
                        for change in price_changes:
                            message += (
                                f"Товар: {change['name']}\n"
                                f"Старая цена: {change['price_min']} руб.\n"
                                f"Новая цена: {change['price_current']} руб.\n"
                                f"Снижение: {change['price_difference']} руб. ({change['price_difference_percent']:.2f}%)\n"
                                f"Ссылка: {change['url']}\n\n"
                            )
                        
                        for sender in self.notification_senders:
                            sender.send_notification(str(user.id), message)

            self.last_check[item_id] = current_time

def run_monitor(db: Session, notification_senders: List[NotificationSender]):
    monitor = PriceMonitor(db, notification_senders)
    while True:
        monitor.check_price_changes()
        time.sleep(60)

# Создаем отправители уведомлений
email_sender = EmailNotificationSender()
telegram_sender = TelegramNotificationSender()

def start_monitor():
    """Запускает мониторинг цен в отдельном процессе"""
    db = Session()
    try:
        run_monitor(db, [email_sender, telegram_sender])
    finally:
        db.close()

# Запускаем монитор в отдельном потоке при импорте модуля
notification_thread = threading.Thread(target=start_monitor, daemon=True)
notification_thread.start()
