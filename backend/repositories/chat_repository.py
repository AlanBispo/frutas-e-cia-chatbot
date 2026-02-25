from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.chat import ChatMessage
from models.produto import Produto
from models.informacao import InformacaoLoja

class ChatRepository:
    @staticmethod
    async def get_all_stock(db: AsyncSession):
        result = await db.execute(select(Produto))
        return result.scalars().all()

    @staticmethod
    async def get_store_info(db: AsyncSession):
        result = await db.execute(select(InformacaoLoja))
        return result.scalars().all()

    @staticmethod
    async def get_recent_history(db: AsyncSession, limit: int = 10):
        result = await db.execute(
            select(ChatMessage).order_by(ChatMessage.created_at.asc()).limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def save_interaction(db: AsyncSession, user_content: str, bot_content: str):
        user_msg = ChatMessage(role="user", content=user_content)
        bot_msg = ChatMessage(role="model", content=bot_content)
        db.add_all([user_msg, bot_msg])
        await db.commit()

    @staticmethod
    async def delete_history(db: AsyncSession):
        await db.execute(delete(ChatMessage))
        await db.commit()