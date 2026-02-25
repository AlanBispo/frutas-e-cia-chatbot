import logging
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.oferta_repository import OfertaRepository

logger = logging.getLogger(__name__)

class OfertaService:
    @staticmethod
    async def get_today_offers_formatted(db: AsyncSession):
        """
        Orquestra a busca de ofertas e formata a resposta para o frontend/LLM.
        """
        try:
            # Busca os dados
            ofertas_data = await OfertaRepository.get_active_offers_with_products(db)

            if not ofertas_data:
                return {
                    "texto": "No momento não temos ofertas ativas. Como posso te ajudar?",
                    "items": []
                }

            texto_parts = ["Certo! Aqui estão as nossas melhores ofertas de hoje:"]
            items = []

            for oferta, produto in ofertas_data:
                texto_parts.append(
                    f"- {produto.nome}: De R$ {produto.preco:.2f} por APENAS R$ {oferta.preco_oferta:.2f}!"
                )
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
            await db.rollback()
            logger.error(f"Erro ao buscar ofertas no OfertaService: {str(e)}", exc_info=True)
            raise e