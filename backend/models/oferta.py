from sqlalchemy import Column, Integer, String, ForeignKey, Float
from database.config import Base

class Oferta(Base):
    __tablename__ = "ofertas"
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    preco_oferta = Column(Float)
    texto_chamada = Column(String(255))