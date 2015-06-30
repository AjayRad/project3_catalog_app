from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import ProdCat, Base, ProdItem, User
from flask import current_app
from config import SQLALCHEMY_DATABASE_URI


def db_init():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.bind = engine
    dbsession = sessionmaker(bind=engine)
    # dbsession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit().

    session = dbsession()
    return session


def get_all_categories():
    ''' returns all categories in db '''
    session1 = db_init()
    all_categories = session1.query(ProdCat).all()
    return all_categories


def get_catg_by_id(category_id):
    '''input parameter: category_id
    Returns category details in given category_id  '''
    session2 = db_init()
    category_details = (session2.query(ProdCat).
                        filter(ProdCat.id == category_id).first())
    return category_details


def get_products_by_catg(category_id):
    '''input parameter: category_id
    Returns all products in category  '''
    session = db_init()
    category_details = get_catg_by_id(category_id)
    products = (session.query(ProdItem).
                filter(ProdItem.prod_category == category_details).all())
    return products


def get_featured_products(is_feat):
    '''input parameter: boolean values True or False
    Returns 10 featured or not featured products across all categories '''
    session = db_init()
    products = (session.query(ProdItem).
                filter(ProdItem.featured == is_feat).limit(10))
    return products


def get_product_details(category_id, product_id):
    '''input parameter: category_id, product_id
    Returns all product details for a category/product_id combo  '''
    session = db_init()
    product_details = (session.query(ProdItem).
                       filter(ProdItem.id == product_id and ProdItem.prdcat_id
                              == category_id).all())
    return product_details


def add_category(catg_name_new, catg_desc_new,
                 catg_owner_id):
    '''
    mandatory input parameter: new category name.
    Optional parameters include other category details.
    SQLAlchemy query adds new category to prod_category table.
    '''
    session = db_init()
    new_catg = ProdCat(name=catg_name_new, desc=catg_desc_new,
                       owner_id=catg_owner_id)
    session.add(new_catg)
    success = True
    try:
        # Commit changes to DB
        session.commit()
    except Exception as e:
        current_app.logger.error(e, exc_info=True)
        # If commit fails, rollback changes from db
        session.rollback()
        session.flush()
        success = False
    return success


def update_product_details(category_id, product_id,
                           product_name_new=None, product_desc_new=None,
                           product_price_new=None, product_feat_new=None):
    '''mandatory input parameter: category_id, product_id.
    Optional parameters include other product details.
    SQLAlchemy query updates product details for the given product_id  '''
    session = db_init()
    cur_product_det = (session.query(ProdItem).
                       filter(ProdItem.id == product_id
                              and ProdItem.prdcat_id == category_id).first())
    if product_name_new is not None:
        cur_product_det.prdname = product_name_new
    if product_desc_new is not None:
        cur_product_det.prd_desc = product_desc_new
    if product_price_new is not None:
        cur_product_det.price = product_price_new
    if product_feat_new is not None:
        cur_product_det.featured = product_feat_new
    success = True
    try:
        # Commit updates to DB
        session.commit()
    except Exception as e:
        current_app.logger.error(e, exc_info=True)
        # rollback updates if commit fails
        session.rollback()
        session.flush()
        success = False
    return success


def add_product(category_id, product_name_new, product_desc_new=None,
                product_price_new=None, product_feat_new=None):
    '''mandatory input parameter: category_id, new product name.
    Optional parameters include other product details.
    SQLAlchemy query adds new product to prod_item table.  '''
    session = db_init()
    new_product = ProdItem(prdname=product_name_new, prd_desc=product_desc_new,
                           price=product_price_new, num_in_stock=1,
                           featured=product_feat_new,
                           prdcat_id=category_id)
    session.add(new_product)
    success = True
    try:
        # Commit changes to DB
        session.commit()
    except Exception as e:
        current_app.logger.error(e, exc_info=True)
        # If commit fails, rollback changes from db
        session.rollback()
        session.flush()
        success = False
    return success


def del_product_details(category_id, product_id):
    '''mandatory input parameter: category_id, product_id.
    SQLAlchemy query deletes product from prod_item table.  '''
    session = db_init()
    session.query(ProdItem).filter(ProdItem.id == product_id and
                                   ProdItem.prdcat_id == category_id).delete(synchronize_session=False)
    success = True
    try:
        # Commit changes to DB
        session.commit()
    except Exception as e:
        current_app.logger.error(e, exc_info=True)
        # if commit fails, rollback changes from DB
        session.rollback()
        session.flush()
        success = False
    return success


def get_all_users():
    session1 = db_init()
    all_users = session1.query(User).all()
    return all_users


def get_user(email):
    session = db_init()
    user = session.query(User).filter(User.email == email).first()
    return user


def get_user_by_id(id):
    session = db_init()
    user = session.query(User).filter(User.id == id).first()
    return user


def add_user(social_id, nickname, email):
    print nickname, email
    session = db_init()
    new_user = User(social_id=social_id, nickname=nickname, email=email)
    session.add(new_user)
    success = True
    try:
        session.commit()
    except Exception as e:
        current_app.logger.error(e)
        session.rollback()
        session.flush()
        success = False
    return success
