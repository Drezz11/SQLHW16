from flask import Flask, request, jsonify
import SQLAlchemy
from sqlalchemy import ForeignKey
from utils import get_all_users, get_all_order, gel_all_offer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Ineger)
    email = db.Column(db.String(100))
    role = db.Column(db.Ctring(100))
    phone = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }

    @property
    def __repr__(self):
        return f"User({self.id}, {self.first_name}, {self.last_name}, {self.age}, {self.email}, {self.role}," \
               f" {self.phone})"


class Order(db.model):
    __tablename__ = 'orders'
    id = db.Column(db.Ineger, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    start_date = db.Column(db.Text)
    end_date = db.Column(db.Text)
    address = db.Column(db.Text)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, ForeignKey("user.id"))
    customer = db.relationship("User", foreign_keys=[customer_id])
    executor = db.relationship("User", foreign_keys=[executor_id])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
        }

    def __repr__(self):
        return f"Order({self.id}, {self.name}, {self.description}, {self.start_date}, {self.end_date}, {self.address}," \
               f" {self.price})"


class Offer(db.Model):
    # """Модель предложения"""
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, ForeignKey("user.id"))

    order_1 = db.relationship("Order")
    user = db.relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }

    def __repr__(self):
        return f"Offer({self.id})"


db.drop_all()
db.create_all()

# Создаем users
users = [User(**row) for row in get_all_users()]
order = [Order(**row) for row in get_all_order()]
offer = [Offer(**row) for row in gel_all_offer()]

# Загружаем БД
with db.session.begin():
    db.session.add_all(users)
    db.session.add_all(order)
    db.session.add_all(offer)
db.session.commit()

order = db.session.query(Order).get(1)
offer = db.session.query(Offer).get(1)
user = db.session.query(User).get(1)


# """GET и POST для пользователей"""
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        result = []
        for us in db.session.query(User).all():
            result.append(us.to_dict())
        return jsonify(result), 200
    elif request.method == "POST":
        content = request.json
        user_add_all = [User(**row) for row in content]
        db.session.add_all(user_add_all)
        db.session.commit()

        result = []
        for us in db.session.query(User).all():
            result.append(us.to_dict())
        return jsonify(result), 200


@app.route('/users/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
# """Работа по конкретному пользователю"""
def read_user(pk):
    if request.method == "GET":
        return f'{db.session.query(User).get(pk)}'

    if request.method == "PUT":
        user_data = request.json
        user_old = db.session.query(User).get(pk)
        user_old.first_name = user_data['first_name']
        user_old.last_name = user_data['last_name']
        user_old.age = user_data['age']
        user_old.email = user_data['email']
        user_old.role = user_data['role']
        user_old.phone = user_data['phone']

        db.session.add(user_old)
        db.session.commit()
        return f'{db.session.query(User).get(pk)}', 200

    if request.method == "DELETE":
        user_del = db.session.query(User).get(pk)

        db.session.delete(user_del)
        db.session.commit()
        return "", 204


@app.route('/orders', methods=["GET", "POST"])
# """Работа по заказам"""
def orders():
    if request.method == "GET":
        result = []
        for order_1 in db.session.query(Order).all():
            result.append(order_1.to_dict())
        return jsonify(result), 200
    elif request.method == "POST":
        content = request.json
        order_add_all = [Order(**row) for row in content]
        db.session.add_all(order_add_all)
        db.session.commit()

        result = []
        for order_1 in db.session.query(Order).all():
            result.append(order_1.to_dict())
        return jsonify(result), 200


@app.route('/orders/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
# """Работа по конкретному заказу"""
def read_order(pk):
    if request.method == "GET":
        return f'{db.session.query(Order).get(pk)}'
    if request.method == "PUT":
        order_data = request.json
        order_old = db.session.query(Order).get(pk)
        order_old.first_name = order_data['first_name']
        order_old.last_name = order_data['last_name']
        order_old.age = order_data['age']
        order_old.email = order_data['email']
        order_old.role = order_data['role']
        order_old.phone = order_data['phone']

        db.session.add(order_old)
        db.session.commit()
        return f'{db.session.query(Order).get(pk)}', 200

    if request.method == "DELETE":
        order_del = db.session.query(Order).get(pk)

        db.session.delete(order_del)
        db.session.commit()
        return "", 204


@app.route('/offers', methods=['GET', 'POST'])
# """Работа по предложениям"""
def offers():
    if request.method == "GET":
        result = []
        for offer_1 in db.session.query(Offer).all():
            result.append(offer_1.to_dict())
        return jsonify(result), 200
    elif request.method == "POST":
        content = request.json
        offer_add_all = [Offer(**row) for row in content]
        db.session.add_all(offer_add_all)
        db.session.commit()

        result = []
        for offer_1 in db.session.query(Offer).all():
            result.append(offer_1.to_dict())
        return jsonify(result), 200


@app.route('/offers/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
# """Работа по конкретному предложению"""
def read_offer(pk):
    if request.method == "GET":
        return f'{db.session.query(Offer).get(pk).order_1}\n{db.session.query(Offer).get(pk).user}'
    if request.method == "PUT":
        offers_data = request.json
        offer_old = db.session.query(Offer).get(pk)
        offer_old.order_id = offers_data['order_id']
        offer_old.executor_id = offers_data['executor_id']

        db.session.add(offer_old)
        db.session.commit()
        return f'{db.session.query(Offer).get(pk).order_1}\n{db.session.query(Offer).get(pk).user}', 200

    if request.method == "DELETE":
        offer_del = db.session.query(Offer).get(pk)

        db.session.delete(offer_del)
        db.session.commit()
        return "", 204


if __name__ == "__main__":
    app.run(debug=True)
