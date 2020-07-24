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
	since_date = None
	until_date = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar argumentos válidos
			json_data = request.get_json()
			validate_arguments = Utils.areValidPostArguments(
				json_data, 
				['account', 'since_date', 'until_date']
			)
			if validate_arguments['status'] == 'success':
				# Crear db, query, y postear query
				account = json_data['account']
				since_date = json_data['since_date']
				until_date = json_data['until_date']
				id_media = json_data['id_media'] if 'id_media' in json_data else None
				db = Database.getInstance(
					Settings.host, 
					Settings.user, 
					Settings.pswd, 
					account
				)
				# Un id_media == 0 indica que no se especifica medio alguno.
				query = """
				SELECT date_format(e.fecha, '%Y/%m'), count(DISTINCT e.numero)
					FROM entrantes e
					WHERE e.fecha BETWEEN '{}' AND '{}' {}
					GROUP BY date_format(e.fecha, '%Y/%m');
				""".format(
					since_date,
					until_date,
					"AND id_medio = {}".format(id_media) if id_media != None else ""
				)
				query_result = db.executeQuery(query, None, True)
				# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
				response = query_result if query_result is not () else Error.NO_RESULTS
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
	since_date = None
	until_date = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar argumentos válidos
			json_data = request.get_json()
			validate_arguments = Utils.areValidPostArguments(
				json_data, 
				['account', 'since_date', 'until_date']
			)
			if validate_arguments['status'] == 'success':
				# Crear db, query, y postear query
				account = json_data['account']
				since_date = json_data['since_date']
				until_date = json_data['until_date']
				id_media = json_data['id_media'] if 'id_media' in json_data else None
				db = Database.getInstance(
					Settings.host, 
					Settings.user, 
					Settings.pswd, 
					account
				)
				# Un id_media == 0 indica que no se especifica medio alguno.
				query = """
				SELECT date_format(en.fecha, '%Y/%m'), count(en.numero)
					FROM (SELECT DISTINCT min(e.id), e.numero, e.fecha, e.id_medio
						FROM entrantes e
						GROUP BY e.numero) en
					WHERE en.fecha BETWEEN '{}' AND '{}' {}
					GROUP BY date_format(en.fecha, '%Y/%m');
				""".format(
					since_date,
					until_date,
					"AND id_medio = {}".format(id_media) if id_media != None else ""
				)
				query_result = db.executeQuery(query, None, True)
				# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
				response = query_result if query_result is not () else Error.NO_RESULTS
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


@chatbots_blueprint.route('/getbubbleskeywordsusage', methods=['POST'])
def get_bubbles_keywords_usage():
	# Variables locales
	error = None
	response = None
	account = None
	id_media = None
	since_date = None
	until_date = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar argumentos válidos
			json_data = request.get_json()
			validate_arguments = Utils.areValidPostArguments(
				json_data, 
				['account', 'since_date', 'until_date']
			)
			if validate_arguments['status'] == 'success':
				# Crear db, query, y postear query
				account = json_data['account']
				since_date = json_data['since_date']
				until_date = json_data['until_date']
				id_media = json_data['id_media'] if 'id_media' in json_data else None
				db = Database.getInstance(
					Settings.host, 
					Settings.user, 
					Settings.pswd, 
					account
				)
				# Un id_media == 0 indica que no se especifica medio alguno.
				query = """
				SELECT e.mensaje palabraclave, count(e.mensaje) cantidad 
    				FROM entrantes e
    				INNER JOIN fcb_administrar a ON e.mensaje = a.palabra
    				WHERE e.fecha BETWEEN '{}' AND '{}' {}
    				GROUP BY e.mensaje
    				ORDER BY count(e.mensaje) DESC;
				""".format(
					since_date,
					until_date,
					"AND id_medio = {}".format(id_media) if id_media != None else ""
				)
				query_result = db.executeQuery(query, None, True)
				# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
				response = query_result if query_result is not () else Error.NO_RESULTS
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