from sqlalchemy import select
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