"""firstmigration

Revision ID: 0cc558e6b3ed
Revises: 
Create Date: 2024-04-03 23:25:29.235416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cc558e6b3ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('lessons')
    op.drop_table('courses')
    op.drop_table('admin')
    op.drop_table('roles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('role_id', sa.INTEGER(), server_default=sa.text("nextval('roles_role_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('rname', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('role_id', name='roles_pkey'),
    sa.UniqueConstraint('rname', name='roles_rname_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('admin',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('admin_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=300), autoincrement=False, nullable=False),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.role_id'], name='admin_role_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='admin_pkey'),
    sa.UniqueConstraint('admin_id', name='admin_admin_id_key')
    )
    op.create_table('courses',
    sa.Column('cid', sa.INTEGER(), server_default=sa.text("nextval('courses_cid_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('cname', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('fee', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('ctime', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('rating', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('cid', name='courses_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('lessons',
    sa.Column('lid', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('cid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['cid'], ['courses.cid'], name='lessons_cid_fkey'),
    sa.PrimaryKeyConstraint('lid', name='lessons_pkey')
    )
    op.create_table('users',
    sa.Column('uid', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('uname', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=300), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('uid', name='users_pkey')
    )
    # ### end Alembic commands ###
