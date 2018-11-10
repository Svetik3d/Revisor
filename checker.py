# Revisor
#!/usr/bin/env python
# -*-coding: utf-8 -*-
# vim: sw=4 ts=4 expandtab ai

import requests
import subprocess
import datetime

IP = "127.0.0.1:5000"

def log(msg):
    log_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print "%s: %s" % (log_dt, str(msg))

def main():
    slo = {}
    popen = subprocess.Popen("/usr/bin/who -u | /bin/grep -v 'pts/' | /usr/bin/awk '{print $1,$6}'", shell=True, stdout=subprocess.PIPE)
    stdout, _ = popen.communicate()
    stdout = stdout.split("\n")
    for i in stdout:
        part = i.split(" ")
        if part == [""]:
            break
        slo[part[0]] = part[1]
    payload = ",".join(slo.keys())
    try:
        rget = requests.get("http://%s/check?users=%s" % (IP, payload))
        users = rget.json()
    except Exception as err:
        users = slo.keys()
        log("Error get from server: %s" % str(err))
    for i in slo.keys():
        if i in users:
            #subprocess.call("kill %s" % (str(slo[i])), shell=True)
            log("kill %s" % (str(slo[i])))

if __name__ == '__main__':
    main()
