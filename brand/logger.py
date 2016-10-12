# coding=utf-8

from codecs import open
import datetime
import time

dt = None
log_file = None


def write(msg):
    global log_file, dt
    if str(datetime.date.today()) != dt:
        dt = str(datetime.date.today())
        if log_file:
            log_file.close()
        log_file = open('../logs/%s.log' % dt, 'a', 'utf-8')
    print time.strftime('%Y-%m-%d %X', time.localtime()) + ' -> ' + msg
    log_file.write(time.strftime('%Y-%m-%d %X', time.localtime()) + ' -> ' + msg + '\n')


