from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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

