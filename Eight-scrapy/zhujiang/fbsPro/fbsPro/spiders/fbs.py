# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from newsofzjPro.items import NewsofzjproItem,DetailItem
from scrapy_redis.spiders import RedisCrawlSpider
class FbsSpider(RedisCrawlSpider):
    name = 'fbs'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['http://www.xxx.com/']
    redis_key = 'newszj'

    #链接提取器：根据指定规则（allow="正则"）进行指定链接的提取
    link = LinkExtractor(allow=r'index\d+\.html')
    link_detail = LinkExtractor(allow=r'zj/\d+/t\d+\.html')
    #http://www.chinawater.com.cn/newscenter/ly/zj/202009/t20200908_756018.html?
    #http://www.chinawater.com.cn/newscenter/ly/zj/202009/t20200916_756332.html
    rules = (
        #规则解析器：将链接提取器提取到的链接进行指定规则（callback）的解析操作
        Rule(link, callback='parse_item', follow=True),
        #follow=True：可以将链接提取器 继续作用到 连接提取器提取到的链接 所对应的页面中
        Rule(link_detail,callback='parse_detail')

    )

    #解析新闻时间和新闻的标题
    #如下两个解析方法中是不可以实现请求传参！
    #如法将两个解析方法解析的数据存储到同一个item中，可以以此存储到两个item
    def parse_item(self, response):
        #注意：xpath表达式中不可以出现tbody标签
        tr_list = response.xpath('/html/body/table/tr/td/div/div/div[1]/table/tr/td[2]/table/tr/td/table[3]/tr')
        for tr in tr_list:
            new_time = tr.xpath('./td[2]/font/text()').extract_first()
            new_title = tr.xpath('./td[1]/a/text()').extract_first()
            item = NewsofzjproItem()
            item['new_title'] = new_title
            item['new_time'] = new_time
            yield item

    #解析新闻内容和新闻编号
    def parse_detail(self,response):
        news_title = response.xpath('/html/body/table/tr/td/div/div/div[1]/table/tr/td[2]/table/tr/td/table/tr[3]/td/strong/text()').extract_first()
        #strong?
        news_content = response.xpath('/html/body/table/tbody/tr/td/div/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[1]/td/font/div//p//text()').extract()
        news_content = ''.join(news_content)

        # print(new_id,new_content)
        item = DetailItem()
        item['news_content'] = news_content
        item['news_title'] = news_title

        yield item