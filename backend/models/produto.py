from sqlalchemy import Column, Integer, String, Float, Text
from database.config import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), index=True, nullable=False)
    descricao = Column(Text, nullable=True)
    preco = Column(Float, nullable=False)
    quantidade_estoque = Column(Integer, nullable=False, default=0)
    categoria = Column(String(50), nullable=True)