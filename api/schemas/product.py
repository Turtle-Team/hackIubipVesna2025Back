from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class MarketPlaceId(Enum):
    WILDBERRIES = 1
    OZON = 2
    MEGA_MARKET = 3
    YANDEX_MARKET = 4
    ALIEXPRESS = 5
    MAGNIT_MARKET = 6


class MarketName(Enum):
    WILDBERRIES = 'WILDBERRIES'
    OZON = 'OZON'
    MEGA_MARKET = 'MEGAMARKET'
    YANDEX_MARKET = 'YANDEX_MARKET'
    ALIEXPRESS = 'ALIEXPRESS'
    MAGNIT_MARKET = 'MAGNIT_MARKET'


class MarketPicture(Enum):
    WILDBERRIES = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Wildberries_Logo.png/250px-Wildberries_Logo.png'
    OZON = 'https://upload.wikimedia.org/wikipedia/ru/thumb/e/ec/OZON_2019.svg/200px-OZON_2019.svg.png'
    MEGA_MARKET = 'https://upload.wikimedia.org/wikipedia/ru/e/e4/%D0%9C%D0%B5%D0%B3%D0%B0%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82_%D0%BB%D0%BE%D0%B3%D0%BE%D1%82%D0%B8%D0%BF_2023.png'
    YANDEX_MARKET = 'https://yastatic.net/market-export/_/i/favicon/ymnew/558.png'
    ALIEXPRESS = 'https://yt3.googleusercontent.com/B3lrzrdjxXBXpgU5kEOBkCrPBzfZmiQXMU9xAMeDLfS97Nj_PEpkepisV-RhVgh1_ObVFCQ2S0g=s900-c-k-c0x00ffffff-no-rj'
    MAGNIT_MARKET = 'https://i.otzovik.com/objects/b/1140000/1135463.png'


class MarketPlace(BaseModel):
    id: MarketPlaceId
    code: MarketName
    icon: MarketPicture
    name: str


class MarketPlaceInfo(Enum):
    markets = [MarketPlace(code=MarketName.WILDBERRIES, id=MarketPlaceId.WILDBERRIES, icon=MarketPicture.WILDBERRIES,
                           name='WILDBERRIES'),
               MarketPlace(code=MarketName.OZON, id=MarketPlaceId.OZON, icon=MarketPicture.OZON, name='OZON'),
               MarketPlace(code=MarketName.MEGA_MARKET, id=MarketPlaceId.MEGA_MARKET, icon=MarketPicture.MEGA_MARKET,
                           name='Мегамаркет'),
               MarketPlace(code=MarketName.YANDEX_MARKET, id=MarketPlaceId.YANDEX_MARKET,
                           icon=MarketPicture.YANDEX_MARKET, name='Яндекс Маркет'),
               MarketPlace(code=MarketName.ALIEXPRESS, id=MarketPlaceId.ALIEXPRESS, icon=MarketPicture.ALIEXPRESS,
                           name='ALIEXPRESS'),
               MarketPlace(code=MarketName.MAGNIT_MARKET, id=MarketPlaceId.MAGNIT_MARKET,
                           icon=MarketPicture.MAGNIT_MARKET, name='Магнит'),
               ]


class ProductBase(BaseModel):
    market: MarketPlace = None
    item_id: int = 0
    name: str = ''
    url: str = ''
    price: float = 0
    rating: float = 0.0
    review_count: int = 0
    buy_count: int = 0
    picture: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    market: Optional[int] = None
    item_id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    buy_count: Optional[int] = None
    picture: Optional[str] = None


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
