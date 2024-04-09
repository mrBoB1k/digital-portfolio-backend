from sqlalchemy import Column, Integer, MetaData, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from auth.models import UserBase
from database import Base

metaData = MetaData()

# InformationBase = declarative_base(metadata=metaData)
InformationBase = UserBase

class Information(InformationBase):
    __tablename__ = "information"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True, nullable=False)
    additional_information = Column(String, nullable=False)
    telegram = Column(String, nullable=False)
    vkontakte = Column(String, nullable=False)
    education = Column(String, nullable=False)
    work = Column(String, nullable=False)

    user = relationship('User', backref='information')


# information = Table(
#     "information",
#     metadata,
#     Column("user_id", Integer, primary_key=True),
#     Column("additional_information", String, nullable=True),
#     Column("telegram", String, nullable=True),
#     Column("vkontakte", String, nullable=True),
#     Column("telephone", String, nullable=True),
# )
