from . import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    wholesale_price = db.Column(db.Float, nullable=False)
    professional_price = db.Column(db.Float, nullable=False)
    orders = db.relationship('Order', backref='product', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
