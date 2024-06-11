from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.dialects.postgresql import ARRAY


class Information(Base):
    __tablename__ = "information"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    email = Column(String, nullable=False)
    technology = Column(ARRAY(String), nullable=False)
    tg = Column(String, nullable=False)
    vk = Column(String, nullable=False)
    education = Column(String, nullable=False)
    work = Column(String, nullable=False)