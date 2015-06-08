from flask import render_template, url_for, request, redirect, flash
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.login import current_user, LoginManager
from catalogapp import app
from models import catalog_dao
from oauth import OAuthSignIn


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


@lm.user_loader
def load_user(id):
    return catalog_dao.get_user_by_id(int(id))


@app.route('/')
@app.route('/index')
@app.route('/catalog')
def get_catalog():
    all_categories = catalog_dao.get_all_categories()
    return render_template("index.html",
                           title='Product Catalog',
                           all_categories=all_categories)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # g is Flask's global object
    # if g.user is not None and g.user.is_authenticated():
    #   return redirect(url_for('index'))
    # if current_user is not None and current_user.is_authenticated():
    #    return redirect(url_for('get_catalog'))
    return render_template('base.html',
                           title='Sign In')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_catalog'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    # Flask-Login function
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    print social_id
    print email
    if social_id is None or email is None:
        # I need a valid email address for my user identification
        flash('Authentication failed.')
        return redirect(url_for('get_catalog'))
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
    return redirect(url_for('get_catalog'))


@app.route('/catalog/<int:category_id>/products')
def products_by_catg(category_id):
    products = catalog_dao.get_products_by_catg(category_id)
    return render_template('products.html', products=products)


@app.route('/catalog/<int:category_id>/products/add',
           methods=['GET', 'POST'])
@login_required
def add_product(category_id):
    if request.method == 'POST':
        if request.form['name']:
            product_name_new = request.form['name']
        if request.form['prd_desc']:
            product_desc_new = request.form['prd_desc']
        if request.form['price']:
            product_price_new = request.form['price']
        success = (catalog_dao.add_product(category_id,
                   product_name_new, product_desc_new, product_price_new))
        if success:
            flash(" Success ! : Product Added ")
            return (redirect(url_for('products_by_catg',
                    category_id=category_id)))
    else:
        return (render_template('add_product.html',
                category_id=category_id))


@app.route('/catalog/<int:category_id>/products/<int:product_id>')
def get_product_details(category_id, product_id):
    product_details = catalog_dao.get_product_details(category_id, product_id)
    return (render_template('product_details.html',
            product_details=product_details))


@app.route('/catalog/<int:category_id>/products/<int:product_id>/edit',
           methods=['GET', 'POST'])
@login_required
def edit_product_details(category_id, product_id):
    if request.method == 'POST':
        if request.form['name']:
            product_name_new = request.form['name']
        if request.form['prd_desc']:
            product_desc_new = request.form['prd_desc']
        if request.form['price']:
            product_price_new = request.form['price']
        success = (catalog_dao.update_product_details(category_id, product_id,
                   product_name_new, product_desc_new, product_price_new))
        if success:
            flash(" Success ! : Product Updated ")
            return (redirect(url_for('get_product_details',
                    category_id=category_id, product_id=product_id)))
    else:
        return (render_template('edit_product_details.html',
                category_id=category_id, product_id=product_id))


@app.route('/catalog/<int:category_id>/products/<int:product_id>/delete',
           methods=['GET', 'POST'])
@login_required
def del_product_details(category_id, product_id):
    if request.method == 'POST':
        success = catalog_dao.del_product_details(category_id, product_id)
        if success:
            flash(" Success ! : Product deleted ")
            return (redirect(url_for('products_by_catg',
                    category_id=category_id)))
    else:
        return (render_template('del_product_details.html',
                category_id=category_id, product_id=product_id))