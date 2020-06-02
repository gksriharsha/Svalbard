from flask import render_template, url_for, flash, redirect, request
from Svalbard import app, db
from Svalbard.forms import RegistrationForm, LoginForm, SearchForm, SubSearchForm
from Svalbard.models import Result, Dataset


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page',1,type=int)
    results = Result.query.order_by(Result.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('home.html', results=results)


@app.route("/search", methods =['GET','POST'])
def search():    
    page = request.args.get('page',1,type=int)
    search = SearchForm()
    search.Process.choices = [(r.process,str(r.process)) for r in db.session.query(Result.process).distinct()]
    search.Task.choices = [(r.task,str(r.task)) for r in db.session.query(Result.task).distinct()]
    search.Platform.choices = [(r.platform,str(r.platform)) for r in db.session.query(Result.platform).distinct()]
    search.Dataset.choices = [(r.dataset_id,str(Dataset.query.filter_by(id=r.dataset_id).first().dataset_name)) for r in db.session.query(Result.dataset_id).distinct()]
    if search.is_submitted():
        results = Result.query
        if search.TaskCheck.data:
            results = results.filter_by(task=search.Task.data)
        if search.ProcessCheck.data:
            results = results.filter_by(process=search.Process.data)
        if search.PlatformCheck.data:
            results = results.filter_by(platform=search.Platform.data)
        if search.DatasetCheck.data:
            results = results.filter_by(dataset_id=search.Dataset.data)
        return render_template('search.html', title='Results', results=results, form=search)
    return render_template('search.html', title='Search Space', form=search)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/task/<string:task>")
def ML_task(task):
    page = request.args.get('page',1,type=int)
    results = Result.query.filter_by(task=task).order_by(Result.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('task.html', title='Task', task=task, results=results)


@app.route("/process/<string:process>")
def process(process):
    page = request.args.get('page',1,type=int)
    results = Result.query.filter_by(process=process).order_by(Result.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('process.html', title='Process', process=process, results=results)


@app.route("/platform/<string:platform>")
def ML_platform(platform):
    page = request.args.get('page',1,type=int)
    results = Result.query.filter_by(platform=platform).order_by(Result.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('platform.html', title='Language', platform=platform, results=results)


@app.route("/dataset/<string:dataset>")
def ML_dataset(dataset):
    page = request.args.get('page',1,type=int)
    results = Result.query.filter_by(dataset_id=dataset).order_by(Result.date_posted.desc()).paginate(page=page,per_page=5)
    dataset_name = Dataset.query.filter_by(
        id=dataset).first_or_404().dataset_name
    return render_template('dataset.html', title='Language', dataset=dataset_name, results=results, dataset_id=dataset)
