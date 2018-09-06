from flask import request, jsonify,render_template,redirect,flash,url_for,session
from functools import wraps
from app import app
from .models import data_query,insert_tables
from .forms import LoginForm,CurlForm,PingForm
from .models import User
from flask_login import login_user,login_required,logout_user


def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-API-KEY') and request.headers.get('X-API-KEY') == app.config["KEY"]:
            return view_function(*args, **kwargs)
        else:
            result = {"success":False,"msg":"missing X-API-KEY or KEY is Wrong"}
            return jsonify(result),401
    return decorated_function


@app.route('/base',methods=['GET'])
def base():
    return render_template('base.html')


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(user_name=data["username"]).first()
        if user is not None and user.user_passwd==data["password"]:
            login_user(user,data["remember_me"])
            session["user"] = data["username"]
            return redirect(request.args.get("next") or url_for("index"))
        flash("Invalid username or password !")
        return redirect(url_for("login"))

    return render_template('login.html',form=form)


@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/api/ping', methods=['GET'])
# @require_appkey
def ping():
    results = data_query("args_ping")
    return jsonify(results)


@app.route('/api/curl', methods=['GET'])
# @require_appkey
def curl():
    results = data_query("args_curl")
    return jsonify(results)


@app.route('/index',methods=['GET','POST'])
@login_required
def index():
    return render_template('index.html')


@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/tables',methods=['GET','POST'])
@login_required
def tables():
    return render_template('tables.html')


@app.route('/charts',methods=['GET','POST'])
@login_required
def charts():
    return render_template('charts.html')


@app.route('/forms',methods=['GET','POST'])
@login_required
def forms():
    form_curl = CurlForm()
    if form_curl.submit_curl.data and form_curl.validate_on_submit():
        args_id=int(form_curl.args_id.data)
        args_ipversion=int(form_curl.args_ipversion.data)
        args_url=form_curl.args_url.data
        args_timeout=int(form_curl.args_timeout.data)
        insert_tables("args_curl",args_id,args_ipversion,args_url,args_timeout)
        flash("Insert succeed!")
        return redirect(url_for("forms"))
    form_ping = PingForm()
    if form_ping.submit_ping.data and form_ping.validate_on_submit():
        print("hello")
        args_id = int(form_ping.args_id.data)
        args_ipversion = int(form_ping.args_ipversion.data)
        args_url = form_ping.args_url.data
        args_packagesize = int(form_ping.args_packagesize.data)
        args_count = int(form_ping.args_count.data)
        args_timeout = int(form_ping.args_timeout.data)
        insert_tables("args_ping", args_id, args_ipversion, args_url,args_packagesize,args_count, args_timeout)
        flash("Insert succeed!")
        return redirect(url_for("forms"))
    return render_template('forms.html',form_ping=form_ping,form_curl=form_curl)





