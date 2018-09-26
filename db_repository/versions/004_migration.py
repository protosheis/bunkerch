from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post_s = Table('post_s', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('body', VARCHAR(length=1800)),
    Column('timestamp', DATETIME),
    Column('trip', VARCHAR(length=10)),
    Column('ip', VARCHAR(length=39)),
    Column('thread', INTEGER),
    Column('bump', INTEGER),
    Column('sage', INTEGER),
    Column('subject', VARCHAR(length=100)),
    Column('banned', INTEGER),
    Column('locked', INTEGER),
    Column('sticky', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post_s'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post_s'].create()
