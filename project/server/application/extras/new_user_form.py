from flask_security import ConfirmRegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
  name = StringField('Full Name', [DataRequired()])
