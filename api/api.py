from flask import Flask, request, jsonify
from flask_cors import CORS
from db import save_data_to_db
from interpreter import save_json
import json
app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}})
CORS(app)

collected_data = {
    "clicks": [],
    "scrollPercentage": 0,
    "scrollMax": 0,
    "scrollData": {},
    "time": [],
    "sectionVisibility": {},
    "userAgent": {},
    "url": {},
    "historyLength": 0,
    "screenWidth": 0,
    "screenHeight": 0,
    "device": {},
    "timezone": {},
    "cookies": {},
    "connectionSpeed": {},
    "noTracking": {},
    "userAgentLanguage": {},
    "cpuCores":{},
    "referrer":{},
}


@app.route('/api/save-data', methods=['POST'])
def save_data():
    try:
        data = request.get_json() 
        save_json(data)
        save_data_to_db(data)
        return jsonify({'message': 'Success'}), 200


    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 
