from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DATE, MetaData
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base(metadata=MetaData(schema="ecommerce"))


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer,
                         primary_key=True,
                         nullable=False)
    password = Column(String)
    name = Column(String)
    phone = Column(String)
    address = Column(String)
    email = Column(String)
    username = Column(String)


class Products(Base):
    __tablename__ = "products"

    product_id = Column(Integer,
                        primary_key=True,
                        nullable=False)
    description = Column(String)
    category = Column(String)
    name = Column(String)
    price = Column(DECIMAL)
    quantity = Column(Integer)
    created_time = Column(DATE)


class Cart(Base):
    __tablename__ = "cart"

    customer_id = Column(Integer,
                         ForeignKey("customers.customer_id"),
                         nullable=False)
    cart_id = Column(Integer,
                     primary_key=True,
                     nullable=False)

    cart_items = relationship("CartItems")


class CartItems(Base):
    __tablename__ = "cart_items"

    cart_id = Column(Integer,
                     ForeignKey("cart.cart_id"),
                     nullable=False)
    product_name = Column(String)
    cart_items_id = Column(Integer,
                           primary_key=True,
                           nullable=False)
    product_id = Column(Integer,
                        ForeignKey("products.product_id"),
                        nullable=False)
    total_price = Column(DECIMAL)
    quantity = Column(Integer)
    price = Column(DECIMAL)


class Orders(Base):
    __tablename__ = "orders"

    order_id = Column(Integer,
                      primary_key=True,
                      nullable=False)
    customer_id = Column(Integer,
                         ForeignKey("customers.customer_id"),
                         nullable=False)
    total_amount = Column(DECIMAL)
    status = Column(String)
    time_open = Column(DATE)

    order_items = relationship("OrderItems")


class OrderItems(Base):
    __tablename__ = "order_items"
    product_id = Column(Integer,
                        ForeignKey("products.product_id"),
                        nullable=True
                        )

    product_name = Column(String)
    quantity = Column(Integer)
    price = Column(DECIMAL)
    total_price = Column(DECIMAL)
    order_id = Column(Integer,
                      ForeignKey("orders.order_id"),
                      nullable=True)
    order_items_id = Column(Integer,
                            primary_key=True,
                            nullable=False)
