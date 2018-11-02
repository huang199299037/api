#-*-coding:utf-8-*-
from flask import Blueprint,request,render_template,redirect
from app.models import Map
from app.of import get_history,get_dashboardnum,get_curl_res

endpoint = Blueprint('endpoint',__name__)

@endpoint.route('/endpoint_detail/',methods=['GET','POST'])
def endpoint_detail():
    if request.method == 'GET':
        maplist = Map.query.filter_by().all()
        return render_template('endpoint_detail.html',endpointlist = maplist)
    else:
        print(request.form.get('endpoint_select'))
        print(request.getParameter('endpoint_select'))
        print(request.form.get('counter_select'))
        return render_template('endpoint_detail.html')

@endpoint.route('/counter/',methods=['POST','GET'])
def counter_list():
    # print(request.values)
    endpoint_id = request.form.get('endpoint_id')
    # print(endpoint_id)
    counterlist = get_dashboardnum.get_endpoint_counter(endpoint_id, '.')

    return counterlist

@endpoint.route('/counters/',methods=['POST','GET'])
def results_list():
    endpoint_id = request.form.get('endpoint_id')
    counter_name = request.form.get('counter_name')
    map = Map.query.filter_by(map_ofid = endpoint_id).first()
    endpoint_name = map.map_ofname
    # print(endpoint_name)
    # print(counter_name)
    res = get_history.get_counter_history(endpoint_name, counter_name)

    return res

@endpoint.route('/counter/detail/<endpoint_name>/<counter_name>',methods=['GET'])
def counter_detail(endpoint_name,counter_name):

    print(endpoint_name)
    print(counter_name)
    timelist ,valuelist = get_history.get_counter_history(endpoint_name,counter_name)
