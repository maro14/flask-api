from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Users class/model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(120), unique=True)
    phone = db.Column(db.Float)

    def __init__(self, name, email, address, phone):
        self.name = name
        self.email = email
        self.address = address
        self.phone = phone

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'address', 'phone')

# Init Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Create a User
@app.route('/user', methods=["POST"])
def add_user():
    name = request.json['name']
    email = request.json['email']
    address =request.json['address']
    phone = request.json['phone']

    new_user = User(name, email, address, phone)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# Get All Users
@app.route("/user", methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# Get one User
@app.route("/user/<id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

# Update user
@app.route('/user/<id>', methods=["PUT"])
def update_user(id):
    user = User.query.get(id)

    name = request.json['name']
    email = request.json['email']
    address =request.json['address']
    phone = request.json['phone']

    user.name = name
    user.email = email
    user.address = address
    user.phone = phone

    db.session.commit()

    return user_schema.jsonify(user)

# Delete User
@app.route("/user/<id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)



if __name__ == "__main__":
    app.run(host="localhost", port=2200, debug=True)