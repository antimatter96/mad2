from functools import wraps

from flask import current_app as app
from flask import session, redirect, url_for

from application.models.user import User

from application.database.index import db
