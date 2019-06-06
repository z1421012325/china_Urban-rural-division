# -*- coding: utf-8 -*-
import scrapy


class CxSpider(scrapy.Spider):
    name = 'cx'
    allowed_domains = ['stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html']

    def parse(self, response):
        trs = response.xpath('//tr[@class="provincetr"]/td')
        for tr in trs:
            provincetr_name = tr.xpath('.//a/text()').get()
            provincetr_link = response.urljoin(tr.xpath('./a/@href').get())

            yield scrapy.Request(url=provincetr_link,
                                 callback=self.city,
                                 meta={'item':provincetr_name})


    def city(self,response):
        provincetr_name = response.meta.get('item')

        trs = response.xpath('//table[@class="citytable"]//tr[@class="citytr"]')
        for tr in trs:
            city_name = tr.xpath('.//td[2]/a/text()').get()
            city_code = tr.xpath('.//td[1]/a/text()').get()
            city_link = response.urljoin(tr.xpath('.//td[1]/a/@href').get())

            yield scrapy.Request(url=city_link,
                                 callback=self.countytr,
                                 meta={'item':(provincetr_name,
                                               city_name,
                                               city_code)})


    def countytr(self,response):
        provincetr_name,city_name,city_code = response.meta.get('item')

        trs = response.xpath('//table[@class="countytable"]//tr[@class="countytr"]')[1:]
        for tr in trs:
            countytr_code = tr.xpath('.//td[1]/a/text()').get()
            countytr_name = tr.xpath('.//td[2]/a/text()').get()

            countytr_url  = response.urljoin(tr.xpath('.//td[2]/a/@href').get())

            yield scrapy.Request(url=countytr_url,
                                 callback=self.towntr,
                                 meta={'item':(provincetr_name,city_name,city_code,
                                                           countytr_name,countytr_code)})


    def towntr(self,response):
        provincetr_name, city_name, city_code,countytr_name, countytr_code = response.meta.get('item')

        trs = response.xpath('//tr[@class="towntr"]')
        for tr in trs:
            towntr_code = tr.xpath('.//td[1]/a/text()').get()
            towntr_name = tr.xpath('.//td[2]/a/text()').get()
            towntr_link = response.urljoin(tr.xpath('.//td[2]/a/@href').get())

            yield scrapy.Request(url=towntr_link,
                                 callback=self.villagetr,
                                 meta={'item': (provincetr_name, city_name, city_code,
                                                                 countytr_name, countytr_code,
                                                                 towntr_name,towntr_code)})

    def villagetr(self,response):
        provincetr_name, \
        city_name, city_code, \
        countytr_name, countytr_code,\
        towntr_name,towntr_code = response.meta.get('item')

        item = {}

        trs = response.xpath('//tr[@class="villagetr"]')
        for tr in trs:
            villagetr_code = tr.xpath('.//td[1]/text()').get()
            classification = tr.xpath('.//td[2]/text()').get()
            villagetr_name = tr.xpath('.//td[3]/text()').get()

            item['provincetr_name'] = provincetr_name
            item['city_name'] = city_name
            item['city_code'] = city_code
            item['countytr_name'] = countytr_name
            item['countytr_code'] = countytr_code
            item['towntr_name'] = towntr_name
            item['towntr_code'] = towntr_code
            item['villagetr_code'] = villagetr_code
            item['classification'] = classification
            item['villagetr_name'] = villagetr_name

            yield item

