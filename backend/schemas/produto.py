from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    quantidade_estoque: int

# Criação
class ProdutoCreate(ProdutoBase):
    pass

# Atualização (campos opcionais)
class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = None
    quantidade_estoque: Optional[int] = None

# Resposta 
class ProdutoResponse(ProdutoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)