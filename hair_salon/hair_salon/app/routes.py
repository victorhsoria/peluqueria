# routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Product, Order

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        brand = request.form.get('brand')
        description = request.form.get('description')
        wholesale_price = request.form.get('wholesale_price')
        professional_price = request.form.get('professional_price')

        new_product = Product(brand=brand, description=description, wholesale_price=wholesale_price, professional_price=professional_price)
        db.session.add(new_product)
        db.session.commit()
        flash('Producto agregado exitosamente', 'success')
        return redirect(url_for('main.products'))

    products = Product.query.all()
    return render_template('products.html', products=products)

@main.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.brand = request.form.get('brand')
        product.description = request.form.get('description')
        product.wholesale_price = request.form.get('wholesale_price')
        product.professional_price = request.form.get('professional_price')
        db.session.commit()
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('main.products'))

    return render_template('edit_product.html', product=product)

@main.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('main.products'))

@main.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'POST':
        date = request.form.get('date')
        product_ids = request.form.getlist('product_ids')
        quantities = request.form.getlist('quantities')

        for product_id, quantity in zip(product_ids, quantities):
            new_order = Order(product_id=product_id, quantity=int(quantity), date=date)
            db.session.add(new_order)
        db.session.commit()
        flash('Pedido agregado exitosamente', 'success')
        return redirect(url_for('main.orders'))

    products = Product.query.all()
    orders = Order.query.all()
    total_amount = sum(order.product.wholesale_price * order.quantity for order in orders)
    return render_template('orders.html', products=products, orders=orders, total_amount=total_amount)

@main.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Pedido eliminado exitosamente', 'success')
    return redirect(url_for('main.orders'))

@main.route('/order_summary')
def order_summary():
    orders = Order.query.all()
    return render_template('order_summary.html', orders=orders)
