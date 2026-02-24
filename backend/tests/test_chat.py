import pytest
from httpx import AsyncClient, ASGITransport
from main import app

# Configuração para o pytest-asyncio reconhecer testes assíncronos
pytestmark = pytest.mark.asyncio

async def test_chat_in_context_query():
    """Testa se o bot responde corretamente com base no contexto do estoque."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/chat/", json={"message": "Quantas laranjas tem?"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Valida se a resposta menciona a quantidade mockada (50)
    assert "50" in data["reply"]
    assert "laranja" in data["reply"].lower()

async def test_chat_out_of_context_guardrail():
    """Testa se o bot bloqueia perguntas fora do escopo da loja."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/chat/", json={"message": "Qual é a capital da França e como fazer um bolo?"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Valida se o bot acionou o guardrail e não respondeu a pergunta real
    reply_lower = data["reply"].lower()
    assert "frutas e cia" in reply_lower
    assert "paris" not in reply_lower
    assert "bolo" not in reply_lower or "não posso" in reply_lower