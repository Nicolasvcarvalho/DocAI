"""campo mime type arquivo documento

Revision ID: 89d7cab6b25f
Revises: 94fd7381d358
Create Date: 2026-06-15 22:56:19.261832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.enums.lado_documento import Lado


# revision identifiers, used by Alembic.
revision: str = '89d7cab6b25f'
down_revision: Union[str, Sequence[str], None] = '94fd7381d358'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.drop_table('arquivos_documento')

    op.create_table(
        'arquivos_documento',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('versao_documento_id', sa.Integer(), nullable=False),
        sa.Column('lado', sa.Enum(Lado), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('mime_type', sa.String(), nullable=False), 
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['versao_documento_id'], ['versoes_documento.id'], )
    )

def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_table('arquivos_documento')

    op.create_table(
        'arquivos_documento',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('versao_documento_id', sa.Integer(), nullable=False),
        sa.Column('lado', sa.Enum(Lado), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['versao_documento_id'], ['versoes_documento.id'], )
    )
