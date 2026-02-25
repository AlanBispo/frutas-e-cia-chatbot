from pydantic import BaseModel, ConfigDict
from schemas.produto import ProdutoResponse

class OfertaBase(BaseModel):
    preco_oferta: float

class OfertaCreate(OfertaBase):
    produto_id: int

class OfertaResponse(OfertaBase):
    id: int
    produto_id: int
    produto: ProdutoResponse 

    model_config = ConfigDict(from_attributes=True)