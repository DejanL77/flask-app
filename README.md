<h1>Introduction</h1>
This README.md file provides an in-depth explanation of the Flask application code. The application is designed to handle user information and spending records. It uses Flask as the web framework and MongoDB as the database for storing user information and spending records.

<h2>Libraries Used</h2>
The following Python libraries are imported in the code:

<li>from jsonschema import ValidationError, validate: This library is used for validating JSON data against a predefined schema.</li>

<li>from flask import Flask, request, jsonify: Flask is a micro web framework used for building web applications in Python. It simplifies the process of handling HTTP requests and responses.</li>

<li>import sqlite3: SQLite3 is a lightweight database engine. Though it is imported, it's not actively used in the current version of the code.</li>

<li>from pymongo import MongoClient: This library is used for interacting with MongoDB, a NoSQL database.</li>

<li>from flask_sqlalchemy import SQLAlchemy: SQLAlchemy is a SQL toolkit and Object-Relational Mapping (ORM) library for Python. However, in the code, it is imported but not actively used.</li>

<li>from flask_pymongo import PyMongo: PyMongo is a Flask extension for working with MongoDB. It simplifies the integration of MongoDB with Flask applications.</li>

<li>from http import HTTPMethod: This import appears unused in the code, and HTTPMethod is not explicitly used in the current version.</li>

<h2>Application Structure</h2>
<h3>Flask Configuration</h3>
The Flask application is created and configured with the MongoDB URI. Two collections are defined using PyMongo: UserInfo for storing user information and UserSpending for storing spending records. <br>

app = Flask(__name__) <br>
app.config["MONGO_URI"] = "mongodb://localhost:27017/users_vouchers"  <br>
mongo = PyMongo(app)  <br>
db = mongo.db  <br>
UserInfo = db.UserInfo  <br>
UserSpending = db.UserSpending  <br>

<h2>Endpoints</h2>
<ol>
     <li>
        /all_users - GET
        This endpoint retrieves all user information from the UserInfo collection and returns it as a JSON response.
    </li>
    <li>
         /average_spending_by_age/<int:id> - GET
        This endpoint calculates the total spending for a user specified by the <int:id> parameter and returns a JSON response containing the user's ID, name, and total spending.
    </li>
    <li>
         /average_spending_by_age_range - GET
        This endpoint calculates the average spending for users in different age ranges and returns the results as a JSON response.
    </li>
    <li>
        /write_to_mongodb - POST
        This endpoint allows the insertion of spending records into the UserSpending collection. It validates incoming JSON data against a predefined schema before insertion.
    </li>
    <li>
        /user_spending_records - GET
        This endpoint retrieves all spending records from the UserSpending collection and returns them as a JSON response.
    </li>
</ol> 
            
<h2>Running the Application</h2>
To run the application, execute the flaskapp.py script. The application runs in debug mode and can be accessed at http://127.0.0.1:5000/.

if __name__ == '__main__':  <br>
    app.run(debug=True)  <br>
    
<h2>Running the Application</h2>
Ensure that MongoDB is running on localhost at port 27017.

Execute the flaskapp.py script to start the Flask application.

Access the application at http://127.0.0.1:5000/ in a web browser or via API requests.

<h2>Conclusion</h2>
This Flask application demonstrates a simple RESTful API for managing user information and spending records, with MongoDB as the underlying database. Users can retrieve user information, calculate average spending by age and age range, write spending records, and retrieve spending records. The code is modular and can be extended to include additional functionality or integrate with other databases.
