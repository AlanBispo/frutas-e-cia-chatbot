from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from models.produto import Produto
from models.oferta import Oferta

class OfertaRepository:
    @staticmethod
    async def get_active_offers_with_products(db: AsyncSession):
        """
        Busca todas as ofertas ativas realizando o join com a tabela de produtos.
        """
        query = select(Oferta, Produto).join(Produto, Oferta.produto_id == Produto.id)
        result = await db.execute(query)
        return result.all()

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Oferta).options(joinedload(Oferta.produto)))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, dados: dict):
        nova_oferta = Oferta(**dados)
        db.add(nova_oferta)
        await db.commit()

        return await OfertaRepository.get_by_id(db, nova_oferta.id)

    @staticmethod
    async def delete(db: AsyncSession, oferta_id: int):
        await db.execute(delete(Oferta).where(Oferta.id == oferta_id))
        await db.commit()

    @staticmethod
    async def get_by_id(db: AsyncSession, oferta_id: int):
        # Buscamos a oferta carregando também o objeto produto
        result = await db.execute(
            select(Oferta)
            .options(joinedload(Oferta.produto))
            .where(Oferta.id == oferta_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_active_offers(db: AsyncSession):
        # Busca apenas o que é promoção e está ativo
        result = await db.execute(select(Oferta).where(Oferta.ativa == True))
        return result.scalars().all()