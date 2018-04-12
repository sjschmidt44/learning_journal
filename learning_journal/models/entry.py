# NOTE: Made significant changes here

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
    ForeignKey,
)

from .meta import Base


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    account_id = Column(Text, ForeignKey('accounts.username'), nullable=False)
    title = Column(Text, nullable=False, unique=True)
    author = Column(String(255))
    body = Column(Text)
    date = Column(DateTime)


Index('entry_index', Entry.id, unique=True, mysql_length=255)
