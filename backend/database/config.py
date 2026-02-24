from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool

load_dotenv()

# Substitua pelas suas credenciais reais no arquivo .env
# Exemplo: mysql+aiomysql://root:senha@localhost:3306/frutas_db
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://user:password@localhost:3306/frutas_db")

engine = create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

async def get_db() -> AsyncSession: # type: ignore
    """Dependency para injeção da sessão do banco de dados nas rotas."""
    async with AsyncSessionLocal() as session:
        yield session