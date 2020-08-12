import os

class Settings:
    ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
    WS_PRIVATE_KEY = ROOT_PATH + r"\keys\private.key"
    WS_PUBLIC_KEY = ROOT_PATH + r"\keys\public.key"
    MAX_SESSION_TIME = 3600
    PLATFORM_DB_HOST = '127.0.0.1'
    PLATFORM_DB_USER = 'root'
    PLATFORM_DB_PSWD = ''
    PLATFORM_DB_NAME = 'dev_plataforma'
    WS_DB_HOST = '127.0.0.1'
    WS_DB_USER = 'root'
    WS_DB_PSWD = ''