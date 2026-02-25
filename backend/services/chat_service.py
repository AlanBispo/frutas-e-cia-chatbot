from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.chat import ChatMessage

class ChatService:
    @staticmethod
    async def clear_all_history(db: AsyncSession):
        """
        Executa a limpeza física de todas as mensagens no MySQL.
        """
        try:
            await db.execute(delete(ChatMessage))
            await db.commit()
            return True
        except Exception as e:
            await db.rollback()
            print(f"Erro no ChatService.clear_all_history: {e}")
            raise e
