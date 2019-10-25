from marshmallow import Schema, fields
from marshmallow.validate import Range
from marshmallow.utils import get_value
import json, logging

allowed_files = ['json']

class DriversRequestValidator(Schema):
    latitude = fields.Float(required=True, validate=Range(min=-90.0, max=90.0))
    longitude = fields.Float(required=True, validate=Range(min=-180.0, max=180.0))
    radius = fields.Int(required=False, validate=Range(min=1), default=500, missing=500)
    limit = fields.Int(required=False, validate=Range(min=1), default=10, missing=10)

    @classmethod
    def get_attribute(self, attr, obj, default):
        return get_value(attr, obj, default=default) or missing


class DriverLocationRequestValidator(Schema):
    latitude = fields.Float(required=True, validate=Range(min=-90.0, max=90.0))
    longitude = fields.Float(required=True, validate=Range(min=-180.0, max=180.0))
    accuracy = fields.Float(required=True, validate=Range(min=0.0, max=1.0))

class FoodRecommendationRequestValidator(Schema):
    location = fields.String()
    user_input = fields.String(required=True)

def json_file_validator(file):
    try:
        files = file['file'].filename.split('.')
        ext = files[-1]
        return json.loads(file['file'].read()) if ext in allowed_files else None
    except:
        raise Exception('No files found')