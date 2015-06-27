from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask.ext.login import UserMixin
from config import SQLALCHEMY_DATABASE_URI

Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    social_id = Column(String(64), nullable=False, unique=True)
    nickname = Column(String(64), nullable=False)
    email = Column(String(64), nullable=True)


class ProdCat(Base):
    __tablename__ = 'prod_category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    desc = Column(String(250))
    owner_id = Column(Integer, ForeignKey('users.id'))
    users = relationship(User)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
        }


class ProdItem(Base):
    __tablename__ = 'prod_item'

    prdname = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    prd_desc = Column(String(250))
    price = Column(Float)
    num_in_stock = Column(Integer)
    featured = Column(Boolean, default=False)
    prdcat_id = Column(Integer, ForeignKey('prod_category.id'))
    prod_category = relationship(ProdCat)

    def __repr__(self):
        r = '<Product {:d} {} {}>'
        return r.format(self.id, self.prd_desc, self.price)

    @property
    def serialize(self):

        return {
            'name': self.prdname,
            'description': self.prd_desc,
            'id': self.id,
            'price': self.price,
            'Instock': self.num_in_stock,
            'Featured': self.featured,
        }


engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)
