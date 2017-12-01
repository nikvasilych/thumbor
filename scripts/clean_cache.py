# -*- coding: utf-8 -*-
from collections import defaultdict
import os, re, sys, time


def parseperiod(s):
    RE = r'(\d+Y)?(\d+M)?(\d+W)?(\d+D)?(\d+h)?(\d+m)?(\d+s)?'
    match = re.match(RE, s)
    d = defaultdict(lambda: 0, {_[-1]: int(_[:-1]) for _ in match.groups() if _})
    d['D'] += 7*d['W']
    return [d[_] for _ in 'YMDhms']


def process(path, period):
    now = time.time()
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            curpath = os.path.join(dirpath, file)
            expiration = time.localtime(os.stat(curpath).st_mtime)
            expiration = [period[_]+expiration[_] for _ in range(6)] + [0]*3
            expiration = time.mktime(expiration)
            if expiration < now:
                if os.path.isfile(curpath):
                    os.remove(curpath)
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        for dirname in dirnames:
            curpath = os.path.join(dirpath, dirname)
            files = os.listdir(curpath)
            if not files:
                os.rmdir(curpath)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Pass a path and a period as arguments, period like 1Y4M3W18D5h32m48s, which means 1 year, 4 months, 3 weeks, 18 days, 5 hours, 32 minutes and 48 seconds. In period, any field could be omitted."
        exit(1)
    process(sys.argv[1], parseperiod(sys.argv[2]))
