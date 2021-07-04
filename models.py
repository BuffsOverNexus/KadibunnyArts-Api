from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from database import Base


class Account(Base, SerializerMixin):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    email = Column(String(320))
    password = Column(String(64))
    admin = Column(Boolean, default=False)
    orders = relationship('Order')

    def default(self, o):
        return o.__dict__


class Order(Base, SerializerMixin):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    username = Column(String(100))
    email = Column(String(320))

    date_request = Column(DateTime, default=Date())

    status = Column(Integer, default=1)
    cost = Column(Float)
    emotes = relationship('Emote')

    twitch = Column(String(100), nullable=True)
    date_finished = Column(DateTime, default=None, nullable=True)

class Emote(Base, SerializerMixin):
    __tablename__ = 'emote'

    id = Column(Integer, primary_key=True)
    description = Column(String(1000))
    reference = Column(String(1000)) # reference photo link to imgur
    order_id = Column(Integer, ForeignKey('order.id'))
    price = Column(Float)


class Option(Base, SerializerMixin):
    __tablename__ = 'option'

    id = Column(Integer, primary_key=True)
    key = Column(String(25))
    value = Column(String(100))