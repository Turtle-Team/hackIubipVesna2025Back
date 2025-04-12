import asyncio
import threading

import aiohttp
import json
from datetime import datetime
from typing import Dict, List
from sqlalchemy.orm import Session
from database import Session
from database.schemas.product import Product
from ..crud.monitored_product import get_all_monitored_products
from ..utils.product_fetcher import fetch_product_by_url

class ProductPoller:
    def __init__(self):
        self.base_url = "http://192.168.0.222:7812/api/product/"
        self.session = None

    async def init_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def fetch_products(self, product_name: str) -> Dict | None:
        params = {
            "name": product_name,
            "offset": 10,
            "page_number": 1,
            "filter_by": "asc",
            "filter_name": "buy",
            "price_from": 0
        }
        
        try:
            async with self.session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error fetching products: {response.status}")
                    return None
        except Exception as e:
            print(f"Error in fetch_products: {e}")
            return None

    def save_products(self, db: Session, products_data: Dict, monitored_product_id: int):
        if not products_data:
            return

        # If we got data from URL, wrap it in items array to match the structure
        if "items" not in products_data:
            products_data = {"items": [products_data]}

        for item in products_data["items"]:
            product_data = {
                "monitored_product_id": monitored_product_id,
                "market": item["market"],
                "item_id": str(item["item_id"]),
                "name": item["name"],
                "url": item["url"],
                "price": item["price"],
                "rating": item["rating"],
                "review_count": item["review_count"],
                "buy_count": item["buy_count"],
                "picture": item["picture"],
                "time_ship": item.get("time_ship"),
                "datetime_ship": datetime.fromisoformat(item["datetime_ship"].replace("Z", "+00:00")) if item.get("datetime_ship") else None,
                "geo": item.get("geo")
            }
            new_product = Product(**product_data)
            db.add(new_product)
        db.commit()

    async def poll_products(self):
        await self.init_session()
        db = Session()
        
        try:
            while True:
                monitored_products = get_all_monitored_products(db, skip=0, limit=100)
                
                for monitored_product in monitored_products:
                    if monitored_product.url:
                        # If URL is available, use it exclusively
                        products_data = await fetch_product_by_url(monitored_product.url)
                    else:
                        # Only use name search if no URL is available
                        products_data = await self.fetch_products(monitored_product.name)
                    
                    if products_data:
                        self.save_products(db, products_data, monitored_product.id)
                
                # Wait for 5 minutes before next poll
                await asyncio.sleep(300)
        except Exception as e:
            print(f"Error in poll_products: {e}")
        finally:
            await self.close_session()
            db.close()

    def start(self):
        asyncio.run(self.poll_products())

poller = ProductPoller()
threading.Thread(target=poller.start).start()
