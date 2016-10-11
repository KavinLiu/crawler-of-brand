# coding=utf-8

import requests
import urllib
from lxml import html
from brand.Searcher import Searcher
from brand.KafkaAPI import KafkaAPI
import json
import base64
import sys
from requests.exceptions import ReadTimeout
from brand.ProxyConf import ProxyConf, key1 as app_key


class BrandSearcher(Searcher):

    def __init__(self):
        self.proxy_config = ProxyConf(app_key)
        self.json_result = None
        self.set_config()

    def set_config(self):
        """设置kafka接口"""
        self.group = 'Crawler'  # 正式
        # self.group = 'CrawlerTest'  # 测试
        # self.kafka = KafkaAPI("GSCrawlerTest")  # 测试
        if get_args().get("topic", ""):
            self.kafka = KafkaAPI(get_args()['topic'])  # 存储结果的topic
        else:
            self.kafka = KafkaAPI("GSCrawlerResult")
        self.topic = 'BrandCrawler'  # 批量更新时的数据源topic
        self.kafka.init_producer()

    def submit_search_request(self, name, account_id='null', task_id='null'):
        print u'Searching', name
        self.json_result = dict()
        self.json_result["inputCompanyName"] = name
        self.json_result["account_id"] = account_id
        self.json_result["task_id"] = task_id
        self.json_result["brand_details"] = list()
        headers = {"Host": "so.quandashi.com",
                   "Referer": "http://www.quandashi.com/",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0"}
        cookies = dict(YZNAME='e42c0141250d02dad20c86609d5d19d155f12717')
        key_url = urllib.quote(name.encode('utf-8'))
        # print key_url
        i = 0
        for page in range(1, 10000):
            url = "http://so.quandashi.com/index/search?nonce=833330&param=3&styles=&key=" + key_url + "&per-page=10&page=" + str(page)
            r = self.get_request(url, headers, cookies)
            r.encoding = 'utf-8'
            tree = html.fromstring(r.text)
            result_list = tree.xpath(".//div[4]//li[@class='item']")
            if len(result_list) == 0 and page == 1:
                print u'No brand result'
                break
            for result in result_list:
                i += 1
                values = dict()
                values["ent_name"] = name  # 公司名
                values["reg_no"] = result.xpath(".//div[1]/span[@class='s3']/a")[0].text.split(u"：")[1]  # 注册号
                values["cat_no"] = result.xpath(".//div[1]/span[@class='s2']/a")[0].text.split(u"：")[1]  # 类号
                values["brand_name"] = result.xpath(".//div[1]/span[@class='s1']/a/em")[0].text  # 商标名
                img_url1 = values["reg_no"].rjust(12, "0")  # 将注册号格式化成12位字符串
                img_url = "http://tm-jpg.oss-cn-beijing.aliyuncs.com/jpg/"+img_url1[0:3]+"/"+img_url1[3:6]+"/"+img_url1[6:9]+"/"+img_url1[9:12]+"/logo_middle.jpg"
                r = requests.get(img_url)
                img_str = base64.b64encode(r.content)  # 图片的base64格式字符串
                values['img_str'] = img_str
                values['apply_time'] = result.xpath(".//div[1]/span[@class='s5']/a")[0].text.split(u"：")[1]  # 申请日期
                values['brand_status'] = result.xpath(".//div[2]/span[@class='s1']/a")[0].text.split(u"：")[1]  # 当前状态
                values['id'] = i
                values['rowkey'] = name + "_" + values['apply_time'].replace("-", '') + "_" + values["reg_no"]
                self.json_result["brand_details"].append(values)

            if len(result_list) != 10:
                print u'Search succeed'
                break
        print u'Result to kafka'
        self.kafka.send(json.dumps(self.json_result, ensure_ascii=False))
        # print json.dumps(self.json_result, ensure_ascii=False)

    def get_request(self, url, headers, cookies, t=0):
        try:
            headers['Proxy-Authorization'] = self.proxy_config.get_auth_header(lock_id=self.lock_id)
            r = requests.get(url, headers=headers, cookies=cookies, proxies=self.proxy_config.get_proxy(), timeout=15)
            return r
        except ReadTimeout as e:
            if t == 10:
                raise e
            else:
                return self.get_request(url, headers, cookies, t+1)


def get_args():
    args = dict()
    for arg in sys.argv:
        kv = arg.split('=')
        if len(kv) == 2:
            k = kv[0]
            if k != 'topic':
                v = kv[1].decode('gbk', 'ignore')
            else:
                v = kv[1]
            args[k] = v
    return args

if __name__ == '__main__':
    args_dict = get_args()
    searcher = BrandSearcher()
    # searcher.submit_search_request(u'河南正浩测绘有限公司')
    searcher.submit_search_request(args_dict["companyName"], account_id=args_dict['accountId'], task_id=args_dict['taskId'])
