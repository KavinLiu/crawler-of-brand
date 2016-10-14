# coding=utf-8

import PackageTool
from brand.GsSrcCousumer import GsSrcCousumer
from BrandSearcher import BrandSearcher


class BrandUpdateJob(GsSrcCousumer):

    def __init__(self):
        super(BrandUpdateJob, self).__init__()

    def set_config(self):
        self.searcher = BrandSearcher()

if __name__ == '__main__':
    job = BrandUpdateJob()
    job.run()
