import os
import json
import requests

USER_KEY = 'a67139954b624b37d34fc27bcf085d3e'
FILE = 'static/resto-cuisines-{}.json'
BASE_API = 'https://developers.zomato.com/api/v2.1/' 
RESTAURANT_ENDPOINT = 'restaurant'
SEARCH_ENDPOINT = 'search'
REVIEW_ENDPOINT = 'reviews'

zones = [74001, 74002, 74003, 74004, 74005]

def parse_reviews(resto_info):
    data = []
    reviews = resto_info.get('all_reviews').get('reviews')
    for r in reviews:
        review = r.get('review')
        data.append({
            'rating': review.get('rating'),
            'review_text': review.get('review_text'),
            'id': review.get('id')
        })
    return data

def parse_location(resto_info):
    location = resto_info.get('location')
    return {
        'address': location.get('address'),
        'locality': location.get('locality'),
        'city': location.get('city'),
        'latitude': location.get('latitude'),
        'longitude': location.get('longitude'),
    }

for zone in zones:
    all_data = []
    with open(FILE.format(zone)) as f:
        restaurant_ids = []
        restaurants = json.loads(f.read()).get('restaurants')
        for resto in restaurants:
            resto_info = resto.get('restaurant')
            id = resto_info.get('id')
            reviews = parse_reviews(resto_info)
            for i in range(3):
                params = {
                    'res_id': int(id),
                    'start': 5 * (i+1),
                    'count': 5,
                }
                headers = {'user-key': USER_KEY}
                resp = requests.get(BASE_API + REVIEW_ENDPOINT, params=params, headers=headers)
                temp = resp.json() or []
                for r in temp.get('user_reviews'):
                    review = r.get('review')
                    reviews.append({
                        'rating': review.get('rating'),
                        'review_text': review.get('review_text'),
                        'id': review.get('id')
                    })
            data = {
                'name': resto_info.get('name'),
                'id': resto_info.get('id'),
                'url': resto_info.get('url'),
                'cuisines': resto_info.get('cuisines'),
                'timings': resto_info.get('timings'),
                'highlights': resto_info.get('highlights'),
                'user_rating': {'aggregate_rating': resto_info.get('user_rating').get('aggregate_rating')},
                'featured_image': resto_info.get('featured_image'),
                'reviews': reviews,
                'zone_id': zone,
                'currency': 'IDR',
                'average_cost_for_two': resto_info.get('average_cost_for_two'),
                'location': parse_location(resto_info)
            }
            all_data.append(data)
            
    with open('static/resto-reviews-{}.json'.format(zone), 'w') as h:
        new_data = {
            'data': all_data,
            'zone_id': int(zone),
        }
        h.write(json.dumps(new_data))

