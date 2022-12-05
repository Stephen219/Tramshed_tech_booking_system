"""merge maps migration and bookings

Revision ID: db79793b21ba
Revises: 27b7ee8c3cdd, a9b80e8b6084
Create Date: 2022-11-30 13:32:11.882572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db79793b21ba'
down_revision = ('27b7ee8c3cdd', 'a9b80e8b6084')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
