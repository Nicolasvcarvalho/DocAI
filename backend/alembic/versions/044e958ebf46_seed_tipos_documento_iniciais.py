"""seed tipos_documento iniciais

Revision ID: 044e958ebf46
Revises: 790eb114810d
Create Date: 2026-05-23 10:06:50.089191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '044e958ebf46'
down_revision: Union[str, Sequence[str], None] = '790eb114810d'
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
