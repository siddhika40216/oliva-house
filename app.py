
from flask import Flask, render_template, request, jsonify,redirect,session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.environ.get(
    "OLIVA_SECRET_KEY",
    "dev-only-change-this-secret"
)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + os.path.join(basedir, "oliva_house.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Menu item database model
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250))
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(250))
    available = db.Column(db.Boolean, default=True)


class CustomerOrder(db.Model):
    __tablename__ = "customer_orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    total_amount = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.String(30), nullable=False, default="Pending")
    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )

    items = db.relationship(
        "OrderItem",
        backref="customer_order",
        cascade="all, delete-orphan"
    )


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("customer_orders.id"),
        nullable=False
    )

    menu_item_id = db.Column(
        db.Integer,
        db.ForeignKey("menu_item.id"),
        nullable=True
    )

    item_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)



@app.route("/")
def home():
    menu_items = MenuItem.query.filter_by(available=True).all()
    return render_template("index.html", menu_items=menu_items)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password", "")

        admin_password = os.environ.get("OLIVA_ADMIN_PASSWORD")

        if admin_password and password == admin_password:
            session["is_admin"] = True
            return redirect("/admin/orders")

        return render_template(
            "admin_login.html",
            error="Incorrect password. Please try again."
        )

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect("/admin/login")


@app.route("/place-order", methods=["POST"])
def place_order():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid order data."}), 400

    customer_name = str(data.get("customer_name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    address = str(data.get("address", "")).strip()
    cart_items = data.get("items", [])

    if not customer_name or not address:
        return jsonify({
            "error": "Name and delivery address are required."
        }), 400

    if not phone.isdigit() or len(phone) != 10:
        return jsonify({
            "error": "Enter a valid 10-digit phone number."
        }), 400

    if not isinstance(cart_items, list) or not cart_items:
        return jsonify({"error": "Your cart is empty."}), 400

    order_lines = []
    total_amount = 0

    for cart_item in cart_items:
        name = str(cart_item.get("name", "")).strip()

        try:
            quantity = int(cart_item.get("quantity", 0))
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid quantity."}), 400

        if not name or quantity < 1 or quantity > 100:
            return jsonify({"error": "Invalid cart item."}), 400

        # Fetch the price from the database, not the browser.
        menu_item = MenuItem.query.filter_by(
            name=name,
            available=True
        ).first()

        if menu_item is None:
            return jsonify({
                "error": f"{name} is currently unavailable."
            }), 400

        line_total = menu_item.price * quantity
        total_amount += line_total

        order_lines.append((menu_item, quantity))

    try:
        order = CustomerOrder(
            customer_name=customer_name,
            phone=phone,
            address=address,
            total_amount=round(total_amount, 2),
            status="Pending"
        )

        db.session.add(order)
        db.session.flush()

        for menu_item, quantity in order_lines:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=menu_item.id,
                item_name=menu_item.name,
                price=menu_item.price,
                quantity=quantity
            )
            db.session.add(order_item)

        db.session.commit()

        return jsonify({
            "message": "Your order has been placed successfully!",
            "order_id": order.id,
            "total": round(total_amount, 2)
        }), 201

    except Exception:
        db.session.rollback()
        app.logger.exception("Could not save the order")
        return jsonify({
            "error": "We could not save your order. Please try again."
        }), 500


@app.route("/admin/orders")
def admin_orders():
    orders = CustomerOrder.query.order_by(
        CustomerOrder.created_at.desc()
    ).all()
    if not session.get("is_admin"):
        return redirect("/admin/login")

    return render_template("admin_orders.html", orders=orders)


@app.route("/admin/orders/<int:order_id>/status", methods=["POST"])
def update_order_status(order_id):
    order = db.session.get(CustomerOrder, order_id)
    if not session.get("is_admin"):
        return redirect("/admin/login")

    if order is None:
        return "Order not found", 404

    new_status = request.form.get("status", "").strip()

    allowed_statuses = [
        "Pending",
        "Preparing",
        "Out for Delivery",
        "Delivered",
        "Cancelled"
    ]

    if new_status not in allowed_statuses:
        return "Invalid order status", 400

    order.status = new_status
    db.session.commit()

    return redirect("/admin/orders")


@app.route("/track-order", methods=["GET", "POST"])
def track_order():
    order = None
    error = None

    if request.method == "POST":
        order_id = request.form.get("order_id", "").strip()
        phone = request.form.get("phone", "").strip()

        if not order_id.isdigit():
            error = "Please enter a valid order number."
        elif not phone.isdigit() or len(phone) != 10:
            error = "Please enter your 10-digit phone number."
        else:
            order = CustomerOrder.query.filter_by(
                id=int(order_id),
                phone=phone
            ).first()

            if order is None:
                error = "No matching order found. Check your details."

    return render_template(
        "track_order.html",
        order=order,
        error=error
    )


# @app.route("/order-confirmation/<int:order_id>")
# def order_confirmation(order_id):
#     order = db.session.get(CustomerOrder, order_id)

#     if order is None:
#         return "Order not found", 404

#     return render_template(
#         "order_confirmation.html",
#         order=order
#     )
@app.route("/order-confirmation/<int:order_id>")
def order_confirmation(order_id):
    order = CustomerOrder.query.get_or_404(order_id)
    return render_template(
        "order_confirmation.html",
        order=order
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
