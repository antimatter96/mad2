import os
import logging

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_sse import sse

from config import LocalDevelopmentConfig, TestingConfig

from application.controllers.restful.index import api
from application.database.models.user import User, Role
from application.database.index import db
from application.background_workers.index import celery as celery_worker, TaskWithContext
from cache import cache

from application.extras.new_user_form import ExtendedRegisterForm

app = None
config = None
celery = None

def create_app():
  app = Flask(__name__, template_folder="templates")

  env = os.getenv('ENV', "development")
  if env == 'production':
    raise Exception("Not specified")
  elif env == 'development':
    app.config.from_object(LocalDevelopmentConfig)
    app.logger.info("Using Local Developlent Config")
  elif env == 'testing':
    app.config.from_object(TestingConfig)

  app.logger.info("Database Setup")
  db.init_app(app)
  app.app_context().push()
  migrate = Migrate(app, db)
  app.logger.info("Database Migrated")

  csrf = CSRFProtect()
  csrf.init_app(app)

  # api.decorators.append(csrf.exempt)

  CORS(app)

  api.init_app(app)
  app.app_context().push()

  user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
  app.security = Security(app, user_datastore, register_form=ExtendedRegisterForm)
  app.app_context().push()

  celery = celery_worker
  celery.conf.update(
      broker_url=app.config['CELERY_BROKER_URL'],
      result_backend=app.config['CELERY_RESULT_BACKEND'],
  )
  celery.Task = TaskWithContext
  app.app_context().push()

  app.logger.info("App setup complete")

  logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
  return app, celery

app, celery = create_app()
cache.init_app(app)
app.app_context().push()

from application.controllers.index import *

app.register_blueprint(sse, url_prefix='/stream')
app.app_context().push()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
