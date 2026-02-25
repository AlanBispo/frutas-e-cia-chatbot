import asyncio
import logging
from sqlalchemy import select
from database.config import AsyncSessionLocal
from models.produto import Produto
from models.oferta import Oferta
from models.informacao import InformacaoLoja
# Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed_data():
    async with AsyncSessionLocal() as db:
        logger.info("Iniciando o povoamento do banco de dados...")

        infos_loja = [
            {'chave': 'horario_funcionamento', 'valor': 'Funcionamos de Segunda a Sexta das 08:00 às 18:00, e Sábados das 08:00 às 12:00.'},
            {'chave': 'formas_pagamento', 'valor': 'Aceitamos PIX, Cartões de Crédito e Débito, e Dinheiro em espécie.'},
            {'chave': 'politica_entrega', 'valor': 'Entregamos em toda a cidade. O frete é fixo em R$ 5,00. Compras acima de R$ 50,00 têm frete grátis!'},
            {'chave': 'sobre_nos', 'valor': 'Somos a Frutas e Cia. Trabalhamos com produtores locais para garantir frescor e qualidade desde 2019.'}
        ]

        for info in infos_loja:
            query = await db.execute(select(InformacaoLoja).where(InformacaoLoja.chave == info['chave']))
            if not query.scalar_one_or_none():
                nova_info = InformacaoLoja(**info)
                db.add(nova_info)
                logger.info(f"Informação adicionada: {info['chave']}")
        # Lista de Produtos de Exemplo
        produtos_exemplo = [
            # Cítricas
            {'nome': 'Laranja Pera', 'descricao': 'Laranja doce e suculenta, excelente para sucos naturais e vitaminas.', 'preco': 2.50, 'quantidade_estoque': 100, 'categoria': 'Cítricas'},
            {'nome': 'Limão Taiti', 'descricao': 'Limão com bastante caldo, ideal para temperos e limonadas.', 'preco': 0.80, 'quantidade_estoque': 200, 'categoria': 'Cítricas'},
            {'nome': 'Tangerina Ponkan', 'descricao': 'Fácil de descascar, muito doce e perfeita para o lanche da tarde.', 'preco': 3.20, 'quantidade_estoque': 80, 'categoria': 'Cítricas'},
            
            # Tropicais e Exóticas
            {'nome': 'Banana Nanica', 'descricao': 'Banana no ponto ideal para consumo rápido, docinha e rica em potássio.', 'preco': 1.80, 'quantidade_estoque': 150, 'categoria': 'Tropicais'},
            {'nome': 'Manga Palmer', 'descricao': 'Manga carnuda, sem fiapos e extremamente doce.', 'preco': 4.50, 'quantidade_estoque': 60, 'categoria': 'Tropicais'},
            {'nome': 'Abacaxi Pérola', 'descricao': 'Abacaxi grande e maduro, direto do produtor.', 'preco': 7.00, 'quantidade_estoque': 30, 'categoria': 'Tropicais'},
            {'nome': 'Pitaya Rosa', 'descricao': 'Fruta exótica com polpa vibrante, refrescante e muito nutritiva.', 'preco': 15.00, 'quantidade_estoque': 15, 'categoria': 'Exóticas'},
            
            # Pomar e Melancia/Melão
            {'nome': 'Maçã Fuji', 'descricao': 'Maçã super crocante, fresca e docinha, ótima para saladas de frutas.', 'preco': 3.50, 'quantidade_estoque': 40, 'categoria': 'Pomar'},
            {'nome': 'Pera Portuguesa', 'descricao': 'Textura macia e sabor delicado que derrete na boca.', 'preco': 5.90, 'quantidade_estoque': 25, 'categoria': 'Pomar'},
            {'nome': 'Melancia Inteira', 'descricao': 'Melancia grande (aprox. 8kg), muito vermelha e refrescante.', 'preco': 22.00, 'quantidade_estoque': 10, 'categoria': 'Melancia e Melão'},
            
            # Frutas Vermelhas e Uvas
            {'nome': 'Morango Bandeja', 'descricao': 'Morangos selecionados, vermelhos e sem agrotóxicos.', 'preco': 8.00, 'quantidade_estoque': 20, 'categoria': 'Frutas Vermelhas'},
            {'nome': 'Uva Vitória', 'descricao': 'Uva preta sem semente, muito doce e prática para crianças.', 'preco': 9.50, 'quantidade_estoque': 45, 'categoria': 'Uvas'}
        ]

        for p_data in produtos_exemplo:
            # Verifica se o produto já existe para não duplicar
            query = await db.execute(select(Produto).where(Produto.nome == p_data["nome"]))
            if not query.scalar_one_or_none():
                novo_p = Produto(**p_data)
                db.add(novo_p)
                logger.info(f"Produto adicionado: {p_data['nome']}")
        
        await db.commit()

        # Oferta de Exemplo
        query_manga = await db.execute(select(Produto).where(Produto.nome == "Manga Palmer"))
        manga = query_manga.scalar_one_or_none()

        if manga:
            query_oferta = await db.execute(select(Oferta).where(Oferta.produto_id == manga.id))
            if not query_oferta.scalar_one_or_none():
                nova_oferta = Oferta(produto_id=manga.id, preco_oferta=3.90, ativa=True)
                db.add(nova_oferta)
                logger.info(f"Oferta criada para: {manga.nome}")
        
        await db.commit()
        logger.info("Seed finalizado com sucesso! 🍎🍊")

if __name__ == "__main__":
    asyncio.run(seed_data())