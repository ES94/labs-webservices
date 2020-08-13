import copy
import simplejson as json
from datetime import date, datetime
from collections import OrderedDict

from flask import Blueprint, request
from werkzeug import wrappers

from classes.error import Error
from classes.database import Database
from classes.jwtauth import JWTAuth
from classes.metrics import Metric
from classes.utils import Utils
from settings import Settings


__jwtPrivateKey = Settings.WS_PRIVATE_KEY
__jwtPublicKey = Settings.WS_PUBLIC_KEY
chatbots_blueprint = Blueprint('chatbots', __name__)


@chatbots_blueprint.route('/gettotalusers', methods=['POST'])
def get_bot_total_users():
	# Variables locales
	error = None
	response = None
	account = None
	id_media = None
	date_until = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar existencia del token
			token = Utils.getTokenFromHeader(request)
			if token is not None:
				# Revisar validez del token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
				decoded_token = auth.decodeToken(token)
				if 'errno' not in decoded_token:
					# Revisar argumentos válidos
					json_data = request.get_json()
					validate_arguments = Utils.areValidPostArguments(
						json_data, 
						['account', 'date_until']
					)
					if validate_arguments['status'] == 'success':
						# Crear db, query, y postear query
						account = json_data['account']
						date_until = json_data['date_until']
						id_media = json_data['id_media'] if 'id_media' in json_data else None
						db = Database.getInstance(
							Settings.WS_DB_HOST, 
							Settings.WS_DB_USER, 
							Settings.WS_DB_PSWD, 
							'_' + account
						)
						# Un id_media == None indica que no se especifica medio alguno.
						query = """
						SELECT date_format(e.fecha, '%Y/%m') fecha, count(DISTINCT e.numero) cantidad_usuarios
							FROM entrantes e
							WHERE e.fecha <= '{}' {}
							GROUP BY date_format(e.fecha, '%Y/%m');
						""".format(
							date_until,
							"AND id_medio = {}".format(id_media) if id_media else ""
						)
						query_result = db.executeQuery(query, None, True)

						# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
						if query_result:
							response = Metric.get_users_amount_by_date(query_result)
							# response = query_result
						else:
							# Sin resultados
							error = Error.NO_RESULTS
					else:
						# Argumentos inválidos
						error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
						error['errmsg'] = validate_arguments['message']
				else:
					# Token inválido
					error = decoded_token
			else:
				# Token inexistente
				error = Error.TOKEN_NOT_FOUND
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


@chatbots_blueprint.route('/getnewusers', methods=['POST'])
def get_bot_new_users():
	# Variables locales
	error = None
	response = None
	account = None
	id_media = None
	date_since = None
	date_until = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar existencia del token
			token = Utils.getTokenFromHeader(request)
			if token is not None:
				# Revisar validez del token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
				decoded_token = auth.decodeToken(token)
				if 'errno' not in decoded_token:
					# Revisar argumentos válidos
					json_data = request.get_json()
					validate_arguments = Utils.areValidPostArguments(
						json_data, 
						['account', 'date_since', 'date_until']
					)
					if validate_arguments['status'] == 'success':
						# Crear db, query, y postear query
						account = json_data['account']
						date_since = json_data['date_since']
						date_until = json_data['date_until']
						id_media = json_data['id_media'] if 'id_media' in json_data else None
						db = Database.getInstance(
							Settings.WS_DB_HOST, 
							Settings.WS_DB_USER, 
							Settings.WS_DB_PSWD, 
							'_' + account
						)
						# Un id_media == None indica que no se especifica medio alguno.
						query = """
						SELECT date_format(en.fecha, '%Y/%m'), count(en.numero)
							FROM (SELECT DISTINCT min(e.id), e.numero, e.fecha, e.id_medio
								FROM entrantes e
								GROUP BY e.numero) en
							WHERE en.fecha BETWEEN '{}' AND '{}' {}
							GROUP BY date_format(en.fecha, '%Y/%m');
						""".format(
							date_since,
							date_until,
							"AND id_medio = {}".format(id_media) if id_media else ""
						)
						query_result = db.executeQuery(query, None, True)
						
						# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
						if query_result:
							response = Metric.get_users_amount_by_date(query_result)
						else:
							error = Error.NO_RESULTS
					else:
						# Argumentos inválidos
						error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
						error['errmsg'] = validate_arguments['message']
				else:
					# Token inválido
					error = decoded_token
			else:
				# Token inexistente
				error = Error.TOKEN_NOT_FOUND
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


@chatbots_blueprint.route('/getblockersunsuscriberdusers', methods=['POST'])
def get_bot_blockers_unsuscribers():
	# Variables locales
	error = None
	response = None
	account = None
	id_media = None
	# date_since = None
	# date_until = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar existencia del token
			token = Utils.getTokenFromHeader(request)
			if token is not None:
				# Revisar validez del token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
				decoded_token = auth.decodeToken(token)
				if 'errno' not in decoded_token:
					# Revisar argumentos válidos
					json_data = request.get_json()
					validate_arguments = Utils.areValidPostArguments(
						json_data, 
						['account']#, 'date_since', 'date_until']
					)
					if validate_arguments['status'] == 'success':
						# Crear db, query, y postear query
						account = json_data['account']
						# date_since = json_data['date_since']
						# date_until = json_data['date_until']
						id_media = json_data['id_media'] if 'id_media' in json_data else None
						db = Database.getInstance(
							Settings.WS_DB_HOST, 
							Settings.WS_DB_USER, 
							Settings.WS_DB_PSWD, 
							'_' + account
						)
						# Un id_media == None indica que no se especifica medio alguno.
						query = """
						SELECT count(DISTINCT b.numero) usuarios_dados_baja
							FROM bajas b;
						"""
						query_result = db.executeQuery(query, None, True)
						# Chequear en cada medio algun bloqueo y contrastarlo con las bajas.
						# Todos los medios
						if (id_media == None):
							pass
						# Whatsapp
						if(id_media == 1):
							pass
						# Facebook
						if (id_media == 2):
							pass
						# Instagram
						if (id_media == 3):
							pass
						
						# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
						if query_result:
							response = OrderedDict([
								('cantidad_bajas', query_result[0][0])
							])
						else:
							error = Error.NO_RESULTS
					else:
						# Argumentos inválidos
						error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
						error['errmsg'] = validate_arguments['message']
				else:
					# Token inválido
					error = decoded_token
			else:
				# Token inexistente
				error = Error.TOKEN_NOT_FOUND
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


@chatbots_blueprint.route('/getsuscribedusers', methods=['POST'])
def get_bot_suscribed_users():
	# Variables locales
	error = None
	response = None
	account = None
	id_media = None
	date_since = None
	date_until = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar existencia del token
			token = Utils.getTokenFromHeader(request)
			if token is not None:
				# Revisar validez del token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
				decoded_token = auth.decodeToken(token)
				if 'errno' not in decoded_token:
					# Revisar argumentos válidos
					json_data = request.get_json()
					validate_arguments = Utils.areValidPostArguments(
						json_data, 
						['account', 'date_since', 'date_until']
					)
					if validate_arguments['status'] == 'success':
						# Crear db, query, y postear query
						account = json_data['account']
						date_since = json_data['date_since']
						date_until = json_data['date_until']
						id_media = json_data['id_media'] if 'id_media' in json_data else None
						db = Database.getInstance(
							Settings.WS_DB_HOST, 
							Settings.WS_DB_USER, 
							Settings.WS_DB_PSWD, 
							'_' + account
						)
						# Un id_media == None indica que no se especifica medio alguno.
						query = """
						SELECT count(DISTINCT s.numero) cantidad_usuarios_suscriptos
							FROM cd_suscripciones s
							WHERE s.fecha_alta BETWEEN '{}' AND '{}' {};
						""".format(
							date_since,
							date_until,
							"AND s.canal = {}".format(id_media) if id_media else ""
						)
						query_result = db.executeQuery(query, None, True)

						# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
						if query_result:
							response = OrderedDict([
								('cantidad_suscriptos', query_result[0][0])
							])
						else:
							error = Error.NO_RESULTS
					else:
						# Argumentos inválidos
						error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
						error['errmsg'] = validate_arguments['message']
				else:
					# Token inválido
					error = decoded_token
			else:
				# Token inexistente
				error = Error.TOKEN_NOT_FOUND
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
	date_since = None
	date_until = None
	words_limit = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar existencia del token
			token = Utils.getTokenFromHeader(request)
			if token is not None:
				# Revisar validez del token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
				decoded_token = auth.decodeToken(token)
				if 'errno' not in decoded_token:
					# Revisar argumentos válidos
					json_data = request.get_json()
					validate_arguments = Utils.areValidPostArguments(
						json_data, 
						['account', 'date_since', 'date_until']
					)
					if validate_arguments['status'] == 'success':
						# Crear db, query, y postear query
						account = json_data['account']
						date_since = json_data['date_since']
						date_until = json_data['date_until']
						id_media = json_data['id_media'] if 'id_media' in json_data else None
						words_limit = json_data['words_limit'] if 'words_limit' in json_data else 10
						db = Database.getInstance(
							Settings.WS_DB_HOST, 
							Settings.WS_DB_USER, 
							Settings.WS_DB_PSWD, 
							'_' + account
						)
						# Un id_media == None indica que no se especifica medio alguno.
						query = """
						SELECT e.mensaje palabraclave, count(e.mensaje) cantidad 
							FROM entrantes e
							INNER JOIN fcb_administrar a ON e.mensaje = a.palabra
							WHERE e.fecha BETWEEN '{}' AND '{}' {}
							GROUP BY e.mensaje
							ORDER BY count(e.mensaje) DESC
							LIMIT {};
						""".format(
							date_since,
							date_until,
							"AND id_medio = {}".format(id_media) if id_media else "",
							words_limit
						)
						query_result = db.executeQuery(query, None, True)

						# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
						if query_result:
							response = Metric.get_keywords_usage_count(query_result)
						else:
							error = Error.NO_RESULTS
					else:
						# Argumentos inválidos
						error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
						error['errmsg'] = validate_arguments['message']
				else:
					# Token inválido
					error = decoded_token
			else:
				# Token inexistente
				error = Error.TOKEN_NOT_FOUND
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


@chatbots_blueprint.route('/gettotalderivedusers', methods=['POST'])
def get_total_chat_derived_users():
	# Variables locales
	error = None
	response = None
	account = None
	id_media = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar existencia del token
			token = Utils.getTokenFromHeader(request)
			if token is not None:
				# Revisar validez del token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
				decoded_token = auth.decodeToken(token)
				if 'errno' not in decoded_token:
					# Revisar argumentos válidos
					json_data = request.get_json()
					validate_arguments = Utils.areValidPostArguments(
						json_data, 
						['account']
					)
					if validate_arguments['status'] == 'success':
						# Crear db, query, y postear query
						account = json_data['account']
						id_media = json_data['id_media'] if 'id_media' in json_data else None
						db = Database.getInstance(
							Settings.WS_DB_HOST, 
							Settings.WS_DB_USER, 
							Settings.WS_DB_PSWD, 
							'_' + account
						)
						# Un id_media == None indica que no se especifica medio alguno.
						query = """
						SELECT count(c.id) usuarios_totales_derivados_al_chat
							FROM chat c {};
						""".format(
							"WHERE id_medio = {}".format(id_media) if id_media else ""
						)
						query_result = db.executeQuery(query, None, True)

						# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
						if query_result:
							response = OrderedDict([
								('cantidad_derivados', query_result[0][0])
							])
						else:
							error = Error.NO_RESULTS
					else:
						# Argumentos inválidos
						error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
						error['errmsg'] = validate_arguments['message']
				else:
					# Token inválido
					error = decoded_token
			else:
				# Token inexistente
				error = Error.TOKEN_NOT_FOUND
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


@chatbots_blueprint.route('/getderivedusersbetweendates', methods=['POST'])
def get_chat_derived_users_between_dates():
	# Variables locales
	error = None
	response = None
	account = None
	id_media = None
	date_since = None
	date_until = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar existencia del token
			token = Utils.getTokenFromHeader(request)
			if token is not None:
				# Revisar validez del token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
				decoded_token = auth.decodeToken(token)
				if 'errno' not in decoded_token:
					# Revisar argumentos válidos
					json_data = request.get_json()
					validate_arguments = Utils.areValidPostArguments(
						json_data, 
						['account', 'date_since', 'date_until']
					)
					if validate_arguments['status'] == 'success':
						# Crear db, query, y postear query
						account = json_data['account']
						date_since = json_data['date_since']
						date_until = json_data['date_until']
						id_media = json_data['id_media'] if 'id_media' in json_data else None
						db = Database.getInstance(
							Settings.WS_DB_HOST, 
							Settings.WS_DB_USER, 
							Settings.WS_DB_PSWD, 
							'_' + account
						)
						# Un id_media == None indica que no se especifica medio alguno.
						query = """
						SELECT count(c.id) usuarios_totales_derivados_al_chat
							FROM chat c
							WHERE c.hora_inicio BETWEEN '{}' AND '{}' {};
						""".format(
							date_since,
							date_until,
							"AND id_medio = {}".format(id_media) if id_media else ""
						)
						query_result = db.executeQuery(query, None, True)

						# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
						if query_result:
							response = OrderedDict([
								('cantidad_derivados', query_result[0][0])
							])
						else:
							error = Error.NO_RESULTS
					else:
						# Argumentos inválidos
						error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
						error['errmsg'] = validate_arguments['message']
				else:
					# Token inválido
					error = decoded_token
			else:
				# Token inexistente
				error = Error.TOKEN_NOT_FOUND
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


@chatbots_blueprint.route('/gettopusers', methods=['POST'])
def get_chat_top_users():
	# Variables locales
	error = None
	response = None
	account = None
	date_since = None
	date_until = None
	users_limit = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar existencia del token
			token = Utils.getTokenFromHeader(request)
			if token is not None:
				# Revisar validez del token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
				decoded_token = auth.decodeToken(token)
				if 'errno' not in decoded_token:
					# Revisar argumentos válidos
					json_data = request.get_json()
					validate_arguments = Utils.areValidPostArguments(
						json_data, 
						['account', 'date_since', 'date_until']
					)
					if validate_arguments['status'] == 'success':
						# Crear db, query, y postear query
						account = json_data['account']
						date_since = json_data['date_since']
						date_until = json_data['date_until']
						users_limit = json_data['users_limit'] if 'users_limit' in json_data else 5
						db = Database.getInstance(
							Settings.WS_DB_HOST, 
							Settings.WS_DB_USER, 
							Settings.WS_DB_PSWD, 
							'_' + account
						)
						# Un id_media == None indica que no se especifica medio alguno.
						query = """
						SELECT DISTINCT e.numero top_usuarios, count(e.numero) cantidad_mensajes
							FROM entrantes e
							WHERE e.fecha BETWEEN '{}' AND '{}'
							GROUP BY e.numero
							ORDER BY count(e.numero) DESC
							LIMIT {};
						""".format(
							date_since,
							date_until,
							users_limit
						)
						query_result = db.executeQuery(query, None, True)

						# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
						if query_result:
							response = Metric.get_top_users(query_result)
						else:
							error = Error.NO_RESULTS
					else:
						# Argumentos inválidos
						error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
						error['errmsg'] = validate_arguments['message']
				else:
					# Token inválido
					error = decoded_token
			else:
				# Token inexistente
				error = Error.TOKEN_NOT_FOUND
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


@chatbots_blueprint.route('/getsessionstime', methods=['POST'])
def get_sessions_time():
	# Variables locales
	error = None
	response = None
	account = None
	date_since = None
	date_until = None
	id_media = None
	sessions_details = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar existencia del token
			token = Utils.getTokenFromHeader(request)
			if token is not None:
				# Revisar validez del token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
				decoded_token = auth.decodeToken(token)
				if 'errno' not in decoded_token:
					# Revisar argumentos válidos
					json_data = request.get_json()
					validate_arguments = Utils.areValidPostArguments(
						json_data, 
						['account', 'date_since', 'date_until', 'id_media', 'sessions_details']
					)
					if validate_arguments['status'] == 'success':
						# Crear db, query, y postear query
						account = json_data['account']
						date_since = json_data['date_since']
						date_until = json_data['date_until']
						id_media = json_data['id_media']
						sessions_details = bool(json_data['sessions_details'] == 'True')
						db = Database.getInstance(
							Settings.WS_DB_HOST, 
							Settings.WS_DB_USER, 
							Settings.WS_DB_PSWD, 
							'_' + account
						)
						# Un id_media == None indica que no se especifica medio alguno.
						query = """
						SELECT e.numero usuario, date_format(e.fecha, '%Y/%m/%d %H:%i:%S') fecha
							FROM entrantes e
							WHERE e.fecha BETWEEN '{}' AND '{}' 
							AND id_medio = {}
							ORDER BY e.numero, e.id;
						""".format(date_since, date_until, id_media)
						query_result = db.executeQuery(query, None, True)

						# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
						if query_result:
							response = Metric.get_sessions_time(
								query_result, 
								Settings.MAX_SESSION_TIME, 
								sessions_details
							)
						else:
							error = Error.NO_RESULTS
					else:
						# Argumentos inválidos
						error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
						error['errmsg'] = validate_arguments['message']
				else:
					# Token inválido
					error = decoded_token
			else:
				# Token inexistente
				error = Error.TOKEN_NOT_FOUND
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


@chatbots_blueprint.route('/getinteractions', methods=['POST'])
def get_interactions():
	# Variables locales
	error = None
	response = None
	account = None
	date_since = None
	date_until = None
	id_media = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar existencia del token
			token = Utils.getTokenFromHeader(request)
			if token is not None:
				# Revisar validez del token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
				decoded_token = auth.decodeToken(token)
				if 'errno' not in decoded_token:
					# Revisar argumentos válidos
					json_data = request.get_json()
					validate_arguments = Utils.areValidPostArguments(
						json_data, 
						['account', 'date_since', 'date_until', 'id_media']
					)
					if validate_arguments['status'] == 'success':
						# Crear db, query, y postear query
						account = json_data['account']
						date_since = json_data['date_since']
						date_until = json_data['date_until']
						id_media = json_data['id_media']
						db = Database.getInstance(
							Settings.WS_DB_HOST, 
							Settings.WS_DB_USER, 
							Settings.WS_DB_PSWD, 
							'_' + account
						)
						query = """
						SELECT date_format(str_to_date(e.fecha, '%Y/%m/%d %H:%i:%s'), '%Y/%m/%d') as fecha, 
							date_format(str_to_date(e.fecha, '%Y/%m/%d %H:%i:%s'), '%H') as hora, 
							count(*) cant_mensajes, count(DISTINCT e.numero) cant_usuarios
							FROM entrantes e
							WHERE e.fecha BETWEEN '{}' AND '{}'
								AND id_medio = {}
							GROUP BY date_format(str_to_date(e.fecha, '%Y/%m/%d %H:%i:%s'), '%Y/%m/%d'), 
								date_format(str_to_date(e.fecha, '%Y/%m/%d %H:%i:%s'), '%H')
							ORDER BY DATE_FORMAT(str_to_date(e.fecha, '%Y/%m/%d %H:%i:%s'), '%Y/%m/%d %H:%i:%s') ASC;
						""".format(date_since, date_until, id_media)
						query_result = db.executeQuery(query, None, True)

						# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
						if query_result:
							response = Metric.get_interactions(query_result)
						else:
							error = Error.NO_RESULTS
					else:
						# Argumentos inválidos
						error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
						error['errmsg'] = validate_arguments['message']
				else:
					# Token inválido
					error = decoded_token
			else:
				# Token inexistente
				error = Error.TOKEN_NOT_FOUND
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


@chatbots_blueprint.route('/getopenforms', methods=['POST'])
def get_open_forms():
	error = None
	response = None
	account = None
	date_since = None
	date_until = None
	id_media = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar existencia del token
			token = Utils.getTokenFromHeader(request)
			if token is not None:
				# Revisar validez del token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
				decoded_token = auth.decodeToken(token)
				if 'errno' not in decoded_token:
					# Revisar argumentos válidos
					json_data = request.get_json()
					validate_arguments = Utils.areValidPostArguments(
						json_data, 
						['account', 'date_since', 'date_until']
					)
					if validate_arguments['status'] == 'success':
						# Crear db, query, y postear query
						account = json_data['account']
						date_since = json_data['date_since']
						date_until = json_data['date_until']
						#id_media = json_data['id_media']
						db = Database.getInstance(
							Settings.WS_DB_HOST, 
							Settings.WS_DB_USER, 
							Settings.WS_DB_PSWD, 
							'_' + account
						)
						query_forms = """
						SELECT DISTINCT descripcion, nombre_tabla
							FROM formularios_adm
						"""
						forms_list = db.executeQuery(query_forms, None, True)
						query_result = ()
						for form in forms_list:
							query = """
							SELECT '{}' formulario,
								date_format(f.fecha_inicio, '%Y/%m') fecha, 
								count(f.identificador) cant_formularios, 
								count(DISTINCT f.identificador) cant_usuarios
								FROM {} f
								WHERE f.fecha_inicio BETWEEN '{}' AND '{}'
									AND f.fecha_fin = '' OR f.fecha_fin IS NULL
								GROUP BY date_format(f.fecha_inicio, '%Y/%m');
							""".format(form[0], form[1], date_since, date_until)
							query_result += db.executeQuery(query, None, True)

						# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
						if query_result:
							response = Metric.get_forms(query_result)
						else:
							error = Error.NO_RESULTS
					else:
						# Argumentos inválidos
						error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
						error['errmsg'] = validate_arguments['message']
				else:
					# Token inválido
					error = decoded_token
			else:
				# Token inexistente
				error = Error.TOKEN_NOT_FOUND
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


@chatbots_blueprint.route('/getsendedforms', methods=['POST'])
def get_send_forms():
	error = None
	response = None
	account = None
	date_since = None
	date_until = None
	id_media = None

	try:
		# Revisar formato JSON
		valid_json_data = Utils.isValidJsonData(request)
		if valid_json_data:
			# Revisar existencia del token
			token = Utils.getTokenFromHeader(request)
			if token is not None:
				# Revisar validez del token
				auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)
				decoded_token = auth.decodeToken(token)
				if 'errno' not in decoded_token:
					# Revisar argumentos válidos
					json_data = request.get_json()
					validate_arguments = Utils.areValidPostArguments(
						json_data, 
						['account', 'date_since', 'date_until']
					)
					if validate_arguments['status'] == 'success':
						# Crear db, query, y postear query
						account = json_data['account']
						date_since = json_data['date_since']
						date_until = json_data['date_until']
						#id_media = json_data['id_media']
						db = Database.getInstance(
							Settings.WS_DB_HOST, 
							Settings.WS_DB_USER, 
							Settings.WS_DB_PSWD, 
							'_' + account
						)
						query_forms = """
						SELECT DISTINCT descripcion, nombre_tabla
							FROM formularios_adm
						"""
						forms_list = db.executeQuery(query_forms, None, True)
						query_result = ()
						for form in forms_list:
							query = """
							SELECT '{}' formulario,
								date_format(f.fecha_inicio, '%Y/%m') fecha, 
								count(f.identificador) cant_formularios, 
								count(DISTINCT f.identificador) cant_usuarios
								FROM {} f
								WHERE f.fecha_inicio BETWEEN '{}' AND '{}'
									AND f.fecha_fin <> '' OR f.fecha_fin IS NOT NULL
								GROUP BY date_format(f.fecha_inicio, '%Y/%m');
							""".format(form[0], form[1], date_since, date_until)
							query_result += db.executeQuery(query, None, True)
							print(query_result)

						# Si la query trae resultados, devolverlos. Caso contrario, un mensaje.
						if query_result:
							response = Metric.get_forms(query_result)
						else:
							error = Error.NO_RESULTS
					else:
						# Argumentos inválidos
						error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
						error['errmsg'] = validate_arguments['message']
				else:
					# Token inválido
					error = decoded_token
			else:
				# Token inexistente
				error = Error.TOKEN_NOT_FOUND
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