# database/models.py
"""
SQLAlchemy ORM models for the Personal Finance Categorizer.
Defines the database schema and relationships between different entities
such as transactions, categories, payees, and accounts.
"""
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Constants
CATEGORIES_ID = 'categories.id'

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    institution = Column(String)
    bank_identifier = Column(String, unique=True)

    transactions = relationship('Transaction', back_populates='account')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey(CATEGORIES_ID), nullable=True)

    parent = relationship('Category', remote_side=[id])
    split_transactions = relationship('SplitTransaction', back_populates='category')

class Payee(Base):
    __tablename__ = 'payees'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    transactions = relationship('Transaction', back_populates='payee')
    orders = relationship('Order', back_populates='payee')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    order_id = Column(String, unique=True, nullable=False)
    order_date = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)
    payee_id = Column(Integer, ForeignKey('payees.id'), nullable=False)

    payee = relationship('Payee', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order')
    order_payments = relationship('OrderPayment', back_populates='order')

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    item_description = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey(CATEGORIES_ID), nullable=False)
    item_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    order = relationship('Order', back_populates='order_items')
    category = relationship('Category')

class OrderPayment(Base):
    __tablename__ = 'order_payments'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    payment_amount = Column(Float, nullable=False)

    order = relationship('Order', back_populates='order_payments')
    transaction = relationship('Transaction')

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    transaction_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    payee_id = Column(Integer, ForeignKey('payees.id'))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    description = Column(String)
    
    payee = relationship('Payee', back_populates='transactions')
    account = relationship('Account', back_populates='transactions')
    split_transactions = relationship('SplitTransaction', back_populates='transaction')

class SplitTransaction(Base):
    __tablename__ = 'transaction_splits'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    allocated_amount = Column(Float, nullable=False)
    
    transaction = relationship('Transaction', back_populates='split_transactions')
    category = relationship('Category', back_populates='split_transactions')
