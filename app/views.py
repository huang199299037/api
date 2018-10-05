from flask import request, jsonify,render_template,redirect,flash,url_for,session
from functools import wraps
from app import app
from .forms import  LoginForm,CurlForm,PingForm
from .models import User,args_ping,args_curl,Map
from flask_login import login_user,login_required,logout_user
from . import db
from .of import get_endpoint_id,get_endpoint


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
    a_p=args_ping.query.all()
    result = []
    for tmp in a_p:
        result.append(tmp.to_json())
    return jsonify(result), 200


@app.route('/api/curl', methods=['GET'])
# @require_appkey
def curl():
    a_c=args_curl.query.all()
    result = []
    for tmp in a_c:
        result.append(tmp.to_json())
    return jsonify(result), 200


@app.route('/index',methods=['GET','POST'])
@login_required
def index():
    return render_template('index.html')


@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    group = {
        "endpoint_num": get_endpoint.get_endpoint_number(),
        "liveendpoint_num": get_endpoint.get_live_endpoint_number(),
        "pinglist_num": get_endpoint.get_pinglist_number(),
        "curllist_num": get_endpoint.get_curllist_number()
    }
    res_list = get_endpoint_id.func2()

    return render_template('dashboard.html', res_list=res_list, **group)


@app.route('/tables',methods=['GET','POST'])
@login_required
def tables():
    return render_template('tables.html')


@app.route('/charts',methods=['GET','POST'])
@login_required
def charts():
    return render_template('charts.html')


@app.route("/ping",methods=['GET','POST'])
@login_required
def ping_table():
    page = int(request.args.get('page', 1, type=int))
    per_page = int(request.args.get('per_page', 5))
    pagination = args_ping.query.order_by('args_id').paginate(page, per_page, error_out=False)
    ap = pagination.items

    return render_template('ping.html', pagination=pagination, ap=ap)


@app.route("/curl",methods=['GET','POST'])
@login_required
def curl_table():
    page = int(request.args.get('page', 1,type=int))
    per_page = int(request.args.get('per_page', 5))
    pagination = args_curl.query.order_by('args_id').paginate(page, per_page, error_out=False)
    ac=pagination.items

    return render_template('curl.html',pagination=pagination, ac=ac)


@app.route("/curl_add",methods=['GET','POST'])
@login_required
def curl_add():
    form_curl = CurlForm()
    a_c=args_curl()
    if form_curl.submit_curl.data and form_curl.validate_on_submit():
        a_c.args_id=0
        a_c.args_ipversion = int(form_curl.args_ipversion.data)
        a_c.args_url = form_curl.args_url.data
        a_c.args_timeout = int(form_curl.args_timeout.data)
        db.session.add(a_c)
        db.session.commit()
        flash("Add Succeed!!")
        return redirect(url_for("curl_add"))
    return render_template('curl_add.html',form_curl=form_curl)


@app.route("/ping_add", methods=['GET', 'POST'])
@login_required
def ping_add():
    form_ping =PingForm()
    a_p=args_ping()
    if form_ping.submit_ping.data and form_ping.validate_on_submit():
        a_p.args_id=0
        a_p.args_ipversion = int(form_ping.args_ipversion.data)
        a_p.args_url = form_ping.args_url.data
        a_p.args_packagesize = int(form_ping.args_packagesize.data)
        a_p.args_count = int(form_ping.args_count.data)
        a_p.args_timeout = int(form_ping.args_timeout.data)
        db.session.add(a_p)
        db.session.commit()
        flash("Add Succeed!!")
        return redirect(url_for("ping_add"))
    return render_template('ping_add.html',form_ping=form_ping)


@app.route("/ping_delete/<int:id>", methods=['GET', 'POST'])
@login_required
def ping_delete(id=None):
    result=args_ping.query.filter_by(args_id=id).first()
    db.session.delete(result)
    db.session.commit()
    flash("Delete Succeed!!")
    return  redirect(url_for('ping_table'))


@app.route("/curl_delete/<int:id>", methods=['GET', 'POST'])
@login_required
def curl_delete(id=None):
    result = args_curl.query.filter_by(args_id=id).first()
    db.session.delete(result)
    db.session.commit()
    flash("Delete Succeed!!")
    return redirect(url_for('curl_table'))


@app.route("/ping_update/<int:id>", methods=['GET', 'POST'])
@login_required
def ping_update(id=None):
    form=PingForm()
    result = args_ping.query.filter_by(args_id=id).first()
    if form.submit_ping.data and form.validate_on_submit():
        result.args_ipversion=form.args_ipversion.data
        result.args_url = form.args_url.data
        result.args_packagesize = form.args_packagesize.data
        result.args_count=form.args_count.data
        result.args_timeout=form.args_timeout.data
        db.session.add(result)
        db.session.commit()
        flash("Update Succeed!!")
        return redirect(url_for('ping_table'))
    return render_template('ping_update.html',form=form,result=result)


@app.route("/curl_update/<int:id>", methods=['GET', 'POST'])
@login_required
def curl_update(id=None):
    form=CurlForm()
    result = args_curl.query.filter_by(args_id=id).first()
    if form.submit_curl.data and form.validate_on_submit():
        result.args_ipversion=form.args_ipversion.data
        result.args_url=form.args_url.data
        result.args_timeout=form.args_timeout.data
        db.session.add(result)
        db.session.commit()
        flash("Update Succeed!!")
        return redirect(url_for('curl_table'))
    return render_template('curl_update.html',form=form,result=result)


@app.route("/ping_search", methods=['GET', 'POST'])
@login_required
def ping_search():
    key=request.args.get("key","")
    page = int(request.args.get('page', 1, type=int))
    per_page = int(request.args.get('per_page', 5))
    pagination = args_ping.query.filter(
        args_ping.args_url.ilike("%"+key+"%")
        ).paginate(page, per_page, error_out=False)
    return render_template("ping_search.html",pagination=pagination)


@app.route("/curl_search", methods=['GET', 'POST'])
@login_required
def curl_search():
    key=request.args.get("key","")
    page = int(request.args.get('page', 1, type=int))
    per_page = int(request.args.get('per_page', 5))
    pagination = args_curl.query.filter(
        args_curl.args_url.ilike("%"+key+"%")
        ).paginate(page, per_page, error_out=False)
    return render_template("curl_search.html",pagination=pagination)


@app.route('/forms',methods=['GET','POST'])
@login_required
def forms():
    return render_template('forms.html')


@app.route('/api/push/<endpoint_name>/<endpoint_id>/')
def endpoint_name_id(endpoint_name, endpoint_id):
    '''

    :param endpoint_name:
    :param endpoint_id:
    :return:
    '''
    map = Map.query.filter_by(map_ofid=endpoint_id).first()
    if map is not None:
        return "ERROR : the endpoint is already in database !"
    else:
        map = Map(map_ofid=endpoint_id, map_ofname=endpoint_name)
        db.session.add(map)
        db.session.commit()
        return "success !!!"


@app.route('/mapconfig/')
def mapconfig():
    maplist = Map.query.filter_by().all()

    # print(type(maplist))
    # print(maplist)
    # print(type(maplist[0]))
    # print(maplist[0].map_id)
    return render_template('map_config.html', maplists=maplist)


@app.route('/mapdetail/<mapid>/', methods=['GET', 'POST'])
def mapdetail(mapid):
    if request.method == 'GET':
        # print(mapid)
        map = Map.query.filter_by(map_id=mapid).first()
        # print(map[0])
        return render_template('mapdetail.html', map=map)
    else:
        desc = request.form.get('map_desc')
        print(desc)
        if desc == '':
            return redirect(url_for('mapconfig'))
        else:
            map = Map.query.filter_by(map_id=mapid).first()
            map.map_desc = desc
            db.session.add(map)
            db.session.commit()
            return redirect(url_for('mapconfig'))











