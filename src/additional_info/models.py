from sqlalchemy import ForeignKey, Table, Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from database import Base

from src.auth.models import metaData as metadata_auth

metadata = metadata_auth

information = Table(
    "information",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("additional_information", String, nullable=True),
    Column("telegram", String, nullable=True),
    Column("vkontakte", String, nullable=True),
    Column("telephone", String, nullable=True),
)
