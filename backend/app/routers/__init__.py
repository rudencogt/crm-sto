from fastapi import APIRouter
from app.routers import vehicle, order, user, auth  # Импортируем дополнительные роутеры

router = APIRouter()

# Подключаем роу́теры к основному приложению с пояснениями
router.include_router(vehicle.router, prefix="/vehicles", tags=["Vehicles"], responses={404: {"description": "Not Found"}})
router.include_router(order.router, prefix="/orders", tags=["Orders"], responses={404: {"description": "Not Found"}})
router.include_router(user.router, prefix="/users", tags=["Users"], responses={404: {"description": "Not Found"}})
router.include_router(auth.router, prefix="/auth", tags=["Authentication"], responses={404: {"description": "Not Found"}})
