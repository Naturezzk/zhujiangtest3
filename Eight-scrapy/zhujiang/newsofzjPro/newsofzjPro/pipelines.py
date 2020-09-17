# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class NewsofzjproPipeline(object):
    fp = None
    #重写父类的一个方法：该方法只在开始爬虫的时候被调用一次
    def open_spider(self,spider):
        print('开始爬虫......')
        self.fp = open('./newsofzj.txt','w',encoding='utf-8')

    def process_item(self, item, spider):
        #如何判定item的类型
        #将数据写入数据库时，如何保证数据的一致性
        if item.__class__.__name__ == 'DetailItem':
            news_title = item['news_title']
            news_content = item['news_content']
            print( news_title,news_content)
            self.fp.write(news_title + ':' + news_content + '\n')
        else:
            new_time = item['new_time']
            new_title = item['new_title']
            print(item['new_time'],item['new_title'])
            self.fp.write(new_title + ':' + new_time + '\n')
        return item

    def close_spider(self,spider):
        print('结束爬虫！')
        self.fp.close()

class mysqlPileLine(object):
    conn = None
    cursor = None
    def open_spider(self,spider):
        self.conn = pymysql.Connect(host='127.0.0.1',port=3306,user='root',password='1207081779',db='newszj',charset='utf8')
    def process_item(self,item,spider):
        self.cursor = self.conn.cursor()

        try:
            if item.__class__.__name__ == 'DetailItem':
                self.cursor.execute('insert into newszjcontent values("%s","%s")'%(item["news_title"],item["news_content"]))
            else:
                self.cursor.execute('insert into newszjtitle values("%s","%s")'%(item["new_title"],item["new_time"]))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()