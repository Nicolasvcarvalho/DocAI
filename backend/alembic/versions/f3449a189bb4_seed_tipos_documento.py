"""seed tipos documento

Revision ID: f3449a189bb4
Revises: 30bc9bee621e
Create Date: 2026-05-15 10:41:16.977001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3449a189bb4'
down_revision: Union[str, Sequence[str], None] = '30bc9bee621e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute("""
        INSERT INTO tipos_documento (nome, obrigatorio_base, exige_maioridade, sexo_obrigatorio, ativo)
        VALUES 
            ('RG', true, false, NULL, true),
            ('CPF', true, false, NULL, true),
            ('Comprovante de Endereço', true, false, NULL, true),
            ('Histórico Escolar', false, false, NULL, false),
            ('Título de Eleitor', false, true, NULL, false),
            ('Documento Militar', false, true, 'MASCULINO', false)
""")


def downgrade() -> None:

    op.execute("""
        DELETE FROM tipos_documento
        WHERE nome in ('RG', 'CPF', 'Comprovante de Endereço', 'Histórico Escolar', 'Título de Eleitor', 'Documento Militar')
""")
