from flask import Flask, render_template, request, redirect, url_for, session, flash
import models

app = Flask(__name__)
app.secret_key = "пароль"


def check_admin():
    if 'username' in session and session['username'] == 'admin':
        return True
    return False


def require_admin(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not check_admin():
            flash('Требуются права администратора', 'error')
            return redirect(url_for('index'))
        return func(*args, **kwargs)

    return wrapper


@app.route('/')
def index():
    products = models.get_all_products()
    return render_template('index.html', products=products)


@app.route('/products')
def products_list():
    products = models.get_all_products()
    return render_template('products/list.html', products=products)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = models.get_product_by_id(product_id)
    if not product:
        flash('Товар не найден', 'error')
        return redirect(url_for('products_list'))

    categories = models.get_product_categories(product_id)
    return render_template('products/detail.html',
                           product=product,
                           categories=categories,
                           is_admin=check_admin())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if models.check_login(username, password):
            session['username'] = username
            flash(f'Вход выполнен успешно', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверные учетные данные', 'error')

    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if models.get_user(username):
            flash('Пользователь с таким именем уже существует', 'error')
        else:
            models.create_user(username, email, password)
            flash('Регистрация прошла успешно', 'success')
            return redirect(url_for('login'))

    return render_template('auth/register.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))


@app.route('/order/<int:product_id>', methods=['GET', 'POST'])
def create_order(product_id):
    if 'username' not in session:
        flash('Для оформления заказа необходимо войти в систему', 'warning')
        return redirect(url_for('login'))

    product = models.get_product_by_id(product_id)
    if not product:
        flash('Товар не найден', 'error')
        return redirect(url_for('products_list'))

    if request.method == 'POST':
        quantity = int(request.form.get('quantity', 1))
        phone = request.form.get('phone')

        user = models.get_user(session['username'])
        if not user:
            flash('Ошибка: пользователь не найден. Пожалуйста, войдите заново.', 'error')
            return redirect(url_for('login'))
        order_id = models.create_order(product_id, user['id'], quantity, phone)

        flash(f'Заказ #{order_id} оформлен успешно', 'success')
        return redirect(url_for('my_orders'))

    return render_template('products/order.html', product=product)


@app.route('/my-orders')
def my_orders():
    if 'username' not in session:
        flash('Необходима авторизация', 'warning')
        return redirect(url_for('login'))

    user = models.get_user(session['username'])
    orders = models.get_orders_by_user(user['id'])
    return render_template('orders/my_orders.html', orders=orders)


@app.route('/product/new', methods=['GET', 'POST'])
@require_admin
def new_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        image_url = request.form.get('image_url')

        user = models.get_user(session['username'])
        product_id = models.add_product(name, description, price, user['id'], image_url)

        flash('Товар добавлен успешно', 'success')
        return redirect(url_for('product_detail', product_id=product_id))

    categories = models.get_all_categories()
    return render_template('products/new.html', categories=categories)


@app.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
@require_admin
def edit_product(product_id):
    product = models.get_product_by_id(product_id)
    if not product:
        flash('Товар не найден', 'error')
        return redirect(url_for('products_list'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        image_url = request.form.get('image_url')

        models.update_product(product_id, name, description, price, image_url)
        flash('Товар обновлен успешно', 'success')
        return redirect(url_for('product_detail', product_id=product_id))

    categories = models.get_all_categories()
    product_categories = models.get_product_categories(product_id)
    product_category_ids = [c['id'] for c in product_categories]

    return render_template('products/edit.html',
                           product=product,
                           categories=categories,
                           product_category_ids=product_category_ids)


@app.route('/product/<int:product_id>/delete', methods=['POST'])
@require_admin
def delete_product(product_id):
    product = models.get_product_by_id(product_id)
    if product:
        models.delete_product(product_id)
        flash('Товар удален успешно', 'success')
    return redirect(url_for('products_list'))


@app.route('/admin')
@require_admin
def admin_panel():
    users = models.get_all_users()
    products = models.get_all_products()
    orders = models.get_all_orders()

    return render_template('admin/panel.html',
                           users=users,
                           products=products,
                           orders=orders,
                           users_count=len(users),
                           products_count=len(products),
                           orders_count=len(orders))


if __name__ == '__main__':
    app.run(debug=True)