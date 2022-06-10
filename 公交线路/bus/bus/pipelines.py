# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exporters import CsvItemExporter
import pymysql
from pymysql import cursors
from twisted.enterprise import adbapi


#同步存储到Mysql
class BusPipelineMysql:
    def __init__(self):
        self.conn = pymysql.Connect(
            host='localhost',port=3306,user='root',password='123456'
            ,database='bus',charset='utf8'
        )
        self.cursor = self.conn.cursor()
        self._sql = None
    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into beijing_bus(city_name,line_name,run_time,ticket_price,
                company,update_time,line_sites) values (%s,%s,%s,%s,%s,%s,%s);
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item['city_name'],item['line_name'],item['run_time'],
                        item['ticket_price'], item['company'],item['last_update_time'],item['line_sites']))
        self.conn.commit()
        print(item)
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()

#异步存储到Mysql
class BusPipelineTwisted:
    def __init__(self):
        params = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'bus',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **params)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                            insert into beijing_bus(city_name,line_name,run_time,ticket_price,
                            company,update_time,line_sites) values (%s,%s,%s,%s,%s,%s,%s);
                        """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        derfer = self.dbpool.runInteraction(self.insert_item, item)
        derfer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item['city_name'],item['line_name'],item['run_time'],
                        item['ticket_price'], item['company'],item['last_update_time'],item['line_sites']))

    def handle_error(self, error, item, spider):
        print('=' * 10 + 'error' + '=' * 10)
        print(error)
        print('=' * 10 + 'error' + '=' * 10)

#存入csv文件
class BusPipelineCsv:
    def __init__(self):
        self.fp = open('beijing_bus_line.csv','wb')
        head = ['city_name','line_name','run_time','ticket_price',
                'company','last_update_time','line_sites']
        self.exporter = CsvItemExporter(self.fp,fields_to_export=head)
        self.exporter.start_exporting()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        print(item)
        return item
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.fp.close()
