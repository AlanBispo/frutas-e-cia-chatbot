import logging
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.oferta_repository import OfertaRepository
from repositories.produto_repository import ProdutoRepository

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
        
    @staticmethod
    async def criar_oferta(db, oferta_data):
        # Validação: O produto existe?
        produto = await ProdutoRepository.get_by_id(db, oferta_data.produto_id)
        if not produto:
            raise ValueError("Produto não encontrado.")
        
        # Validação: Preço da oferta deve ser menor que o original
        if oferta_data.preco_oferta >= produto.preco:
            raise ValueError("O preço de oferta deve ser menor que o preço original.")

        return await OfertaRepository.create(db, oferta_data.model_dump())

    @staticmethod
    async def listar_ofertas(db):
        return await OfertaRepository.get_all(db)

    @staticmethod
    async def remover_oferta(db, oferta_id):
        return await OfertaRepository.delete(db, oferta_id)