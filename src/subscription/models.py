from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class UserSubscription(Base):
    __tablename__ = "user_subscription"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    subscriber_id = Column(Integer, ForeignKey('user.id'), nullable=False)