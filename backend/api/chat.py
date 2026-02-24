from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from database.config import get_db
from models.produto import Produto
from models.informacao import InformacaoLoja
from services.llm_service import generate_chat_response

router = APIRouter(prefix="/chat", tags=["Chatbot"])

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat_endpoint(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    # 1. Busca todos os produtos do estoque
    result_produtos = await db.execute(select(Produto))
    produtos = result_produtos.scalars().all()
    
    # 2. Busca informações institucionais da loja
    result_infos = await db.execute(select(InformacaoLoja))
    infos = result_infos.scalars().all()
    
    # 3. Formata o contexto para o LLM
    contexto_estoque = "\n".join([
        f"- {p.nome} ({p.categoria}): R$ {p.preco:.2f}. Estoque: {p.quantidade_estoque}. Descrição: {p.descricao}" 
        for p in produtos
    ])
    
    contexto_loja = "\n".join([f"- {i.chave}: {i.valor}" for i in infos])
    
    full_context = f"ESTOQUE ATUAL:\n{contexto_estoque}\n\nINFORMAÇÕES DA LOJA:\n{contexto_loja}"
    
    # 4. Gera resposta com a IA
    reply = await generate_chat_response(request.message, full_context)
    
    return {"reply": reply}