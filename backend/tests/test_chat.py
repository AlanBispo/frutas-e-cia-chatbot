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

async def test_admin_create_product():
    """Valida se o painel administrativo consegue cadastrar um novo produto."""
    novo_produto = {
        "nome": "Abacate Hass",
        "preco": 12.50,
        "quantidade_estoque": 45
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/admin/produtos/", json=novo_produto)
    
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Abacate Hass"
    assert data["preco"] == 12.50
    assert "id" in data # Garante que o banco gerou um ID

async def test_chat_offer_priority_logic():
    """
    Garante que o bot prioriza o preço de oferta em vez do preço original.
    Baseado no seed da Melancia (De 22.00 por 20.00).
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/chat/", json={"message": "A melancia está em promoção? Qual o valor?"})
    
    assert response.status_code == 200
    reply = response.json()["reply"].lower()
    
    # O bot DEVE informar o preço de 20 e não o de 22
    assert "20" in reply
    assert "promoção" in reply or "oferta" in reply
    # Teste de segurança: ele não deve dizer que custa 22 como sendo o preço atual
    assert "22" not in reply or "de r$ 22" in reply # Aceita se disser "De 22 por 20"