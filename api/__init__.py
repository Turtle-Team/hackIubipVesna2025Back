from fastapi import APIRouter
from .endpoints import user, role, auth, monitored_product, product, notification
from . import events

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(role.router, prefix="/roles", tags=["roles"])
router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(monitored_product.router, prefix="/monitored-products", tags=["monitored-products"])
router.include_router(product.router, prefix="/products", tags=["products"])
router.include_router(notification.router, prefix="/notifications", tags=["notifications"])
