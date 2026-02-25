from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from database.config import Base
from sqlalchemy.orm import relationship

class Oferta(Base):
    __tablename__ = "ofertas"
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    preco_oferta = Column(Float)
    texto_chamada = Column(String(255))
    ativa = Column(Boolean, default=True)
    produto = relationship("Produto")