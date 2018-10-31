# Revisor
#!/usr/bin/env python
# -*-coding: utf-8 -*-
# vim: sw=4 ts=4 expandtab ai

from flask import Flask, request, Response
import json
import time

PATH = "/home/sveta/программирование/cnf.txt"

APP = Flask(__name__)

@APP.route('/get_cnf')
def get_cnf():
    slo = json.load(open(PATH, "r"))
    return Response(json.dumps(slo), mimetype='application/json')

@APP.route('/check', methods=['GET'])
def check():
    retn = []
    if request.method == 'GET':
        try:
            user_cnfig = request.args.get("users")
            user_cnf = user_cnfig.split(",")
        except Exception as err:
            print "ERROR %s" % str(err)
            return 500
        slo = json.load(open(PATH, "r"))
        if not slo["data"] == int(time.time()/(3600*24)):
            for key in slo:
                slo["users"][key][1] = 0
            slo["data"] = int(time.time()/(3600*24))
        for i in user_cnf:
            slo["users"][i][1] = slo["users"][i][1]+1
            if slo["users"][i][1] >= slo["users"][i][0]:
                retn.append(i)
        json.dump(slo, open(PATH, "w"))
        return Response(json.dumps(retn), mimetype='application/json')
    else:
        return 406

@APP.route('/set_cnf', methods=['GET'])
def set_cnf():
    slo = json.load(open(PATH, "r"))
    try:
        user = str(request.args.get("user"))
        val = request.args.get("value")
    except Exception as err:
        print "ERROR %s" % str(err)
        return 500
    slo["users"][user] = int(val)
    json.dump(slo, open(PATH, "w"))
    return Response(json.dumps(slo), mimetype='application/json')

if __name__ == '__main__':
    APP.run(host='0.0.0.0', debug=True)

