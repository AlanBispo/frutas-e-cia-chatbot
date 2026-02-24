import pytest
import asyncio
from database.config import engine

# Garante que o loop de eventos seja o mesmo para todos os testes
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Fecha o engine ANTES do loop terminar
@pytest.fixture(scope="session", autouse=True)
async def disconnect_db():
    yield
    await engine.dispose()