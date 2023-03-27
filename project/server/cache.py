import os
from flask import config as flask_config
from flask_caching import Cache

from config import LocalDevelopmentConfig, TestingConfig

_configClass = None

env = os.getenv('ENV', "development")
if env == 'production':
  raise Exception("Not specified")
elif env == 'development':
  _configClass = LocalDevelopmentConfig
elif env == 'testing':
  _configClass = TestingConfig

_config = flask_config.Config(_configClass())
_config.from_object(_configClass())
cache = Cache(config=_config.get_namespace("CACHE_", trim_namespace=True))
