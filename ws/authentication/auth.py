import copy
from collections import OrderedDict

import simplejson as json
from flask import request
from werkzeug import wrappers

from . import auth_blueprint
from classes.database import Database
from classes.error import Error
from classes.jwtauth import JWTAuth
from classes.procedure import Procedure
from classes.utils import Utils
from settings import Settings


__jwtPrivateKey = Settings.WS_PRIVATE_KEY
__jwtPublicKey = Settings.WS_PUBLIC_KEY


@auth_blueprint.route('/getauth', methods=['POST'])
def get_auth():
    error = None
    response = None

    try:
        # Revisa que el body de la petición sea un json válido
        validJsonData = Utils.isValidJsonData(request)
        if validJsonData == True:
            jsonData = request.get_json()

            # Revisa que en el json esten los argumentos necesarios. En este caso, user y password
            validateArguments = Utils.areValidPostArguments(
                jsonData, ["username", "password"])
            if validateArguments['status'] == 'success':
                # Crea instancia de DB, arma tupla de argumentos y llama al SP correspondiente
                DATABASE = Database.getInstance(
                    Settings.PLATFORM_DB_HOST, 
                    Settings.PLATFORM_DB_USER, 
                    Settings.PLATFORM_DB_PSWD, 
                    Settings.PLATFORM_DB_NAME
                )
                username = jsonData["username"]
                password = jsonData["password"]
                args = (username, password, 0,)
                res = DATABASE.callProc(Procedure.GET_USER_API, args, False)

                # Si res es NONE, no trajo resultados el SP
                if res is None:
                    error = Error.INVALID_USER
                else:
                    # Si el usuario existe, genera el token
                    auth = JWTAuth(__jwtPrivateKey, __jwtPublicKey)

                    # 1: Cantidad de días de vigencia del token
                    # user-api-: SUBJECT del token, meramente informativo. Podemos usar el id del usuario y que es de la api
                    userId = res["id"]
                    token = auth.encodeToken(1, 'user-api-' + str(userId))
                    if token is not None:
                        response = OrderedDict([
                            ("token", token["token"]),
                            ("expires", token["expires"].isoformat())
                        ])
                    else:
                        error = Error.TOKEN_GENERATION_ERROR
            else:
                # Si hay que modificar algo del mensaje, se hace un deepcopy, no modificamos directamente la variable porque es estatica
                error = copy.deepcopy(Error.REQUIRED_ARGUMENTS)
                error["errmsg"] = error["errmsg"].format(validateArguments[1])
        else:
            error = Error.INVALID_REQUEST_BODY
    except:
        Utils.setLog()
        error = Error.PROGRAMMING_ERROR

    return wrappers.Response(
        json.dumps(response if error is None else error), 200, mimetype='application/json'
    )