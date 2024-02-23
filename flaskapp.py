from jsonschema import ValidationError, validate
from flask import Flask, request, jsonify
import sqlite3
from pymongo import MongoClient
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/users_vouchers" 
mongo = PyMongo(app)
db = mongo.db
UserInfo = db.UserInfo
UserSpending = db.UserSpending

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/all_users', methods=['GET'])
def all_users():
    all_users_info = UserInfo.find()

    if not all_users_info:
        return jsonify({'message': 'No users found.'}), 404

    users_data = [
        {
            'user_id': user['user_id'],
            'name': user['name'],
            'email': user['email'],
            'age': user['age']
        } for user in all_users_info
    ]

    return jsonify({'users': users_data})


#1 endpoint
@app.route('/average_spending_by_age/<int:id>', methods=['GET'])
def average_spending_by_age(id):
    user_info = UserInfo.find_one({"user_id": id})

    if not user_info:
        return jsonify({'message': 'User not found.'}), 404

    user_name = user_info.get('name')

    user_spending_entries = UserSpending.find({"user_id": id})
    total_spending = sum(entry.get('money_spent', 0) for entry in user_spending_entries)

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
        users_in_range = UserInfo.find(UserInfo.age >= lower, UserInfo.age <= upper).all()
        
        total_spending_in_range = 0
        total_users_in_range = len(users_in_range)

        for user in users_in_range:
            user_spending_entry = UserSpending.find_one(user_id=user.user_id).first()
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

if __name__ == '__main__':
    app.run(debug=True)