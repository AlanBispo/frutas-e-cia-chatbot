from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from database.config import get_db
from services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chatbot"])

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat_endpoint(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    try:
        reply = await ChatService.process_message(request.message, db)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Ocorreu um erro ao processar sua mensagem com a IA."
        )

@router.delete("/clear")
async def clear_chat(db: AsyncSession = Depends(get_db)):
    try:
        await ChatService.clear_all_history(db)
        return {"message": "Histórico limpo com sucesso!"}
    except Exception as e:
        print(f"Erro ao limpar histórico: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível limpar o histórico de conversas."
        )