import copy
import simplejson as json
from datetime import date, datetime

from flask import Blueprint, request
from werkzeug import wrappers

from classes.error import Error
from classes.database import Database
from classes.settings import Settings
from classes.utils import Utils


chatbots_blueprint = Blueprint('chatbots', __name__)


@chatbots_blueprint.route('/getbottotalusers', methods=['POST'])
def get_bot_total_users():
	# Variables locales
	error = None
	response = None
	account = None
	id_media = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar argumentos válidos
			json_data = request.get_json()
			validate_arguments = Utils.areValidPostArguments(
				json_data, 
				['account', 'id_media']
			)
			if validate_arguments['status'] == 'success':
				# Crear db, query, y postear query
				account = json_data['account']
				id_media = json_data['id_media']
				db = Database.getInstance(
					Settings.host, 
					Settings.user, 
					Settings.pswd, 
					account
				)
				# Un id_media == 0 indica que no se especifica medio alguno.
				query = """
				SELECT COUNT(DISTINCT(e.numero)), STR_TO_DATE(e.fecha, '%Y/%m')
					FROM entrantes e
					WHERE STR_TO_DATE(e.fecha, '%Y/%m') <= CURDATE() {}
					GROUP BY STR_TO_DATE(e.fecha, '%Y/%m');
				""".format("AND id_medio = {}".format(id_media) if id_media != '0' else "")
				response = db.executeQuery(query, None, True)
			else:
				# Argumentos inválidos
				error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
				error['errmsg'] = validate_arguments['message']
		else:
			# Formato JSON inválido
			error = Error.INVALID_REQUEST_BODY
	except:
		Utils.setLog()
		error = Error.PROGRAMMING_ERROR

	return wrappers.Response(
		json.dumps(response if error is None else error),
		200,
		mimetype='application/json'
	)


@chatbots_blueprint.route('/getbotnewusers', methods=['POST'])
def get_bot_new_users():
	# Variables locales
	error = None
	response = None
	account = None
	id_media = None
	since_date = '{}-{}-{}'.format(
		date.today().year, 
		date.today().month, 
		1
	)

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar argumentos válidos
			json_data = request.get_json()
			validate_arguments = Utils.areValidPostArguments(
				json_data, 
				['account', 'id_media']
			)
			if validate_arguments['status'] == 'success':
				# Crear db, query, y postear query
				account = json_data['account']
				id_media = json_data['id_media']
				db = Database.getInstance(
					Settings.host, 
					Settings.user, 
					Settings.pswd, 
					account
				)
				# Un id_media == 0 indica que no se especifica medio alguno.
				query = """
				SELECT *
					FROM (SELECT DISTINCT MIN(e.id), e.numero, e.fecha, e.id_medio
						FROM entrantes e
						GROUP BY e.numero) en
					WHERE STR_TO_DATE(en.fecha, '%Y/%m/%d') BETWEEN {} AND CURDATE() {}
					GROUP BY STR_TO_DATE(en.fecha, '%Y/%m/%d');
				""".format(
					since_date,
					"AND id_medio = {}".format(id_media) if id_media != '0' else ""
				)
				query_result = db.executeQuery(query, None, True)
				# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
				response = query_result if query_result is not () else "No matching results"
			else:
				# Argumentos inválidos
				error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
				error['errmsg'] = validate_arguments['message']
		else:
			# Formato JSON inválido
			error = Error.INVALID_REQUEST_BODY
	except:
		Utils.setLog()
		error = Error.PROGRAMMING_ERROR

	return wrappers.Response(
		json.dumps(response if error is None else error),
		200,
		mimetype='application/json'
	)