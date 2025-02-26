from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/ecommerce_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    accounts = db.relationship('CustomerAccount', backref='customer', lazy=True)

class CustomerAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_level = db.Column(db.Integer, default=0)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    expected_delivery_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order = db.relationship('Order', backref=db.backref('items', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

@app.before_request
def create_tables():
    db.create_all()

@app.errorhandler(IntegrityError)
def handle_integrity_error(error):
    return jsonify({"error": str(error.orig)}), 400

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    customer = Customer(name=data['name'], email=data['email'], phone_number=data['phone_number'])
    db.session.add(customer)
    db.session.commit()
    return jsonify({"message": "Customer created successfully"}), 201

@app.route('/customers/<int:id>', methods=['GET'])
def read_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({"id": customer.id, "name": customer.name, "email": customer.email, "phone_number": customer.phone_number})

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.json
    customer = Customer.query.get_or_404(id)
    customer.name = data['name']
    customer.email = data['email']
    customer.phone_number = data['phone_number']
    db.session.commit()
    return jsonify({"message": "Customer updated successfully"})

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"})

@app.route('/customer_accounts', methods=['POST'])
def create_customer_account():
    data = request.json
    account = CustomerAccount(username=data['username'], password=data['password'], customer_id=data['customer_id'])
    db.session.add(account)
    db.session.commit()
    return jsonify({"message": "Customer account created successfully"}), 201

@app.route('/customer_accounts/<int:id>', methods=['GET'])
def read_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    return jsonify({"id": account.id, "username": account.username, "customer_id": account.customer_id, "customer": {"name": account.customer.name, "email": account.customer.email, "phone_number": account.customer.phone_number}})

@app.route('/customer_accounts/<int:id>', methods=['PUT'])
def update_customer_account(id):
    data = request.json
    account = CustomerAccount.query.get_or_404(id)
    account.username = data['username']
    account.password = data['password']
    db.session.commit()
    return jsonify({"message": "Customer account updated successfully"})

@app.route('/customer_accounts/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Customer account deleted successfully"})

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    product = Product(name=data['name'], price=data['price'], stock_level=data.get('stock_level', 0))
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product created successfully"}), 201

@app.route('/products/<int:id>', methods=['GET'])
def read_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({"id": product.id, "name": product.name, "price": product.price, "stock_level": product.stock_level})

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    product = Product.query.get_or_404(id)
    product.name = data['name']
    product.price = data['price']
    product.stock_level = data.get('stock_level', product.stock_level)
    db.session.commit()
    return jsonify({"message": "Product updated successfully"})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})

@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{"id": product.id, "name": product.name, "price": product.price, "stock_level": product.stock_level} for product in products])

@app.route('/orders', methods=['POST'])
def place_order():
    data = request.json
    order = Order(order_date=data['order_date'], customer_id=data['customer_id'])
    db.session.add(order)
    db.session.commit()
    for item in data['items']:
        order_item = OrderItem(order_id=order.id, product_id=item['product_id'], quantity=item['quantity'])
        db.session.add(order_item)
    db.session.commit()
    return jsonify({"message": "Order placed successfully"}), 201

@app.route('/orders/<int:id>', methods=['GET'])
def retrieve_order(id):
    order = Order.query.get_or_404(id)
    items = [{"product_id": item.product_id, "quantity": item.quantity, "product_name": item.product.name} for item in order.items]
    return jsonify({"id": order.id, "order_date": order.order_date, "customer_id": order.customer_id, "items": items})

@app.route('/orders/<int:id>/total_price', methods=['GET'])
def calculate_order_total_price(id):
    order = Order.query.get_or_404(id)
    total_price = sum(item.quantity * item.product.price for item in order.items)
    return jsonify({"order_id": order.id, "total_price": total_price})

@app.route('/orders/<int:id>/cancel', methods=['POST'])
def cancel_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order canceled successfully"})

@app.route('/customers/<int:customer_id>/orders', methods=['GET'])
def manage_order_history(customer_id):
    orders = Order.query.filter_by(customer_id=customer_id).all()
    return jsonify([{"id": order.id, "order_date": order.order_date, "items": [{"product_id": item.product_id, "quantity": item.quantity} for item in order.items]} for order in orders])

@app.route('/orders/<int:id>/track', methods=['GET'])
def track_order(id):
    order = Order.query.get_or_404(id)
    return jsonify({"id": order.id, "order_date": order.order_date, "expected_delivery_date": order.expected_delivery_date, "status": order.status, "customer_id": order.customer_id})

@app.route('/products/<int:id>/stock', methods=['PUT'])
def update_product_stock(id):
    data = request.json
    product = Product.query.get_or_404(id)
    product.stock_level = data['stock_level']
    db.session.commit()
    return jsonify({"message": "Product stock updated successfully"})

@app.route('/products/restock', methods=['POST'])
def restock_products():
    data = request.json
    threshold = data['threshold']
    restock_amount = data['restock_amount']
    products = Product.query.filter(Product.stock_level < threshold).all()
    for product in products:
        product.stock_level += restock_amount
    db.session.commit()
    return jsonify({"message": "Products restocked successfully"})

if __name__ == '__main__':
    app.run(debug=True)