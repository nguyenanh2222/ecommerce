from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    password = Column(String)
    name = Column(String)
    phone = Column(String)
    address = Column(String)
    email = Column(String)
    username = Column(String)

    class Config:
        arbitrary_types_allowed = True


    # def __repr__(self):
    #     return """<Customer(password='%s',
    #     name='%s', phone='%s', address='%s',
    #     email='%s', username='%s')>""" % (
    #     self.name, self.sex, self.clas,
    #     self.grade, self.email, self.username)
