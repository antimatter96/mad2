import time
import bcrypt
import hashlib

from flask import current_app as app
from flask import request
from flask import render_template, redirect, url_for, session

from application.models.user import User

from application.database.index import db
from application.errors import FieldsNotValidError
from application.controllers.utils import get_redirect_error, flatten_from_errors
from application.controllers.decorators import ensure_logged_in
from application.controllers.user.form import SigninForm, SignupForm

@app.route("/search_by_prefix", methods=['GET'])
def render_signup():
  prefix = request.args.get('search_text', "").strip()
  if prefix != "":
    try:
      return "RedirectError(decored_redirect_error)"
    except:
      return None

