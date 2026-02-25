from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.config import get_db
from services.oferta_service import OfertaService

router = APIRouter(prefix="/ofertas", tags=["Ofertas"])

@router.get("/hoje")
async def get_daily_offers(db: AsyncSession = Depends(get_db)):
    try:
        return await OfertaService.get_today_offers_formatted(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao processar ofertas.")