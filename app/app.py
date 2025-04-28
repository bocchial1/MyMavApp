# app.py
from flask import Flask, jsonify
from flask_cors import CORS
import requests  
import connectedcar
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
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