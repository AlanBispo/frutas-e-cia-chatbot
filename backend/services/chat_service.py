import logging
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.chat_repository import ChatRepository
from repositories.oferta_repository import OfertaRepository
from services.llm_service import generate_chat_response

# Configuração básica de log para ver erros no terminal do Docker
logger = logging.getLogger(__name__)

class ChatService:
    @staticmethod
    async def process_message(user_message: str, db: AsyncSession) -> str:
        """
        Orquestra a busca de contexto e a chamada ao LLM com suporte a ofertas.
        """
        try:
            # Busca dados
            produtos = await ChatRepository.get_all_stock(db)
            infos = await ChatRepository.get_store_info(db)
            history_db = await ChatRepository.get_recent_history(db)
            ofertas = await OfertaRepository.get_active_offers(db)

            mapa_ofertas = {o.produto_id: o.preco_oferta for o in ofertas}
            history_for_llm = [
                {"role": m.role, "parts": [m.content]} for m in history_db
            ]

            linhas_estoque = []
            for p in produtos:
                preco_promocional = mapa_ofertas.get(p.id)
                
                if preco_promocional:
                    linha = f"- {p.nome}: DE R$ {p.preco:.2f} POR R$ {preco_promocional:.2f} (PROMOÇÃO ATIVA)"
                else:
                    linha = f"- {p.nome}: R$ {p.preco:.2f}"
                
                linhas_estoque.append(linha)

            contexto_estoque = "\n".join(linhas_estoque)
            contexto_loja = "\n".join([f"- {i.chave}: {i.valor}" for i in infos])
            
            contexto_completo = f"ESTOQUE E PROMOÇÕES:\n{contexto_estoque}\n\nINFORMAÇÕES DA LOJA:\n{contexto_loja}"

            reply = await generate_chat_response(user_message, contexto_completo, history_for_llm)


            await ChatRepository.save_interaction(db, user_message, reply)
            
            return reply
        except Exception as e:
            await db.rollback()
            logger.error(f"Erro ao processar mensagem no ChatService: {str(e)}", exc_info=True)
            raise e

    @staticmethod
    async def clear_all_history(db: AsyncSession):
        """
        Deleta o histórico e garante o rollback em caso de falha.
        """
        try:
            await ChatRepository.delete_history(db)
            return True
        except Exception as e:
            await db.rollback()
            logger.error(f"Erro ao limpar histórico no ChatService: {str(e)}", exc_info=True)
            raise e