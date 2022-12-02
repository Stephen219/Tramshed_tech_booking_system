"""merged admin changes and current changes

Revision ID: 97a9c7a7edd7
Revises: cc92ab660553, 0f14622c489d
Create Date: 2022-12-01 23:34:10.053503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97a9c7a7edd7'
down_revision = ('cc92ab660553', '0f14622c489d')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
