from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.produto import Produto
from models.oferta import Oferta

class ProdutoRepository:
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Produto).order_by(Produto.nome))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, produto_id: int):
        result = await db.execute(select(Produto).where(Produto.id == produto_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, dados_produto: dict):
        novo_produto = Produto(**dados_produto)
        db.add(novo_produto)
        await db.commit()
        await db.refresh(novo_produto)
        return novo_produto

    @staticmethod
    async def update(db: AsyncSession, produto_id: int, novos_dados: dict):
        await db.execute(
            update(Produto).where(Produto.id == produto_id).values(**novos_dados)
        )
        await db.commit()
        return await ProdutoRepository.get_by_id(db, produto_id)

    @staticmethod
    async def delete(db: AsyncSession, produto_id: int):
        await db.execute(delete(Oferta).where(Oferta.produto_id == produto_id))
    
        await db.execute(delete(Produto).where(Produto.id == produto_id))
        await db.commit()