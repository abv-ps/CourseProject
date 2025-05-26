"""initial tables: authors, books, authorbooklink"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20240512_01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Таблиця authors
    op.create_table(
        'authors',
        sa.Column('author_id', sa.Integer, primary_key=True),
        sa.Column('author_name', sa.String(), nullable=False),
    )

    # Таблиця books
    op.create_table(
        'books',
        sa.Column('book_id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
    )

    # Зв’язуюча таблиця authorbooklink
    op.create_table(
        'authorbooklink',
        sa.Column('author_id', sa.Integer, sa.ForeignKey('authors.author_id', ondelete="CASCADE"), primary_key=True),
        sa.Column('book_id', sa.Integer, sa.ForeignKey('books.book_id', ondelete="CASCADE"), primary_key=True),
    )


def downgrade():
    op.drop_table('authorbooklink')
    op.drop_table('books')
    op.drop_table('authors')
