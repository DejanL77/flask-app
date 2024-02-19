from jsonschema import ValidationError, validate
from flask import Flask, request, jsonify
import sqlite3
from pymongo import MongoClient
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo


app = Flask(__name__)
mongo_client = MongoClient('mongodb://localhost:27017')
mongo_db = mongo_client['users_vouchers']
mongo = PyMongo(app)

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

#1 endpoint
@app.route('/average_spending_by_age/<int:user_id>', methods=['GET'])
def average_spending_by_age(id):
    user_info = UserInfo.query.filter_by(user_id=id).first()

    if not user_info:
        return jsonify({'message': 'User not found.'}), 404

    user_name = user_info.name

    user_spending = UserSpending.query.filter_by(user_id=id).all()
    total_spending = sum(entry.money_spent for entry in user_spending)

    return jsonify({'user_id': id, 'user_name': user_name, 'total_spending': total_spending})

#2 endpoint
@app.route('/average_spending_by_age_range', methods=['GET'])
def average_spending_by_age_range():
    age_ranges = {
        '18-24': (18, 24),
        '25-30': (25, 30),
        '31-36': (31, 36),
        '37-47': (37, 47),
        '>47': (48, 120)
    }

    average_spending_by_age_range = {}

    for range_name, (lower, upper) in age_ranges.items():
        users_in_range = UserInfo.query.filter(UserInfo.age >= lower, UserInfo.age <= upper).all()
        
        total_spending_in_range = 0
        total_users_in_range = len(users_in_range)

        for user in users_in_range:
            user_spending_entry = UserSpending.query.filter_by(user_id=user.user_id).first()
            if user_spending_entry:
                total_spending_in_range += user_spending_entry.money_spent

        average_spending = total_spending_in_range / total_users_in_range if total_users_in_range > 0 else 0
        average_spending_by_age_range[range_name] = average_spending

    return jsonify({'average_spending_by_age_range': average_spending_by_age_range})

#3 endpoint
user_spending_schema = {
    "type": "object",
    "properties": {
        'user_id': {"type": "integer"},
        'money_spent': {"type": "number"},
        'year': {"type": "integer"}
    },
    "required": ["user_id", "money_spent", "year"]
}

@app.route('/write_to_mongodb', methods=['POST'])
def write_to_mongodb():
    if request.method == 'POST':
        data = request.get_json()

        try:
            validate(instance=data, schema=user_spending_schema)
        except ValidationError as e:
            return jsonify({'message': f'Validation error: {str(e)}'}), 400

        try:
            mongo.db.user_spending.insert_one(data)
            return jsonify({'message': 'Data written to MongoDB successfully.'}), 201
        except Exception as e:
            return jsonify({'message': f'Error writing to MongoDB: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Method Not Allowed'}), 405

@app.route('/user_spending_records', methods=['GET'])
def user_spending_records():
    user_spending_data = list(mongo.db.user_spending.find())

    if len(user_spending_data) == 0:
        return jsonify({'message': 'No user spending records found.'}), 404

    records = []
    for record in user_spending_data:
        records.append({
            'user_id': record['user_id'],
            'money_spent': record['money_spent'],
            'year': record['year']
        })

    return jsonify({'user_spending_records': records})