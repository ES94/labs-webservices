import sys
from datetime import date, datetime, timedelta
import jwt
from classes.error import Error
import pytz
import traceback
import inspect

class JWTAuth:
	privateKey = None
	publicKey = None
	
	def __init__(self, privateKey, publicKey):
		"""
		Return JWTAuth instance\n
		Param: RSA privateKey -> Private key path\n
		Param: RSA publicKey -> Public key path\n
		"""
		self.privateKey = privateKey
		self.publicKey = publicKey
	
	@staticmethod
	def __setLog():
		try:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			error = repr(traceback.format_exception("", exc_value, exc_traceback))
			origin = inspect.stack()[1][3]

			now = datetime.now()
			time = now.strftime("%d/%m/%Y %H:%M:%S")
			stringError = str(time) + " --- " + str(origin) + ": " + str(error) + "\n"
			with open(r"D:\eniac\LABS357 Dashboard\API Labs\API\v1\logs\jwtAuth.log", "a") as logFile:
				logFile.write(stringError)
		except Exception as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			error = repr(traceback.format_exception("", exc_value, exc_traceback))
			origin = inspect.stack()[1][3]
			
			now = datetime.now()
			time = now.strftime("%d/%m/%Y %H:%M:%S")
			stringError = str(time) + " --- " + str(origin) + ": " + str(error) + "\n"
			with open(r"D:\eniac\LABS357 Dashboard\API Labs\API\v1\logs\jwtAuth.log", "a") as logFile:
				logFile.write(stringError)
	
	def __getPrivateKey(self):
		try:
			with open(self.privateKey) as pk:
				return pk.read()
			return None
		except Exception:
			JWTAuth.__setLog()
			return None

	def __getPublicKey(self):
		try:
			with open(self.publicKey) as pk:
				return pk.read()
			return None
		except Exception:
			JWTAuth.__setLog()
			return None            

	def encodeToken(self, days, subject):
		"""
		Generates the Auth Token\n
		Param: days -> Days from now for token expiration\n
		Param: subject -> Subject of token request\n
		Return: {\n
			token: <token string>,\n
			expires: <expiration date>\n
		}
		"""
		try:
			exp = datetime.utcnow() + timedelta(days=days)
			payload = {
				'exp': exp,
				'iat': datetime.utcnow(),
				'sub': subject
			}
			key = self.__getPrivateKey()
			if key is not None:
				token = jwt.encode(payload, key, algorithm='RS256')
				tz = pytz.timezone('America/Argentina/Buenos_Aires')
				exp = exp.replace(tzinfo=pytz.UTC)
				return {
					"token": token, 
					"expires": exp.astimezone(tz)
				}
			
			return None
		except Exception:
			JWTAuth.__setLog()
			return None

	def decodeToken(self, auth_token):
		"""
		Decodes the auth token\n
		Param: auth_token -> Token previously generated\n
		Return: {\n
			status: <ok|error>,\n
			sub: <subject>
		}
		"""
		try:
			key = self.__getPublicKey()
			
			if key is not None:
				payload = jwt.decode(auth_token, key, algorithms=['RS256'])
				return {
					"status": "ok", 
					"sub": payload['sub']
				}
			return None
		except jwt.ExpiredSignatureError:
			return Error.EXPIRED_TOKEN
		except jwt.InvalidTokenError as e:
			return Error.INVALID_TOKEN
		except Exception:
			JWTAuth.__setLog()
			return None
