from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    Process = SelectField('Process', id='process-select')
    ProcessCheck = BooleanField(
        'Process', default="checked", id='isProcessChecked')
    Task = SelectField('Task', id='task-select')
    TaskCheck = BooleanField('Task', default="checked", id='isTaskChecked')
    Dataset = SelectField('Dataset', id='dataset-select')
    DatasetCheck = BooleanField(
        'Dataset', default="checked", id='isDatasetChecked')
    Platform = SelectField('Platform', id='platform-select')
    PlatformCheck = BooleanField(
        'Platform', default="checked", id='isPlatformChecked')
    submit = SubmitField('Search')


class SubSearchForm(FlaskForm):
    submit = SubmitField('Search')


if __name__ == '__main__':
    clf = SubSearchForm(['K', 'weights', 'algorithm'])
    print(clf)
