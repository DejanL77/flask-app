from flask import Flask, request, jsonify
import sqlite3
from pymongo import MongoClient
import requests
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
mongo_client = MongoClient('mongodb://localhost:27017')
mongo_db = mongo_client['users_vouchers']

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_vouchers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#db = 'C:\\Users\\deki_\\OneDrive\\Desktop\\pythonsemos\\flask\\flask-app\\users_vouchers.db'
class UserInfo(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)

class UserSpending(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    money_spent = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)

@app.route('/average_spending_by_age/<int:user_id>', methods=['GET'])
def average_spending_by_age(id):
    user_info = UserInfo.query.filter_by(user_id=id).first()

    if not user_info:
        return jsonify({'message': 'User not found.'}), 404

    user_name = user_info.name

    user_spending = UserSpending.query.filter_by(user_id=id).all()
    total_spending = sum(entry.money_spent for entry in user_spending)

    return jsonify({'user_id': id, 'user_name': user_name, 'total_spending': total_spending})