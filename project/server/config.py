import os

basedir = os.path.abspath(os.path.dirname(__file__))

print("basedir", basedir)

class Config():
  DEBUG = False
  SQLITE_DB_DIR = None
  SQLALCHEMY_DATABASE_URI = None
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_ECHO = False

  SECURITY_FLASH_MESSAGES = False
  SECURITY_DEFAULT_REMEMBER_ME = True
  SECURITY_URL_PREFIX = '/api/accounts'

  # Turn on all the great Flask-Security features
  SECURITY_REGISTERABLE = True
  SECURITY_SEND_REGISTER_EMAIL = False

  # These need to be defined to handle redirects
  # As defined in the API documentation - they will receive the relevant context
  SECURITY_REDIRECT_BEHAVIOR = "spa"

  # CSRF protection is critical for all session-based browser UIs

  # enforce CSRF protection for session / browser - but allow token-based
  # API calls to go through
  SECURITY_CSRF_PROTECT_MECHANISMS = ["session", "basic"]
  SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True

  # Send Cookie with csrf-token. This is the default for Axios and Angular.
  SECURITY_CSRF_COOKIE_NAME = "XSRF-TOKEN"
  WTF_CSRF_CHECK_DEFAULT = False
  WTF_CSRF_TIME_LIMIT = None

  SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"


class NonProdConfig(Config):
  DEBUG = True

class LocalDevelopmentConfig(NonProdConfig):
  SQLITE_DB_DIR = os.path.join(basedir, "./db_directory")
  SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "local.sqlite3")
  SECRET_KEY = "ash ah secet"
  SECURITY_PASSWORD_HASH = "bcrypt"
  SECURITY_PASSWORD_SALT = "really super secret"
  SQLALCHEMY_ECHO = True


class TestingConfig(NonProdConfig):
  SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
  SECRET_KEY = "ash ah secet"
  SECURITY_PASSWORD_HASH = "bcrypt"
  SECURITY_PASSWORD_SALT = "really super secret"
  WTF_CSRF_ENABLED = False
