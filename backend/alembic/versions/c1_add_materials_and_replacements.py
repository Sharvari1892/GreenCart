"""Add materials, purchase_url, is_sustainable, and product_replacements table

Revision ID: c1_add_materials_and_replacements
Revises: 8ad2d531a51e
Create Date: 2026-10-31 23:25:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c1_materials_replacements'
down_revision = '8ad2d531a51e'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add new product columns
    with op.batch_alter_table('products') as batch_op:
        batch_op.add_column(sa.Column('materials', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('purchase_url', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('source_verification_status', sa.String(), server_default='unverified', nullable=False))
        batch_op.add_column(sa.Column('is_sustainable', sa.Boolean(), server_default=sa.text('false'), nullable=False))

    # Create product_replacements table
    op.create_table(
        'product_replacements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('original_product_id', sa.Integer(), nullable=False),
        sa.Column('replacement_product_id', sa.Integer(), nullable=False),
        sa.Column('replacement_type', sa.String(), nullable=False),
        sa.Column('reason', sa.String(), nullable=False),
        sa.Column('main_change', sa.String(), nullable=False),
        sa.Column('known_limitations', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['original_product_id'], ['products.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['replacement_product_id'], ['products.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_replacements_id'), 'product_replacements', ['id'], unique=False)
    op.create_index(op.f('ix_product_replacements_original_product_id'), 'product_replacements', ['original_product_id'], unique=False)
    op.create_index(op.f('ix_product_replacements_replacement_product_id'), 'product_replacements', ['replacement_product_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_product_replacements_replacement_product_id'), table_name='product_replacements')
    op.drop_index(op.f('ix_product_replacements_original_product_id'), table_name='product_replacements')
    op.drop_index(op.f('ix_product_replacements_id'), table_name='product_replacements')
    op.drop_table('product_replacements')

    with op.batch_alter_table('products') as batch_op:
        batch_op.drop_column('is_sustainable')
        batch_op.drop_column('purchase_url')
        batch_op.drop_column('materials')
