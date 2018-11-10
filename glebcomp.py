# Revisor
#!/usr/bin/env python
# -*-coding: utf-8 -*-
# vim: sw=4 ts=4 expandtab ai

from flask import Flask, request, Response
import json
import time
import datetime

PATH = "/home/sveta/программирование/cnf.txt"
PASSWORD = "123"
APP = Flask(__name__)

def log(msg):
    log_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print "%s: %s" % (log_dt, str(msg))

@APP.route('/get_cnf')
def get_cnf():
    log("Пришел запрос get")
    slo = json.load(open(PATH, "r"))
    return Response(json.dumps(slo), mimetype='application/json')

@APP.route('/check', methods=['GET'])
def check():
    retn = []
    if request.method == 'GET':
        log("Пришел запрос check")
        try:
            user_cnfig = request.args.get("users")
            user_cnf = user_cnfig.split(",")
        except Exception as err:
            log("ERROR %s" % str(err))
            return 500
        log("check с параметрами %s" % user_cnf)

        try:
            slo = json.load(open(PATH, "r"))
        except Exception as err:
            log("ERROR %s" % str(err))
        log("Прочитали конфиг %s" % slo)

        if not slo["data"] == int(time.time()/(3600*24)):
            for key in slo["users"]:
                slo["users"][key][1] = slo["users"][key][0]
            slo["data"] = int(time.time()/(3600*24))
            log("Изменяем парамаетры всвязи с изменением даты с %s нв %s" %
                (slo["data"], str(int(time.time()/(3600*24)))))

        for i in user_cnf:
            slo["users"][i][1] = slo["users"][i][1] - 1
            log("Поьзователю %s добавили минуту" % i)
            if slo["users"][i][1] <= 0:
                retn.append(i)
                log("У %s кончилось время" % i)
        json.dump(slo, open(PATH, "w"))
        log("Записали новый конфиг")
        return Response(json.dumps(retn), mimetype='application/json')
    else:
        return 406

@APP.route('/set_cnf', methods=['GET'])
def set_cnf():
    log("Пришел запрос set")
    slo = json.load(open(PATH, "r"))
    try:
        user = str(request.args.get("user"))
        val = int(request.args.get("value"))
        nom = int(request.args.get("nomer"))
        pas = int(request.args.get("password"))
    except Exception as err:
        log("ERROR %s" % str(err))
        return 500
    if hash(PASSWORD) == pas:
        slo["users"][user][nom] = int(val)
        log("Пользователю %s установленно время %s" % (user, val))
        json.dump(slo, open(PATH, "w"))
        return Response(json.dumps(slo), mimetype='application/json')
    else:
        log("Неверный пароль")
        return 403

if __name__ == '__main__':
    APP.run(host='0.0.0.0', debug=True)
