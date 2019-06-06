# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import csv

class ChengxiangPipeline(object):

    def __init__(self):

        a = ['省份','城市','城市代码','区域','区域代码','城镇','城镇代码','街道(村庄)代码','街道(村庄)代号','街道(村庄)']
        f = open('城乡划分代码.csv','a',newline='',encoding='utf-8')
        self.w = csv.writer(f)
        self.w.writerow(a)


    def process_item(self, item, spider):
        try:
            self.w.writerow([item['provincetr_name'],item['city_name'],item['city_code'],item['countytr_name'],
                item['countytr_code'],item['towntr_name'],item['towntr_code'],item['villagetr_code'],
                item['classification'],item['villagetr_name']])
        except:
            print('--'*20)
        return item


    def close_spider(self,spider):
        self.w.close()