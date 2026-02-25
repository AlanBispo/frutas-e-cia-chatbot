from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.config import get_db
from services.oferta_service import OfertaService
from schemas.oferta import OfertaCreate, OfertaResponse
from typing import List

router = APIRouter(prefix="/admin/ofertas", tags=["Admin - Ofertas"])

@router.get("/", response_model=List[OfertaResponse])
async def listar(db: AsyncSession = Depends(get_db)):
    return await OfertaService.listar_ofertas(db)

@router.post("/", response_model=OfertaResponse)
async def criar(oferta: OfertaCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await OfertaService.criar_oferta(db, oferta)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{oferta_id}")
async def deletar(oferta_id: int, db: AsyncSession = Depends(get_db)):
    await OfertaService.remover_oferta(db, oferta_id)
    return {"message": "Oferta removida"}