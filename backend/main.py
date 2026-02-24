from fastapi import FastAPI
from api.chat import router as chat_router

app = FastAPI(
    title="Frutas e Cia API",
    description="API para o Chatbot de atendimento integrado a estoque e IA.",
    version="1.0.0"
)

app.include_router(chat_router)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "API rodando perfeitamente."}