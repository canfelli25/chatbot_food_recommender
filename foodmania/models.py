from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import logging

db = SQLAlchemy(app)

class Restaurants(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    res_name = db.Column(db.String)
    res_photo_url = db.Column(db.String)
    rating = db.Column(db.Float)
    average_cost = db.Column(db.Integer)
    currency = db.Column(db.VARCHAR(length=8))
    open_time = db.Column(db.String)
    location_address = db.Column(db.String)
    location_city = db.Column(db.String)
    location_locality = db.Column(db.String)
    lat_long = db.ARRAY(db.Float, as_tuple=True)
    location_zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'))
    location_zone = relationship("Zones")

    @classmethod
    def add_restaurant_bulk(cls, restaurants, zone_id):
        """Put a new restaurants in the database."""

        rests = []
        for res in restaurants:
            timing = res.get('timings', None)
            new_restaurant = Restaurants(
                id = res['id'],
                res_name = res['name'],
                res_photo_url = res['featured_image'],
                rating = res['user_rating']['aggregate_rating'],
                average_cost = res['average_cost_for_two'],
                currency = res['currency'],
                open_time = timing.replace('to', 'sampai') if timing is not None else "",
                location_address = res['location']['address'],
                location_city = res['location']['city'],
                location_locality = res['location']['locality'],
                location_zone_id = int(zone_id),
                lat_long = (res['location']['latitude'], res['location']['longitude'])
            )

            rests.append(new_restaurant)

        db.session.add_all(rests)
        db.session.commit()

class Zones(db.Model):
    __tablename__ = 'zones'

    id = db.Column(db.Integer, primary_key=True)
    zone_name = db.Column(db.VARCHAR(length=255))

    @classmethod
    def add_zone_bulk(cls, zones):
        """Put a new restaurants in the database."""

        new_zones = []
        for zone in zones:
            new_zone = Zones(
                id = zone['id'],
                zone_name = zone['name']
            )

            new_zones.append(new_zone)

        db.session.add_all(new_zones)
        db.session.commit()

class RestaurantScore(db.Model):
    __tablename__ = 'restaurant_score'

    id = db.Column(db.Integer, primary_key=True)
    res_id = db.Column(db.Integer)
    score = db.Column(db.ARRAY(db.String, dimensions=1))

    @classmethod
    def add_restaurant_score_bulk(cls, res_score):
        """Put a new restaurants in the database."""

        new_res_score = []
        for rs in res_score:
            res_sc = RestaurantScore(
                res_id = rs['res_id'],
                score = rs['score']
            )

            new_res_score.append(res_sc)

        db.session.add_all(new_res_score)
        db.session.commit()


db.Index('zone_name', Zones.zone_name)
db.Index('locality', Restaurants.location_locality)
    