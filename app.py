from flask import Flask, request, jsonify, make_response, url_for
import logging, json, os

from foodmania.validator import (
    json_file_validator, FoodRecommendationRequestValidator
)

from foodmania.return_message import (
    return_message, success_message
)

validators = {
    'recommender_request' : FoodRecommendationRequestValidator()
}

ZONES = {
    "jakpus": "JAKARTA PUSAT",
    "jaksel": "JAKARTA SELATAN",
    "jakbar": "JAKARTA BARAT",
    "jaktim": "JAKARTA TIMUR",
    "jakut": "JAKARTA UTARA",
}

app = Flask(__name__)
app.config.from_object('foodmania.config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from foodmania.models import (
    Restaurants, Zones, RestaurantScore
)

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

        RestaurantScore.add_restaurant_score_bulk(json_file['data'])
            
        return success_message("New restaurants'score succesfully added")
    except Exception as e:
        logging.warn(str(e))
        return return_message(422, "invalidParameter", str(e)), 422

@app.route("/get_food_recommendation", methods=['GET'])
def get_food_recommendation():
    validated = validators['recommender_request'].loads(json.dumps(request.args))
    if validated.errors:
        return return_message(423, "invalidRequest", validated.errors), 423
    
    data = validated.data
    user_inputs = data['user_input'].lower().split(' ')

    logging.warn(ZONES[data['location'].lower()])

    if data['location'] and (data['location'].lower() in ZONES):
        restaurants = Restaurants.query.filter(Restaurants.location_zone.has(zone_name=ZONES[data['location'].lower()]))

        logging.warn(restaurants)
        


    

if __name__ == '__main__':
    app.run()