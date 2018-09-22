
from .get_auth import get_Apitoken
import requests
import time
import json

name = "root"
password = "608"
api_addr = "http://202.120.83.82:8080/api/v1"
Apitoken = get_Apitoken(name, password, api_addr)

def get_endpoint():
    print(Apitoken)
    h = {
         "Apitoken": Apitoken ,
         "X-Forwarded-For":"202.120.83.82"
        }

    d = {
        "q":"."
        }

    r = requests.get("%s/graph/endpoint" %(api_addr,), params=d , headers=h)

    if r.status_code != 200:
        raise Exception("%s %s" %(r.status_code, r.text))


    return r.text

def get_endpoint_counter(eidlist,metriclist):
    print(Apitoken)
    d = {
        "eid": eidlist,
        "metricQuery": metriclist
    }
    h = {
        "Apitoken": Apitoken,
        "X-Forwarded-For": "202.120.83.82"
    }
    r = requests.get("%s/graph/endpoint_counter" %(api_addr,), params=d , headers=h)
    if r.status_code != 200:
        raise Exception("%s %s" %(r.status_code, r.text))

    return r.text

def get_endpoint_number():
    res = get_endpoint()
    return len(json.loads(res))

def get_live_endpoint_number():
    print(Apitoken)
    eidlist = []
    res = get_endpoint()
    res = json.loads(res)

    for re in res:
        eidlist.append(re['id'])

    eidlist = ",".join('%s' %id for id in eidlist)

    res = get_endpoint_counter(eidlist,"agent.alive")

    return len(json.loads(res))

def get_pinglist_number():

    r = requests.get("http://202.120.83.82:3456/api/ping")

    if r.status_code != 200:
        raise Exception("%s %s" %(r.status_code, r.text))

    return len(json.loads(r.text))

def get_curllist_number():

    r = requests.get("http://202.120.83.82:3456/api/curl")

    if r.status_code != 200:
        raise Exception("%s %s" %(r.status_code, r.text))

    return len(json.loads(r.text))