# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsofzjproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    new_title = scrapy.Field()
    new_time = scrapy.Field()

class DetailItem(scrapy.Item):
    news_title = scrapy.Field()
    news_content = scrapy.Field()