from datetime import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import  Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship

from download.models import Download

from database import Base

class User(SQLAlchemyBaseUserTable[int],Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    city =  Column(String, nullable=False)
    sex = Column(String, nullable=False)
    birth_date = Column(TIMESTAMP, nullable=False)
    registered_at = Column(TIMESTAMP, default = datetime.now, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    information = relationship('Information', backref='user', uselist=False)
    download = relationship(Download, backref='user_download')
    # download = relationship('src.download.models.Download', backref='user_download')

