# coding:utf-8
import pymongo
import sys
import tornado
import tornado.web
import tornado.gen
import logging
import time
from bson import ObjectId

# reload(sys)
# import importlib
# importlib.reload(sys)
# sys.setdefaultencoding('utf-8')
error_log = logging.getLogger('error')


# 模糊搜索
class BtSearchHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        page_index = 1
        bt_keywords = None
        try:
            bt_keywords = self.get_argument('bt_keywords')  # 搜索关键词
            page_index = self.get_argument('page_index', 1)  # 页码
        except Exception as e:
            error_log.error(e)

        if bt_keywords:

            try:
                from pywormsite import RedisDriver
                ip = self.request.remote_ip
                if not ip:
                    ip = '111.111.111.111'

                key = 'bt_search:{0}'.format(ip)
                master_13 = RedisDriver().master_13
                master_13.lpush(key, bt_keywords)
            except:
                pass

            mongo_url = 'mongodb://localhost:27017/'
            db = pymongo.MongoClient(mongo_url).bt

            mongo_find = db.bt_info.find({'$or': [{'name': {'$regex': bt_keywords, '$options': 'i'}},
                                                  {"files": {"$elemMatch": {"file_name": {'$regex': bt_keywords}}}}]})

            # 如果相关数据超过100条，只按100条算
            max_data = mongo_find.skip(10 * (int(page_index) + 9)).limit(1)

            print(page_index)
            print(max_data.count())
            if max_data.count():
                print(111111111111)
                bt_count = 10 * (int(page_index) + 9) - 1
            else:
                print(222222222222)
                bt_count = int(mongo_find.count())

            links = mongo_find.sort('create_at', pymongo.ASCENDING).skip(10 * (int(page_index) - 1)).limit(10)
            page_num = int(bt_count / 10) + 1  # 共有几页

            new_links = []
            for link in links:
                link_files = link.get('files')
                _files = link_files[:15]
                link['files'] = _files
                new_links.append(link)
            self.render('bt_list.html', links=new_links, page_index=int(page_index), page_num=int(page_num),
                        bt_keywords=bt_keywords, time=time)
        else:
            self.render('bt_list.html', links=None, page_index=int(page_index), page_num=0, bt_keywords=bt_keywords,
                        time=time)


# 精确搜索
class BtDetailSearchHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        mongo_url = 'mongodb://localhost:27017/'
        db = pymongo.MongoClient(mongo_url).bt

        bt_id = self.get_argument('bt_id')

        link = db.bt_info.find_one({"_id": ObjectId(bt_id)})

        self.render('bt_detail.html', link=link)
