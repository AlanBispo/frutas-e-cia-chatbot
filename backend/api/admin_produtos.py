from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database.config import get_db
from services.produto_service import ProdutoService

from schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate

router = APIRouter(prefix="/admin/produtos", tags=["Admin - Produtos"])

@router.get("/", response_model=List[ProdutoResponse])
async def listar(db: AsyncSession = Depends(get_db)):
    return await ProdutoService.listar_produtos(db)

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
async def criar(produto: ProdutoCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await ProdutoService.criar_produto(db, produto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{produto_id}", response_model=ProdutoResponse)
async def editar_produto(produto_id: int, produto: ProdutoUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await ProdutoService.atualizar_produto(db, produto_id, produto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )

@router.delete("/{produto_id}")
async def deletar_produto(produto_id: int, db: AsyncSession = Depends(get_db)):
    await ProdutoService.excluir_produto(db, produto_id)
    return {"message": "Produto excluído com sucesso"}