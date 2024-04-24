from sqlalchemy import Column, Integer, MetaData, String, ForeignKey
from sqlalchemy.orm import relationship
from auth.models import UserBase

metaData = MetaData()

InformationBase = UserBase

class Information(InformationBase):
    __tablename__ = "information"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    additional_information = Column(String, nullable=False)
    telegram = Column(String, nullable=False)
    vkontakte = Column(String, nullable=False)
    education = Column(String, nullable=False)
    work = Column(String, nullable=False)
    # , unique=True
    # user = relationship('User', backref='information')
