from flask import Blueprint

facebook_blueprint = Blueprint('facebook', __name__)

# Routes
from . import (fb_city_chatbot_routes, 
    fb_gender_age_chatbot_routes, fb_number_chatbot_routes, 
    fb_post_videos_chatbot_routes, fb_type_chatbot_routes, 
    fb_type_ordered_chatbot_routes)