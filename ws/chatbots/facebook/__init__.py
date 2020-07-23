from flask import Blueprint

facebook_blueprint = Blueprint('facebook', __name__)

# Routes
from . import (fb_city_methods_routes, 
    fb_gender_age_methods_routes, fb_number_methods_routes, 
    fb_post_videos_methods_routes, fb_type_methods_routes, 
    fb_type_ordered_methods_routes)