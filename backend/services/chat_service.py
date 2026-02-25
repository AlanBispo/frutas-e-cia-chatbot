import logging
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.chat_repository import ChatRepository
from services.llm_service import generate_chat_response

# Configuração básica de log para ver erros no terminal do Docker
logger = logging.getLogger(__name__)

class ChatService:
    @staticmethod
    async def process_message(user_message: str, db: AsyncSession) -> str:
        """
        Orquestra a busca de contexto e a chamada ao LLM.
        """
        try:
            # Busca dados 
            produtos = await ChatRepository.get_all_stock(db)
            infos = await ChatRepository.get_store_info(db)
            history_db = await ChatRepository.get_recent_history(db)
            
            history_for_llm = [
                {"role": m.role, "parts": [m.content]} for m in history_db
            ]
            contexto_estoque = "\n".join([f"- {p.nome}: R$ {p.preco:.2f}" for p in produtos])
            contexto_loja = "\n".join([f"- {i.chave}: {i.valor}" for i in infos])
            contexto_completo = f"ESTOQUE:\n{contexto_estoque}\n\nLOJA:\n{contexto_loja}"

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