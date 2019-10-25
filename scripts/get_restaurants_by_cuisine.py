import os
import json
import requests

USER_KEY = 'a67139954b624b37d34fc27bcf085d3e'
FILE = 'static/cuisines.json'
BASE_API = 'https://developers.zomato.com/api/v2.1/' 
RESTAURANT_ENDPOINT = 'restaurant'
SEARCH_ENDPOINT = 'search'
REVIEW_ENDPOINT = 'review'

with open(FILE) as f:
    restaurant_ids = []
    cuisines = json.loads(f.read())
    cuisine_ids = [str(cuisine.get('cuisine').get('cuisine_id')) for cuisine in cuisines.get('cuisines')]
    params = {
        'cuisines': ','.join(cuisine_ids),
        'entity_id': '74005',
        'entity_type': 'zone'
    }
    headers = {'user-key': USER_KEY}
    resp = requests.get(BASE_API + SEARCH_ENDPOINT, params=params, headers=headers)

    with open('static/resto-cuisines-74005.json', 'w') as h:
        h.write(json.dumps(resp.json()))

