from sqlalchemy.ext.asyncio import AsyncSession
from repositories.produto_repository import ProdutoRepository

class ProdutoService:
    @staticmethod
    async def listar_produtos(db: AsyncSession):
        return await ProdutoRepository.get_all(db)

    @staticmethod
    async def criar_produto(db: AsyncSession, produto_data):
        if produto_data.preco <= 0:
            raise ValueError("O preço do produto deve ser maior que zero.")
        
        return await ProdutoRepository.create(db, produto_data.model_dump())

    @staticmethod
    async def atualizar_produto(db: AsyncSession, produto_id: int, produto_data):
        existente = await ProdutoRepository.get_by_id(db, produto_id)
        if not existente:
            raise ValueError("Produto não encontrado.")
            
        return await ProdutoRepository.update(db, produto_id, produto_data.model_dump())

    @staticmethod
    async def excluir_produto(db: AsyncSession, produto_id: int):
        return await ProdutoRepository.delete(db, produto_id)