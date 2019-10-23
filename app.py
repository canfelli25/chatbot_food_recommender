from flask import Flask, request, jsonify, make_response, url_for
import logging, json, os

from api.validator import (
    DriversRequestValidator, DriverLocationRequestValidator,
    json_file_validator

)

from api.return_message import (
    return_message, success_message
)

validators = {
    'drivers' : DriversRequestValidator(),
    'location': DriverLocationRequestValidator()
}

app = Flask(__name__)
app.config.from_object('api.config.ProductionConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from api.models import *

@app.route('/', methods=['GET'])
def hello():
    return jsonify(status_code=200, status="OK", body={'message':
                        'hello'})

@app.route('/upload/all_restaurants', methods=['POST'])
def upload_restaurant():
    context = request.files
    try:
        json_file = json_file_validator(context)
        if json_file is None:
            return return_message(421, "invalidFile", "Only json files allowed"), 421

        Restaurants.add_restaurant_bulk(json_file['data'], json_file['zone_id'])
            
        return success_message("New restaurants succesfully added")
    except Exception as e:
        logging.warn(str(e))
        return return_message(422, "invalidParameter", str(e)), 422

@app.route('/upload/all_zones', methods=['POST'])
def upload_zones():
    context = request.files
    try:
        json_file = json_file_validator(context)
        if json_file is None:
            return return_message(421, "invalidFile", "Only json files allowed"), 421

        Zones.add_zone_bulk(json_file['data'])
            
        return success_message("New zones succesfully added")
    except Exception as e:
        logging.warn(str(e))
        return return_message(422, "invalidParameter", str(e)), 422

@app.route('/upload/all_restaurant_score', methods=['POST'])
def upload_restaurants_score():
    context = request.files
    try:
        json_file = json_file_validator(context)
        if json_file is None:
            return return_message(421, "invalidFile", "Only json files allowed"), 421

        RestaurantScore.add_retaurant_score_bulk(json_file['data'])
            
        return success_message("New restaurants'score succesfully added")
    except Exception as e:
        logging.warn(str(e))
        return return_message(422, "invalidParameter", str(e)), 422

if __name__ == '__main__':
    app.run()