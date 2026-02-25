from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat import router as chat_router
from api.ofertas import router as ofertas_router

app = FastAPI(title="Frutas e Cia API")

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(ofertas_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}