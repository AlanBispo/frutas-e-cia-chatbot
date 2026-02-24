from fastapi import APIRouter
from pydantic import BaseModel, Field
from services.llm_service import generate_chat_response

router = APIRouter(prefix="/chat", tags=["Chatbot"])

class ChatRequest(BaseModel):
    message: str = Field(..., description="Mensagem enviada pelo usuário")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="Resposta gerada pelo assistente")

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # TODO: Na Fase 2, faremos a query real no MySQL via SQLAlchemy usando a dependency get_db.
    # Por enquanto, simulamos a injeção do estoque de frutas no contexto.
    mock_db_context = """
    Estoque Atual:
    - Laranjas: 50 unidades disponíveis. Preço: R$ 2,00 cada.
    - Maçãs: 20 unidades disponíveis. Preço: R$ 3,00 cada.
    - Bananas: 100 unidades disponíveis. Preço: R$ 1,50 cada.
    """
    
    reply = await generate_chat_response(
        user_message=request.message, 
        db_context=mock_db_context
    )
    
    return ChatResponse(reply=reply)