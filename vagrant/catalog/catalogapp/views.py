from flask import render_template, url_for, request, redirect, flash, jsonify
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.login import current_user, LoginManager
from catalogapp import app
from models import catalog_dao
from oauth import OAuthSignIn
from functools import wraps


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


@lm.user_loader
def load_user(id):
    return catalog_dao.get_user_by_id(int(id))


def has_permission(func_check):
    """
    decorator checks whether user has permission to add/update/del
    products in a category
    """
    @wraps(func_check)
    def wrapped_f(*args, **kwargs):
        category_id = kwargs['category_id']
        category_details = catalog_dao.get_catg_by_id(category_id)
        if category_details.owner_id != int(current_user.get_id()):
            flash('Only category owners can add/update/delete products .')
            flash('For permission, please contact admin@bas.com')
            return redirect(url_for('get_categories'))
        else:
            return func_check(*args, **kwargs)
    return wrapped_f


# Flasks error handler decorators
@app.errorhandler(404)
def not_found_error(error):
    return render_template('Err_404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('Err_500.html'), 500


@app.route('/')
@app.route('/index')
@app.route('/catalog')
def get_categories():
    ''' main index page;
    gets & renders all categories & featured product from DB.'''
    all_categories = catalog_dao.get_all_categories()
    is_feat = True
    products = catalog_dao.get_featured_products(is_feat)
    return render_template("index.html",
                           title='Product Catalog',
                           products=products,
                           all_categories=all_categories)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url_for('get_categories'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_categories'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    # Flask-Login function
    if not current_user.is_anonymous():
        return redirect(url_for('get_categories'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('get_categories'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    print social_id
    print email
    if social_id is None or email is None:
        # Need a valid email address for my user identification
        flash('Authentication failed.')
        return redirect(url_for('get_categories'))
    # Look if the user already exists
    user = catalog_dao.get_user(email)
    if not user:
        # Create the user. Try and use their name returned by provider,
        # but if it is not set, split the email address at the @.
        nickname = username
        if nickname is None or nickname == "":
            nickname = email.split('@')[0]
        success = catalog_dao.add_user(social_id, nickname, email)
        print success
        if success:
            user = catalog_dao.get_user(email)
    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(user, remember=True)
    return redirect(url_for('get_categories'))


@app.route('/catalog/<int:category_id>/products')
def products_by_catg(category_id):
    ''' get & render product for a particular categoty.
    Input needed: category_id'''
    products = catalog_dao.get_products_by_catg(category_id)
    all_categories = catalog_dao.get_all_categories()
    return render_template('products.html',
                           products=products,
                           category_id=category_id,
                           all_categories=all_categories)


@app.route('/catalog/add',
           methods=['GET', 'POST'])
@login_required
def add_category():
    ''' Allows user to add a category to catalog.
    User needs to be logged in.
    Will be setup of the owner for this category
    Input param: none/blank
    '''
    # Capture category details entered on form
    if request.method == 'POST':
        if request.form['name']:
            catg_name_new = request.form['name']
        if request.form['desc']:
            catg_desc_new = request.form['desc']
        catg_owner_id = int(current_user.get_id())
        # Call add catg query in catalog_dao with given data
        success = (catalog_dao.add_category(catg_name_new, catg_desc_new,
                   catg_owner_id))
        if success:
            flash(" Success ! : Category Added. You are the Category Owner")
        else:
            flash("OOPS! did not add category. db error. Contact admin")
        return (redirect(url_for('get_categories')))
    else:
        return (render_template('add_category.html'))


@app.route('/catalog/<int:category_id>/products/add',
           methods=['GET', 'POST'])
@login_required
@has_permission
def add_product(category_id):
    ''' Allows user to add products for a category.
    User needs to be logged in. And
    have permissions for that category i.e. (be the category owner).
    both checks implemented using decorators.
    Input param : category_id '''
    product_feat_new = None
    product_name_new = None
    product_desc_new = None
    product_price_new = None
    # Capture product details entered on form
    if request.method == 'POST':
        if request.form['name']:
            product_name_new = request.form['name']
        if request.form['prd_desc']:
            product_desc_new = request.form['prd_desc']
        if request.form['price']:
            product_price_new = request.form['price']
        if request.form['feat']:
            product_feat_new = (True if request.form['feat'] == 'True'
                                else False)
        # Call add query in catalog_dao with given data
        success = (catalog_dao.add_product(category_id,
                   product_name_new, product_desc_new, product_price_new,
                   product_feat_new))
        if success:
            flash(" Success ! : Product Added ")
        else:
            flash("OOPS! did not add product. db error. Contact admin")
        return (redirect(url_for('products_by_catg',
                                 category_id=category_id)))
    else:
        return (render_template('add_product.html',
                category_id=category_id))


@app.route('/catalog/<int:category_id>/products/<int:product_id>')
def get_product_details(category_id, product_id):
    product_details = catalog_dao.get_product_details(category_id, product_id)
    all_categories = catalog_dao.get_all_categories()
    return (render_template('product_details.html',
            product_details=product_details,
            all_categories=all_categories))


@app.route('/catalog/<int:category_id>/products/<int:product_id>/edit',
           methods=['GET', 'POST'])
@login_required
@has_permission
def edit_product_details(category_id, product_id):
    ''' Allows user to edit product details.
    User needs to be logged in. And
    have permissions for that category i.e. (be the category owner).
    both checks implemented using decorators.
    Input param : category_id , product_id'''
    product_feat_new = None
    product_name_new = None
    product_desc_new = None
    product_price_new = None
    # Capture product details from form
    if request.method == 'POST':
        if request.form['name']:
            product_name_new = request.form['name']
        if request.form['prd_desc']:
            product_desc_new = request.form['prd_desc']
        if request.form['price']:
            product_price_new = request.form['price']
        if request.form['feat']:
            product_feat_new = (True if request.form['feat'] == 'True'
                                else False)
        # call update methods in catalog_dao
        success = (catalog_dao.update_product_details(category_id, product_id,
                   product_name_new, product_desc_new, product_price_new,
                   product_feat_new))
        if success:
            flash(" Success ! : Product Updated ")
        else:
            flash(" OOPS!Did not update: Db error. Please contact admin")
        return (redirect(url_for('get_product_details',
                                 category_id=category_id,
                                 product_id=product_id)))
    else:
        product_details = catalog_dao.get_product_details(category_id,
                                                          product_id)
        return (render_template('edit_product_details.html',
                category_id=category_id, product_details=product_details,
                product_id=product_id))


@app.route('/catalog/<int:category_id>/products/<int:product_id>/delete',
           methods=['GET', 'POST'])
@login_required
@has_permission
def del_product_details(category_id, product_id):
    ''' Allows user to delete products for a category.
    User needs to be logged in. And
    have permissions for that category i.e. (be the category owner).
    both checks implemented using decorators.
    Input param : category_id, product_id '''
    if request.method == 'POST':
        success = catalog_dao.del_product_details(category_id, product_id)
        if success:
            flash(" Success ! : Product deleted ")
            return (redirect(url_for('products_by_catg',
                    category_id=category_id)))
    else:
        return (render_template('del_product_details.html',
                category_id=category_id, product_id=product_id))


# JSON endpoint for all categories
@app.route('/catalog/categories/JSON')
def get_categoriesjson():
    all_categories = catalog_dao.get_all_categories()
    return jsonify(Categories=[i.serialize for i in all_categories])


# JSON endpoint for all products within a category_id
@app.route('/catalog/<int:category_id>/products/JSON')
def products_by_catgjson(category_id):
    products = catalog_dao.get_products_by_catg(category_id)
    return jsonify(ProductItems=[i.serialize for i in products])
