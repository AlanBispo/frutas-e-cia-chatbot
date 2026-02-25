from fastapi import APIRouter
from api.chat import router as chat_router
from api.ofertas import router as ofertas_router
from api.admin_produtos import router as admin_produtos_router
from api.admin_ofertas import router as admin_ofertas_router

api_router = APIRouter()

api_router.include_router(chat_router)
api_router.include_router(ofertas_router)
api_router.include_router(admin_produtos_router)
api_router.include_router(admin_ofertas_router)