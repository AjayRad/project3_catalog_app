# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from dbsetup import ProdCat, Base, ProdItem, User
from catalog_dao import get_all_categories, get_catg_by_id, get_products_by_catg, get_all_users
'''

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

session.query(ProdCat).delete(synchronize_session=False)
session.query(User).delete(synchronize_session=False)
session.query(ProdItem).delete(synchronize_session=False)

new_ProdCat1 = ProdCat(name="Soccer", desc="the beautiful game")
session.add(new_ProdCat1)
session.commit()
print "added new product category"

new_ProdCat2 = ProdCat(name="Tennis", desc="Serve, volley and more")
session.add(new_ProdCat2)
session.commit()
print "added new product category"

new_ProdCat3 = ProdCat(name="Football", desc="The ball is a foot long")
session.add(new_ProdCat3)
session.commit()
print "added new product category"

new_user = User(social_id="tst123", nickname="tst123", email="test@yahoo.com")
session.add(new_user)
session.commit()
print "added new tst user"


new_ProdItem1 = ProdItem(prdname="Soccer ball", prd_desc="Machined-stitched",
                         price=10, prod_category=new_ProdCat1)
session.add(new_ProdItem1)
session.commit()

new_ProdItem2 = ProdItem(prdname="Soccer cleats", prd_desc="Best cleats ever",
                         price=60, prod_category=new_ProdCat1)
session.add(new_ProdItem2)
session.commit()

new_ProdItem3 = ProdItem(prdname="Soccer gloves", prd_desc="goalkeeper gloves",
                         price=35, prod_category=new_ProdCat1)
session.add(new_ProdItem3)
session.commit()

new_ProdItem4 = ProdItem(prdname="Tennis racquet", prd_desc="light & powerful",
                         price=89, prod_category=new_ProdCat2)
session.add(new_ProdItem4)
session.commit()

new_ProdItem5 = ProdItem(prdname="tennis balls", prd_desc="3 hardcourt balls",
                         price=12.00, prod_category=new_ProdCat2)
session.add(new_ProdItem5)
session.commit()

new_ProdItem6 = ProdItem(prdname="Helmet", prd_desc="Protect your head",
                         price=120, prod_category=new_ProdCat3)
session.add(new_ProdItem6)
session.commit()
'''

all_categories = get_all_categories()
for category in all_categories:
    print category.name, category.id

one_category = get_catg_by_id(1)
print one_category.name, one_category.id

all_items = get_products_by_catg(2)
for item in all_items:
    print item.prdname, item.prd_desc, item.id

users = get_all_users()
print "users:"
for user in users:
    print user.email
    print user.id
    print user.social_id
