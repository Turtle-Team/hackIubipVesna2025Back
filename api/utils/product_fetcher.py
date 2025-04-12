import aiohttp
from typing import Optional, Dict
from urllib.parse import quote


async def fetch_product_by_url(url: str) -> Optional[Dict]:
    """
    Fetch product data from remote server by URL
    """
    base_url = "http://192.168.0.222:7812/api/product/current_market/"
    encoded_url = quote(url)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}?article={encoded_url}") as response:
                if response.status == 200:
                    return await response.json()
                return None
    except Exception as e:
        print(f"Error fetching product data: {e}")
        return None 