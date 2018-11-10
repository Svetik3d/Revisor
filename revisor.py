# Revisor
#!/usr/bin/env python
# -*-coding: utf-8 -*-
# vim: sw=4 ts=4 expandtab ai

import requests
import argparse
import getpass

PATH = "/home/sveta/программирование/cnf.txt"
IP = "127.0.0.1:5000"

def first():
    rget = requests.get("http://%s/get_cnf" % (IP))
    slo = rget.json()
    for key in slo["users"]:
        print "%s - осталось %s мин, всего %s мин" % \
                (str(key), str(slo["users"][key][1]),
                 str(slo["users"][key][0]))

def second(username, val):
    requests.get("http://%s/set_cnf?user=%s&value=%s&nomer=0&password=%s" % \
                 (IP, username, val, password()))
    print("%s установленно по %sмин в день" % (str(username), str(val)))

def third(username, val):
    requests.get("http://%s/set_cnf?user=%s&value=%s&nomer=1&password=%s" % \
                 (IP, username, val, password()))
    print("%s установленно по %sмин на сегодня" % (str(username), str(val)))

def password():
    pas = getpass.getpass()
    return hash(pas)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", dest="return_all", action='store_true')
    parser.add_argument("-u", dest="us_name", default="")
    parser.add_argument("-p", dest="forever", default=0)
    parser.add_argument("-t", dest="temporarily", default=0)
    args = parser.parse_args()
    if args.return_all == True:
        first()
    if args.forever != 0:
        second(args.us_name, args.forever)
    if args.temporarily != 0:
        third(args.us_name, args.temporarily)

if __name__ == '__main__':
    main()
