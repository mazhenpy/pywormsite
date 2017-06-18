# coding:utf-8
import pymongo
import tornado
import tornado.web
import tornado.gen
import logging

from bson import ObjectId

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
            mongo_url = 'mongodb://localhost:27017/'
            db = pymongo.MongoClient(mongo_url).bt
            links = db.bt_info.find({'$or': [{'name': {'$regex': bt_keywords}},
                                             {"files": {"$elemMatch": {"file_name": {'$regex': bt_keywords}}}}]}).sort(
                'create_at', pymongo.ASCENDING).skip(10 * (int(page_index) - 1)).limit(10)

            bt_count = int(db.bt_info.find({'$or': [{'name': {'$regex': bt_keywords}}, {
                "files": {"$elemMatch": {"file_name": {'$regex': bt_keywords}}}}]}).count())
            page_num = int(bt_count / 10) + 1  # 共有几页

            # links = [{u'files': [{u'file_name': u'\u901f\u5ea6\u4e0e\u6fc0\u60c57.\u4e2d\u82f1\u7279\u6548.mkv', u'file_size': u'3,165 MB'}],
            #           u'name': u'\u901f\u5ea6\u4e0e\u6fc0\u60c57.\u4e2d\u82f1\u7279\u6548.mkv', u'total_size': u'3,165 MB',
            #           u'create_at': 1493875745, u'magnet': u'magnet:?xt=urn:btih:1609351afd64c373834a6bd92c84577e5b362223',
            #           u'_id': ObjectId('590abc21f7f28234aa5b0c48')},
            #          {u'files': [{u'file_name': u'\u901f\u5ea6\u4e0e\u6fc0\u60c57.\u4e2d\u82f1\u7279\u6548.mkv',u'file_size': u'3,165 MB'}],
            #           u'name': u'\u901f\u5ea6\u4e0e\u6fc0\u60c57.\u4e2d\u82f1\u7279\u6548.mkv', u'total_size': u'3,165 MB',
            #           u'create_at': 1493875745, u'magnet': u'magnet:?xt=urn:btih:1609351afd64c373834a6bd92c84577e5b362223',
            #           u'_id': ObjectId('590abc21f7f28234aa5b0c48')},
            #          {u'files': [{u'file_name': u'\u901f\u5ea6\u4e0e\u6fc0\u60c57.\u4e2d\u82f1\u7279\u6548.mkv',
            #                       u'file_size': u'3,165 MB'}],
            #           u'name': u'\u901f\u5ea6\u4e0e\u6fc0\u60c57.\u4e2d\u82f1\u7279\u6548.mkv', u'total_size': u'3,165 MB',
            #           u'create_at': 1493875745, u'magnet': u'magnet:?xt=urn:btih:1609351afd64c373834a6bd92c84577e5b362223',
            #           u'_id': ObjectId('590abc21f7f28234aa5b0c48')},
            #          {u'files': [{u'file_name': u'\u901f\u5ea6\u4e0e\u6fc0\u60c57.\u4e2d\u82f1\u7279\u6548.mkv',
            #                       u'file_size': u'3,165 MB'}],
            #           u'name': u'\u901f\u5ea6\u4e0e\u6fc0\u60c57.\u4e2d\u82f1\u7279\u6548.mkv', u'total_size': u'3,165 MB',
            #           u'create_at': 1493875745, u'magnet': u'magnet:?xt=urn:btih:1609351afd64c373834a6bd92c84577e5b362223',
            #           u'_id': ObjectId('590abc21f7f28234aa5b0c48')}
            #          ]

            self.render('bt_list.html', links=links, page_index=int(page_index), page_num=int(page_num),
                        bt_keywords=bt_keywords)
        else:
            self.render('bt_list.html', links=None, page_index=int(page_index), page_num=0, bt_keywords=bt_keywords)


# 精确搜索
class BtDetailSearchHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        mongo_url = 'mongodb://localhost:27017/'
        db = pymongo.MongoClient(mongo_url).bt

        bt_id = self.get_argument('bt_id')

        link = db.bt_info.find({"_id": ObjectId(bt_id)})

        # link = {u'files': [{u'file_name': u'\u901f\u5ea6\u4e0e\u6fc0\u60c57.\u4e2d\u82f1\u7279\u6548.mkv',
        #                     u'file_size': u'3,165 MB'}],
        #         u'name': u'\u901f\u5ea6\u4e0e\u6fc0\u60c57.\u4e2d\u82f1\u7279\u6548.mkv', u'total_size': u'3,165 MB',
        #         u'create_at': 1493875745, u'magnet': u'magnet:?xt=urn:btih:1609351afd64c373834a6bd92c84577e5b362223',
        #         u'_id': ObjectId('590abc21f7f28234aa5b0c48')}

        self.render('bt_detail.html', link=link)
