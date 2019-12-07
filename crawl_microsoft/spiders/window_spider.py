# -*- coding: utf-8 -*-
import scrapy
import requests
from selenium import webdriver

class WindowSpiderSpider(scrapy.Spider):
    name = 'window_spider'
    allowed_domains = ['www.catalog.update.microsoft.com']
    start_urls = ['https://www.catalog.update.microsoft.com/Search.aspx?q=windows']

    def __init__(self):
        self.driver = webdriver.Chrome("/Users/cuongvu/Desktop/project/crawl_microsoft/chromedriver")

    def parse(self, response):
        self.driver.get(response.url)
        while True:
            next = self.driver.find_element_by_xpath('//*[@id="ctl00_catalogBody_nextPageLink"]/a')
            try:
                data = response.xpath('//*[@class="resultsBorder resultsBackGround"]//tr')
                for d in data:
                    headers = {
                        'content-type': 'application/json',
                        'Authorization': 'Bearer ' + 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzU2OTIwMjEsImlkIjp7IlVzZXJuYW1lIjoiYWRtaW4iLCJQYXNzd29yZCI6IjEyMzQ1NiJ9LCJvcmlnX2lhdCI6MTU3NTY4ODQyMX0.LghbjOeemGTmzCt3h9BbxdCY5z-jyo4hMV5l4ID2Hdw'
                    }
                    test = d.xpath('td')
                    title = test[1].xpath('a/text()').extract_first()
                    title = str(title).replace("\r\n","").strip()

                    product = test[2].xpath('text()').extract_first()
                    product = product.strip()

                    size = test[6].xpath('span/text()').extract_first()
                    url = test[7].xpath('input/@id').extract_first()

                    classification = test[3].xpath('text()').extract_first()
                    classification = str(classification).replace("\r\n","").strip()

                    last_updated = test[4].xpath('text()').extract_first()
                    last_updated = str(last_updated).replace("\r\n","").strip()

                    version = test[5].xpath('text()').extract_first()
                    version = str(version).replace("\r\n","").strip()

                    real_url = "https://www.catalog.update.microsoft.com/ScopedViewInline.aspx?updateid=" + str(url)
                    params = {
                        'title': title,
                        'product': product,
                        'size': size,
                        'url': real_url,
                        'classification': classification,
                        'last_updated': last_updated,
                        'version': version
                    }
                    requests.post("http://127.0.0.1:8099/custom/updates", json=params, headers=headers)
                    print(params)

                    next.click()
            except:
                break

        self.driver.close()