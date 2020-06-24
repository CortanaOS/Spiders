import pymongo
from pymongo.errors import DuplicateKeyError
from .settings import MONGO_HOST, MONGO_PORT


class BiLiBiLiPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        db = client['bili']
        self.User = db["user"]
        self.Focus = db["focus"]
        self.Relationship = db["relation"]

    def process_item(self, item, spider):
        if spider.name == 'user':
            self.insert_item(self.User, item)
        if spider.name == 'relationship':
            self.insert_item(self.Relationship, item)
        if spider.name == 'focus':
            self.insert_item(self.Focus, item)

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            pass

    # 用于更新对象列表存储格式数据
    # {user_id:1,focus_list:[]}
    def process_item_stop(self, item, spider):
        if spider.name == 'user':
            self.insert_item(self.User, item)
        elif spider.name == 'focus':
            key = {"user_id": item.get('user_id'), 'total': item.get('total')}
            add_state = {'$addToSet': {'focus_list': {"focus_id": item.get('focus_id'),
                                                      'focus_name': item.get('focus_name'),
                                                      'focus_face': item.get('focus_face'),
                                                      'introduction': item.get('introduction')
                                                      }}}
            self.update_info(key, add_state, self.Focus)
        return item

    @staticmethod
    def update_info(key, add_state, collection):
        """

        :param key: 此处表示 user_id
        :param add_state: {'$addToSet': {'list': {"focus": 5, 'name': '小明', 'age': 66}}}
        :param collection: 集合对象
        :return:
        """
        try:
            # 不存在时插入数据
            collection.update_one(key, add_state, upsert=True)
            print("更新成功")
        except Exception as e:
            print("更新失败:{}".format(e))
