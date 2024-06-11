from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Download(Base):
    __tablename__ = "download"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    tag = Column(String, nullable=False)
    path = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    __table_args__ = {'extend_existing': True}