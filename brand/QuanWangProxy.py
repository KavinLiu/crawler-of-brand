# coding=utf-8

import socket
import requests
import time
from codecs import open
import logger

host = '172.16.0.26'
port = 12345
order_list = ['2f28510b6108968e731f1b1036d47903', '620263bcd5bc55c1c00e080901bb455c',
              '2525d0e5635b43c32a674031210caf24', '420a98c49b8dda4b9a081ac350f0fd57',
              '2dff9864d163bbe959224da73862624d', 'a01561721fd7d56fb945b4e6e2625b7c',
              '57e0f252b5965a1fd2d6fa1c68fed655', '65b5bb9dbbda999cd7a155290ac4af99']
sub_order_list = ['%s,%d' % (o, i) for o in order_list for i in range(5)]
sub_order_ts_dict = dict.fromkeys(sub_order_list, -1)
# sub_order_cnt_dict = dict.fromkeys(sub_order_list, 0)


def start_server():
    """
    启动代理分发服务
    :return:
    """
    global host, port
    s = socket.socket()
    s.bind((host, port))
    s.listen(10)
    while True:
        c, addr = s.accept()
        order = get_proxy_order()
        logger.write(str(addr)+", order: " + order)
        try:
            c.send(order)
            c.close()
        except socket.error:
            del c, addr
            pass


def get_proxy_order():
    """
    通过接口从全网代理获取代理
    :return:
    """
    global sub_order_ts_dict
    sub_order = None
    min_ts = long(time.time()*1000)
    for so in sub_order_ts_dict:
        ts = sub_order_ts_dict[so]
        if ts <= min_ts:
            min_ts = ts
            sub_order = so
    # print 'sub_order -> %s' % sub_order
    logger.write(sub_order)
    if long(time.time()*1000) - min_ts < 1000:
        logger.write(u'休眠1秒...')
        time.sleep(1)
    sub_order_ts_dict[sub_order] = long(time.time()*1000)
    order = sub_order.split(',')[0]
    return order


def get_proxy():
    """
    通过代理分发服务获取代理
    :return:
    """
    global host, port
    s = socket.socket()
    s.connect((host, port))
    order = s.recv(1024)
    print 'order -》' + order
    url = "http://dynamic.goubanjia.com/dynamic/get/" + order + ".html?ttl"
    r = requests.get(url)
    proxy_info = r.text.split(',')
    return proxy_info[0]


if __name__ == '__main__':
    start_server()
    # for i in range(1000):
    #     print i, get_proxy()
