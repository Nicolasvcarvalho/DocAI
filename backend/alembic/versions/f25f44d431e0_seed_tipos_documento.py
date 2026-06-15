"""seed tipos documento

Revision ID: f25f44d431e0
Revises: f5a43775109f
Create Date: 2026-06-13 04:54:40.436066

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f25f44d431e0'
down_revision: Union[str, Sequence[str], None] = 'f5a43775109f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        INSERT INTO tipos_documento (
            nome,
            obrigatorio_base,
            exige_maioridade,
            sexo_obrigatorio,
            exige_frente_verso,
            ativo
        )
        VALUES
            ('DOCUMENTO_IDENTIFICACAO', true, false, NULL, true, true),
            ('COMPROVANTE_RESIDENCIA', true, false, NULL, false, true)
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DELETE FROM tipos_documento
        WHERE nome IN (
            'DOCUMENTO_IDENTIFICACAO',
            'COMPROVANTE_RESIDENCIA'
        )
    """)
