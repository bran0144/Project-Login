from flask import Flask, request, jsonify
from pymongo import MongoClient
import certifi


app = Flask(__name__)
uri=""

app.secret_key = "your_secret_key"  # Replace with a strong secret key

client = MongoClient(uri, tlsCAFile=certifi.where())
user_db = client['users']  
users_collection = user_db['users']


@app.route('/register', methods=['POST'])
def register():

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    

    # Check if the email already exists
    if users_collection.find_one({'email': email}):
        return jsonify({'message': f'Email already exists. Please choose another.'}), 401
     

    else:
        users_collection.insert_one({'name': name, 'email':email, 'password': password})
        return jsonify({'message': f'Registration successful. You can now log in.'}), 201

   

@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check if the username and password match
    user = users_collection.find_one({'email': email, 'password': password})

    if user:
        return jsonify({'message': f'Login successful.', 'email': email}), 200
            
    else:
        return jsonify({'message': f'Invalid username or password. Please try again.'}), 401
        
if __name__ == "__main__":

    app.run(port=9002, debug=True)