"""add_table_ofertas

Revision ID: 6a51a0f8d0c6
Revises: 8f066d9df4f0
Create Date: 2026-02-25 02:39:51.376492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision: str = '6a51a0f8d0c6'
down_revision: Union[str, Sequence[str], None] = '8f066d9df4f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('ofertas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('produto_id', sa.Integer(), nullable=True),
        sa.Column('preco_oferta', sa.Float(), nullable=True),
        sa.Column('texto_chamada', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['produto_id'], ['produtos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ofertas_id'), 'ofertas', ['id'], unique=False)


    ofertas_table = table('ofertas',
        column('id', sa.Integer),
        column('produto_id', sa.Integer),
        column('preco_oferta', sa.Float),
        column('texto_chamada', sa.String)
    )

    op.bulk_insert(ofertas_table, [
        {'id': 1, 'produto_id': 1, 'preco_oferta': 5.99, 'texto_chamada': 'Promoção Relâmpago!'},
        {'id': 2, 'produto_id': 3, 'preco_oferta': 10.00, 'texto_chamada': 'Oferta de Verão!'}
    ])

def downgrade() -> None:
    # Remove o índice e a tabela
    op.drop_index(op.f('ix_ofertas_id'), table_name='ofertas')
    op.drop_table('ofertas')