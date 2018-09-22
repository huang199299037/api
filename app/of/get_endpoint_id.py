from .get_auth import get_Apitoken
import requests
import time
import json

name = "root"
password = "608"
api_addr = "http://202.120.83.82:8080/api/v1"
Apitoken = get_Apitoken(name, password, api_addr)


def get_name_id(flag):
    '''
    获取name和id
    [
    {
        "endpoint": "Master",
        "id": 178
    },

    {
        "endpoint": "ubuntu-pi-test",
        "id": 1
    },
    ]
    :return:
    '''

    print(Apitoken)

    h = {
        "Apitoken": Apitoken,
        "X-Forwarded-For": "202.120.83.82"
    }

    d = {
        "q": "."
    }

    r = requests.get("%s/graph/endpoint" % (api_addr,), params=d, headers=h)

    if r.status_code != 200:
        raise Exception("%s %s" % (r.status_code, r.text))

    namelist = []
    eidlist = []
    res = []

    res = json.loads(r.text)
    for re in res:
        namelist.append(re['endpoint'])
        eidlist.append(re['id'])

    # print(namelist)
    # print(eidlist)
    if(flag == 0):
        res = namelist
    else:
        res = eidlist

    return res


def get_endpoint_counter(eidlist, metriclist):
    '''
    查询eidlist里面的metriclist的所有 这个节点的参数，可以获得counter，endpointid

    [{"counter":"ping.average_time/ip-version=ipv4,target=www.114.com","endpoint_id":1,"step":60,"type":"GAUGE"},
    {"counter":"ping.average_time/ip-version=ipv4,target=www.126.com","endpoint_id":1,"step":60,"type":"GAUGE"},
    {"counter":"ping.average_time/ip-version=ipv4,target=www.163.com","endpoint_id":1,"step":60,"type":"GAUGE"},
    {"counter":"ping.average_time/ip-version=ipv4,target=www.baidu.com","endpoint_id":1,"step":60,"type":"GAUGE"},
    {"counter":"ping.average_time/ip-version=ipv4,target=www.huang.com","endpoint_id":1,"step":60,"type":"GAUGE"},
    {"counter":"ping.average_time/ip-version=ipv4,target=www.qq.com","endpoint_id":1,"step":60,"type":"GAUGE"},
    {"counter":"ping.average_time/ip-version=ipv6,target=www.126.com","endpoint_id":1,"step":60,"type":"GAUGE"},]
    '''
    print(Apitoken)
    d = {
        "eid": eidlist,
        "metricQuery": metriclist
    }
    h = {
        "Apitoken": Apitoken,
        "X-Forwarded-For": "202.120.83.82"
    }
    r = requests.get("%s/graph/endpoint_counter" % (api_addr,), params=d, headers=h)
    if r.status_code != 200:
        raise Exception("%s %s" % (r.status_code, r.text))

    return r.text


def func():
    '''
    根据counter和endpointid 获得具体参数
    :return:
    '''
    eidlist = get_name_id(1)
    eidlist = ','.join('%s' %eid for eid in eidlist)
    # print(eidlist)

    res = get_endpoint_counter(eidlist,"ping.average_time")

    res = json.loads(res)
    counterlist = []
    # idlist = []
    for re in res:
        counterlist.append(re['counter'])
        # idlist.append(re['id'])
        # print(re['counter'])


    # print(counterlist)
    # print(res)
    return counterlist

def func2():
    # print(Apitoken)
    h = {
        "Apitoken": Apitoken,
        "Content-type": "application/json;charset=utf-8",
        "X-Forwarded-For": "202.120.83.82"
    }
    namelist = get_name_id(0)
    counterlist = func()
    end_time = int(time.time())
    start_time = end_time - 60

    # print (namelist)

    data = {
         "step": 60,

         "start_time": start_time,

         "hostnames": namelist,

         "end_time": end_time,

         "counters": counterlist,

         "consol_fun": "AVERAGE"

        }

    r = requests.post("%s/graph/history" % (api_addr,), data=json.dumps(data), headers=h)
    if r.status_code != 200:
        raise Exception("%s %s" % (r.status_code, r.text))
    res = json.loads(r.text)
    res_list = []
    for re in res:
        if re['Values']:
            for r1 in re['Values']:
                if r1['value'] != None:
                    res_list.append(re)
                    print(re)


    print (res_list)
    return res_list