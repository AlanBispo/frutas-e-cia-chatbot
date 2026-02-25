from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.produto import Produto
from models.oferta import Oferta

class OfertaService:
    @staticmethod
    async def get_today_offers_formatted(db: AsyncSession):
        try:
            query = select(Oferta, Produto).join(Produto, Oferta.produto_id == Produto.id)
            result = await db.execute(query)
            ofertas_data = result.all()

            if not ofertas_data:
                return {
                    "texto": "No momento não temos ofertas ativas. Como posso te ajudar?",
                    "items": []
                }

            texto_parts = ["Certo! Aqui estão as nossas melhores ofertas de hoje:"]
            items = []

            for oferta, produto in ofertas_data:
                texto_parts.append(f"- {produto.nome}: De R$ {produto.preco:.2f} por APENAS R$ {oferta.preco_oferta:.2f}!")
                items.append({
                    "nome": produto.nome,
                    "preco_oferta": oferta.preco_oferta
                })

            texto_parts.append("\nDeseja adicionar algum desses itens ao seu carrinho?")
        
            return {
                "texto": "\n".join(texto_parts),
                "items": items
            }
        except Exception as e:
            raise e