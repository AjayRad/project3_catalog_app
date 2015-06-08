from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import ProdCat, Base, ProdItem, User


def db_init():
    engine = create_engine('sqlite:///catalogapp/models/catalog.db')
    # engine = create_engine('sqlite:///catalog.db')
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
    session1 = db_init()
    all_categories = session1.query(ProdCat).all()
    return all_categories


def get_catg_by_id(category_id):
    session2 = db_init()
    category_details = (session2.query(ProdCat).
                        filter(ProdCat.id == category_id).first())
    return category_details


def get_products_by_catg(category_id):
    session = db_init()
    category_details = get_catg_by_id(category_id)
    products = (session.query(ProdItem).
                filter(ProdItem.prod_category == category_details).all())
    return products


def get_product_details(category_id, product_id):
    session = db_init()
    product_details = (session.query(ProdItem).
                       filter(ProdItem.id == product_id and ProdItem.prdcat_id
                              == category_id).all())
    return product_details


def update_product_details(category_id, product_id,
                           product_name_new, product_desc_new,
                           product_price_new):
    session = db_init()
    cur_product_det = (session.query(ProdItem).
                       filter(ProdItem.id == product_id
                              and ProdItem.prdcat_id == category_id).first())
    cur_product_det.prdname = product_name_new
    cur_product_det.prd_desc = product_desc_new
    cur_product_det.price = product_price_new
    success = True
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        success = False
    return success


def add_product(category_id, product_name_new, product_desc_new,
                product_price_new):
    session = db_init()
    new_product = ProdItem(prdname=product_name_new, prd_desc=product_desc_new,
                           price=product_price_new, num_in_stock=1,
                           prdcat_id=category_id)
    session.add(new_product)
    success = True
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        success = False
    return success


def del_product_details(category_id, product_id):
    session = db_init()
    session.query(ProdItem).filter(ProdItem.id == product_id and
                                   ProdItem.prdcat_id == category_id).delete(synchronize_session=False)
    success = True
    try:
        session.commit()
    except Exception as e:
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
    print "in add user"
    print nickname, email
    session = db_init()
    new_user = User(social_id=social_id, nickname=nickname, email=email)
    session.add(new_user)
    success = True
    try:
        session.commit()
    except Exception as e:
        print e
        session.rollback()
        session.flush()
        success = False
    return success
