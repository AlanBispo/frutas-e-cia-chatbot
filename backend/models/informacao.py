from sqlalchemy import Column, Integer, String, Text
from database.config import Base

class InformacaoLoja(Base):
    __tablename__ = "informacoes_loja"

    id = Column(Integer, primary_key=True, index=True)
    chave = Column(String(50), unique=True, index=True, nullable=False) # Ex: 'horario_funcionamento'
    valor = Column(Text, nullable=False) # Ex: 'Segunda a Sábado, das 08:00 às 18:00'