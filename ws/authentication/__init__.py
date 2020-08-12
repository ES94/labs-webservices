from flask import Blueprint

auth_blueprint = Blueprint('authentication', __name__)

# Routes
from . import auth