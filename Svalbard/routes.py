from flask import render_template, url_for, flash, redirect, request
from Svalbard import app
from Svalbard.forms import RegistrationForm, LoginForm
from Svalbard.models import Result, Dataset


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page',1,type=int)
    results = Result.query.order_by(Result.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('home.html', results=results)


@app.route("/search")
def search():
    results = Result.query.all()
    return render_template('search.html', title='Search Space', results=results)


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
