"""tipos documentais iniciais

Revision ID: 8f8fbbac188f
Revises: 164399dd5ee8
Create Date: 2026-06-20 12:36:33.889486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f8fbbac188f'
down_revision: Union[str, Sequence[str], None] = '164399dd5ee8'
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
