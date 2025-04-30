# app.py
from flask import Flask, jsonify
from flask_cors import CORS
import requests  
import connectedcar
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)from flask import Flask, jsonify
from flask_cors import CORS
import connectedcar
import os
from dotenv import load_dotenv

# Load sensitive variables from .env
load_dotenv()

# Flask app setup
app = Flask(__name__)
CORS(app)


def get_vehicle_data():
    """
    Interacts with the FordPass API to retrieve vehicle data.
    Assumes environment variables for sensitive info.
    """
    try:
        # Retrieve API credentials from environment
        client_id = os.getenv('FORDPASS_CLIENT_ID')
        username = os.getenv('FORDPASS_USERNAME')
        password = os.getenv('FORDPASS_PASSWORD')

        if not client_id or not username or not password:
            raise ValueError("API credentials not found in the environment.")

        # Authenticate and retrieve access token
        client = connectedcar.AuthClient(client_id, None, None)
        access_info = client.get_user_access_token(username, password)
        access_token = access_info.get('access_token')

        if not access_token:
            raise ValueError("Failed to retrieve access token.")

        # Create a User object and fetch vehicles
        user = connectedcar.User(access_token)
        vehicles = user.vehicles()

        # Prepare the list of user vehicles (for simplicity, return basic info)
        vehicle_list = []
        for vehicle in vehicles:
            vehicle_list.append({
                'vin': vehicle.get('vin'),
                'model': vehicle.get('vehicleDetails', {}).get('model'),
                'nickname': vehicle.get('vehicleDetails', {}).get('nickname', 'N/A'),
                'color': vehicle.get('vehicleDetails', {}).get('color'),
            })

        return {
            'status': 'success',
            'vehicles': vehicle_list
        }

    except Exception as e:
        # Basic error handling
        return {
            'status': 'error',
            'message': str(e)
        }


@app.route('/api/vehicle_data', methods=['GET'])
def vehicle_data():
    data = get_vehicle_data()
    if data.get('status') == 'success':
        return jsonify(data)
    else:
        return jsonify(data), 500


if __name__ == '__main__':
    app.run(debug=True)
CORS(app)  


def get_vehicle_data():
    """
    This function should interact with the FordPass API
    and return the relevant vehicle data.
    """
    
    client = connectedcar.AuthClient(
    '9fb503e0-715b-47e8-adfd-ad4b7770f73b',
    None,
    None)  
    access = client.get_user_access_token(
        "alexbocchi17@gmail.com", "Zakumi2001@")  # Fetch client access token

    # user = connectedcar.User(access['access_token'])  # New User Object
    # vehicles = user.vehicles()  # Fetch list of user vehicles

    # vehicleList = []  # Stored list of user vehicles

    # for userVehicle in vehicles:  # For each user vehicle
    #     vehicleList.insert(0, userVehicle['vin'])
    #     break

    # currentVehicle = connectedcar.Vehicle(
    #     vehicleList[0], access['access_token'])  # Create vehicle object
    # print(currentVehicle.start())  # Send start command

    return access

@app.route('/api/vehicle_data', methods=['GET'])
def vehicle_data():
    data = get_vehicle_data()
    if data:
        return jsonify(data)
    else:
        return jsonify({"status": "error", "message": "Failed to retrieve vehicle data"}), 500

if __name__ == '__main__':
    app.run(debug=True) # Run the Flask development server