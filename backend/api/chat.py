from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from database.config import get_db
from models.produto import Produto
from models.informacao import InformacaoLoja
from models.chat import ChatMessage
from services.llm_service import generate_chat_response
from sqlalchemy.orm import Session

router = APIRouter(prefix="/chat", tags=["Chatbot"])

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat_endpoint(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    # Busca Contexto de Negócio
    result_produtos = await db.execute(select(Produto))
    produtos = result_produtos.scalars().all()
    result_infos = await db.execute(select(InformacaoLoja))
    infos = result_infos.scalars().all()
    
    # Busca Contexto de Conversa (MEMÓRIA)
    result_history = await db.execute(
        select(ChatMessage).order_by(ChatMessage.created_at.asc()).limit(10)
    )
    history_db = result_history.scalars().all()
    
    history_for_llm = [
        {"role": m.role, "parts": [m.content]} 
        for m in history_db
    ]

    contexto_estoque = "\n".join([f"- {p.nome}: R$ {p.preco:.2f}" for p in produtos])
    contexto_loja = "\n".join([f"- {i.chave}: {i.valor}" for i in infos])
    
    system_instruction = f"Você é o atendente da Frutas e Cia.\nESTOQUE:\n{contexto_estoque}\nLOJA:\n{contexto_loja}"

    # Gera resposta
    reply = await generate_chat_response(request.message, system_instruction, history_for_llm)
    
    # Salva a interação atual no MySQL para a próxima pergunta
    user_msg = ChatMessage(role="user", content=request.message)
    bot_msg = ChatMessage(role="model", content=reply)
    db.add_all([user_msg, bot_msg])
    await db.commit()
    
    return {"reply": reply}

@router.delete("/chat/reset")
async def reset_chat(db: Session = Depends(get_db)):
    try:
        db.query(ChatMessage).delete()
        db.commit()
        return {"message": "Histórico da Frutas e Cia limpo com sucesso!"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}