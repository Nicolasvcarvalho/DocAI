"""secretarios iniciais

Revision ID: 94fd7381d358
Revises: f25f44d431e0
Create Date: 2026-06-13 04:55:51.688622

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import date

# revision identifiers, used by Alembic.
revision: str = '94fd7381d358'
down_revision: Union[str, Sequence[str], None] = 'f25f44d431e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    usuarios = sa.table(
        'usuarios',
        sa.column('nome', sa.String),
        sa.column('sobrenome', sa.String),
        sa.column('tipo_usuario', sa.String),
        sa.column('email', sa.String),
        sa.column('senha_hash', sa.String),
        sa.column('cpf', sa.String),
        sa.column('data_nascimento', sa.Date)
    )

    op.bulk_insert(usuarios,
        [
            {
                'nome': 'Maria',
                'sobrenome': 'Oliveira',
                'tipo_usuario': 'SECRETARIA',
                'email': 'maria@instituicao.com',
                'senha_hash': '$argon2id$v=19$m=65536,t=3,p=4$8h4DICTkXEup9X7P2bsXIg$JDI/oTv7Rb7QXdNIkilVjWwLMgPipsUmF82sQ52TUpE',
                'cpf': '12345678901',
                'data_nascimento': date(1990, 1, 1)
            },
            {
                'nome': 'João',
                'sobrenome': 'Santos',
                'tipo_usuario': 'SECRETARIA',
                'email': 'joao@instituicao.com',
                'senha_hash': '$argon2id$v=19$m=65536,t=3,p=4$8h4DICTkXEup9X7P2bsXIg$JDI/oTv7Rb7QXdNIkilVjWwLMgPipsUmF82sQ52TUpE', 
                'cpf': '23456789012',
                'data_nascimento': date(1985, 5, 2)
            },
            {
                'nome': 'Ana',
                'sobrenome': 'Costa',
                'tipo_usuario': 'SECRETARIA',
                'email': 'ana@instituicao.com',
                'senha_hash': '$argon2id$v=19$m=65536,t=3,p=4$8h4DICTkXEup9X7P2bsXIg$JDI/oTv7Rb7QXdNIkilVjWwLMgPipsUmF82sQ52TUpE',  
                'cpf': '34567890123',
                'data_nascimento': date(1992, 7, 15)
            }
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DELETE FROM usuarios
        WHERE email IN ('maria@instituicao.com','joao@instituicao.com','ana@instituicao.com')
        """
    )
