from sqlalchemy import ForeignKey, Table, Column, Integer, String, TIMESTAMP, MetaData
from sqlalchemy.orm import relationship

from database import Base

metadata = MetaData()

information = Table(
    "information",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("additional_information", String, nullable=True),
    Column("telegram", String, nullable=True),
    Column("vkontakte", String, nullable=True),
    Column("telephone", String, nullable=True),
)
