from wtforms import BooleanField, Form, StringField, validators


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    rules = BooleanField('I accept the site rules',
                         [validators.InputRequired()])
