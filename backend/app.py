from flask import Flask, request, jsonify
from maxminddb import open_database
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

geoLite2City = open_database('GeoLite2-City_20230317/GeoLite2-City.mmdb')

#method which gets ip data from database and send add to `results` 
@app.route('/geolocation', methods=['POST'])
def geolocation():
    data = request.get_json()
    ip_addresses = data['ip_addresses']
    results = []
    for ip_address in ip_addresses:
        result = {}
        try:
            response = geoLite2City.get(ip_address)
            result['ip_address'] = ip_address
            
            if 'country' in response and response['country']['iso_code'] is not None:
                result['country_code'] = response['country']['iso_code']
            else:
                result['country_code'] = ''

            if 'postal' in response and response['postal']['code'] is not None:
                result['postal_code'] = response['postal']['code']
            else:
                result['postal_code'] = ''
            
            if 'city' in response and response['city']['names']['en'] is not None:
                result['city_name'] = response['city']['names']['en']
            else:
                result['city_name'] = ''
            
            if 'location' in response and response['location']['time_zone'] is not None:
                result['time_zone'] = response['location']['time_zone']
            else:
                result['time_zone'] = ''
            
            if 'location' in response and response['location']['accuracy_radius'] is not None:
                result['accuracy_radius'] = response['location']['accuracy_radius']
            else:
                result['accuracy_radius'] = ''

            result['result_val'] = True
            results.append(result)
        except:
            print('Not adding the value ...',ip_address)
    return jsonify(results)

if __name__ == '__main__':
    app.run()
