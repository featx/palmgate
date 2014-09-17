# -*- coding: utf-8 -*-
__author__ = 'palmtale'

import unittest
from core import account as _account


class AccountMongoTest(unittest.TestCase):
    def setUp(self):
        import core
        from pymongo import MongoClient
        mongo_client = MongoClient()
        core.mongo_db = mongo_client.palms_test
        core.mongo_db.authenticate("test", "test")
        self.__storage = _account.AccountStorage()

    def tearDown(self):
        import core
        core.mongo_db.drop_collection('account')

    def test_create_retrieve(self):
        account = _account.Account()
        account.work_id = "20140918101"
        account.display_name = "月里年"
        account.cell_phone_number = "17601230009"
        account.first_name = "Cartoon"
        account.last_name = "张"
        account.age = 29
        account.gender = "男"
        account.position = "Java 软件工程师"
        account.title = "员工"
        account.email = "cartoon.zhang@dgd.com"
        account.civil_id = "019043243112321321"
        from time import time
        account.create_at = time()
        account.update_at = account.create_at
        self.__storage.create(account)
        account = _account.Account()
        account.work_id = "20140918101"
        account = self.__storage.retrieve(account)
        self.assertIsNotNone(account.id, "Wrong")

if __name__ == "__main__":
    unittest.main()