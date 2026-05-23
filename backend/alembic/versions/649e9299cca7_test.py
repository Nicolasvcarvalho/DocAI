"""
seed: inserir categorias e tipos de documento iniciais

Revision ID: 649e9299cca7
Revises: b4a578e1ea6d
Create Date: 2026-05-22 22:26:00.455403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '649e9299cca7'
down_revision: Union[str, Sequence[str], None] = 'b4a578e1ea6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.execute("""
        INSERT INTO categorias_documento (id, nome)
        VALUES
            (1, 'IDENTIFICACAO'),
            (2, 'ENDERECO')
    """)

    op.execute("""
        INSERT INTO tipos_documento (
            nome,
            obrigatorio_base,
            exige_maioridade,
            sexo_obrigatorio,
            ativo,
            categoria_id
        )
        VALUES
            ('RG', true, false, NULL, true, 1),
            ('CPF', true, false, NULL, true, 1),
            ('Comprovante de Endereço', true, false, NULL, true, 2)
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DELETE FROM tipos_documento
        WHERE nome IN (
            'RG',
            'CPF',
            'Comprovante de Endereço'
        )
    """)

    op.execute("""
        DELETE FROM categorias_documento
        WHERE id IN (1, 2)
    """)
