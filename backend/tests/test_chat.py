import pytest
from httpx import AsyncClient, ASGITransport
from main import app

# Configura o escopo para permitir testes assíncronos
pytestmark = pytest.mark.asyncio

async def test_chat_health_check():
    """Valida se a API está de pé."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

async def test_chat_query_real_stock():
    """
    Testa se o bot consulta o banco e retorna dados do seed.
    Ex: Pitaya Rosa foi inserida via migration.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Pergunta específica sobre um dado do seed
        response = await ac.post("/chat/", json={"message": "Quanto custa a Pitaya Rosa?"})
    
    assert response.status_code == 200
    reply = response.json()["reply"].lower()
    
    # Valida se o bot encontrou o preço de 15.00 definido na migration
    assert "15" in reply
    assert "pitaya" in reply

async def test_chat_business_info():
    """Valida se o bot conhece as regras da loja (Horário, Frete)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/chat/", json={"message": "Vocês entregam? Qual o valor do frete?"})
    
    assert response.status_code == 200
    reply = response.json()["reply"].lower()
    
    # Dados vindos da tabela informacoes_loja
    assert "5" in reply or "cinco" in reply
    assert "entrega" in reply or "frete" in reply

async def test_chat_guardrail_out_of_context():
    """Garante que o bot recusa perguntas que não sejam sobre a loja."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/chat/", json={"message": "Como criar um servidor em Java?"})
    
    assert response.status_code == 200
    reply = response.json()["reply"].lower()
    
    # O bot deve usar a mensagem educada do Guardrail em vez de explicar Java
    assert "frutas e cia" in reply
    assert "java" not in reply