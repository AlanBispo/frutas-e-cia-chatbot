"""popula_table_frutas_loja

Revision ID: 5d1d62da9fdb
Revises: 6a933963a365
Create Date: 2026-02-24 21:32:35.714108

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision: str = '5d1d62da9fdb'
down_revision: Union[str, Sequence[str], None] = '6a933963a365'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Declarando a estrutura das tabelas
    produtos_tabela = table('produtos',
        column('nome', sa.String),
        column('descricao', sa.Text),
        column('preco', sa.Float),
        column('quantidade_estoque', sa.Integer),
        column('categoria', sa.String)
    )
    
    infos_tabela = table('informacoes_loja',
        column('chave', sa.String),
        column('valor', sa.Text)
    )

    # Inserindo estoque para a "Frutas e Cia"
    op.bulk_insert(produtos_tabela, [
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
    ])

    # Mantendo as informações da loja para contexto
    op.bulk_insert(infos_tabela, [
        {'chave': 'horario_funcionamento', 'valor': 'Funcionamos de Segunda a Sexta das 08:00 às 18:00, e Sábados das 08:00 às 12:00.'},
        {'chave': 'formas_pagamento', 'valor': 'Aceitamos PIX, Cartões de Crédito e Débito, e Dinheiro em espécie.'},
        {'chave': 'politica_entrega', 'valor': 'Entregamos em toda a cidade. O frete é fixo em R$ 5,00. Compras acima de R$ 50,00 têm frete grátis!'},
        {'chave': 'sobre_nos', 'valor': 'Somos a Frutas e Cia. Trabalhamos com produtores locais para garantir frescor e qualidade desde 2019.'}
    ])


def downgrade() -> None:
    # 1. Removemos os produtos inseridos baseado no nome
    nomes_produtos = [
        'Laranja Pera', 'Limão Taiti', 'Tangerina Ponkan', 
        'Banana Nanica', 'Manga Palmer', 'Abacaxi Pérola', 
        'Pitaya Rosa', 'Maçã Fuji', 'Pera Portuguesa', 
        'Melancia Inteira', 'Morango Bandeja', 'Uva Vitória'
    ]
    
    op.execute(
        sa.text("DELETE FROM produtos WHERE nome IN :nomes").bindparams(
            nomes=tuple(nomes_produtos)
        )
    )

    # 2. Removemos as informações da loja baseado na chave
    chaves_info = [
        'horario_funcionamento', 
        'formas_pagamento', 
        'politica_entrega', 
        'sobre_nos'
    ]
    
    op.execute(
        sa.text("DELETE FROM informacoes_loja WHERE chave IN :chaves").bindparams(
            chaves=tuple(chaves_info)
        )
    )