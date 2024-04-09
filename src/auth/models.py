from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, Boolean, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from database import Base

metaData = MetaData()

UserBase = declarative_base(metadata = metaData)

class User(UserBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    birth_date = Column(TIMESTAMP, nullable=False)
    registered_at = Column(TIMESTAMP, default = datetime.now, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    information = relationship('Information', backref='user', uselist=False)


    
# user  = Table(
#     "user",
#     metaData,
#     Column("id", Integer, primary_key=True),
#     Column("email", String, nullable=False),
#     Column("first_name", String, nullable=False),
#     Column("last_name", String, nullable=False),
#     Column("hashed_password", String, nullable=False),
#     Column("sex", String, nullable=False),
#     Column("birth_date", TIMESTAMP, nullable=False),
#     Column("registered_at", TIMESTAMP, default = datetime.now, nullable=False),
#     Column("is_active", Boolean, default=True, nullable=False),
#     Column("is_superuser", Boolean, default=False, nullable=False),
#     Column("is_verified", Boolean, default=False, nullable=False),
# )



# class User(SQLAlchemyBaseUserTable[int], Base):
#     id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False)
#     first_name = Column(String, nullable=False)
#     last_name = Column(String, nullable=False)
#     sex = Column(String, nullable=False)
#     birth_date = Column(TIMESTAMP, nullable=False)
#     registered_at = Column(TIMESTAMP, default = datetime.now, nullable=False)
#     hashed_password: str = Column(String(length=1024), nullable=False)
#     is_active: bool = Column(Boolean, default=True, nullable=False)
#     is_superuser: bool = Column(Boolean, default=False, nullable=False)
#     is_verified: bool = Column(Boolean, default=False, nullable=False)
