# -*- coding: utf-8 -*-
__author__ = 'palmtale'
from pyramid.view import view_config
from core.access_token import TokenSurface


class SignSurface(TokenSurface):
    def __init__(self, request):
        super(SignSurface, self).__init__(request)
        self.__storage = SignStorage()

    @view_config(route_name='sign_in', renderer='json')
    def sign_in(self):
        return self.__sign("SignIn", "")

    @view_config(route_name="sign_out", renderer='json')
    def sign_out(self):
        return self.__sign("SignOut", "")

    def __sign(self, category, description):
        check = self._check_token()
        if not check.Pass:
            return check.object
        sign = Sign()
        sign.behavior = check.object
        sign.category = category
        sign.description = description
        self.__storage.create(sign)
        return {'result': {'msg': 'Success', 'time': str(sign.timestamp)}}

    @view_config(route_name="get_signs", renderer='json')
    def get_signs(self):
        check = self._check_token()
        if not check.Pass:
            return check.object
        from datetime import datetime
        date_str = self.request.params.get('date', None)
        date = datetime.strptime(date_str, '%Y%m%d')
        signs = self.__storage.retrieve_from_to(check.object, date.replace(hour=5, minute=0, second=0),
                                                date.replace(hour=23, minute=59, second=59))
        sign_in = dict()
        sign_out = dict()
        length = len(signs)
        if length is 1:
            sign_in = signs[0]
        if length is 2:
            sign_in = signs[0], sign_out = signs[1]
        return {'result': {'msg': 'Success', 'SignIn': str(sign_in.get('timestamp', '')), 'SignOut':
            str(sign_out.get('timestamp', ''))}}


class Sign:
    id = None
    behavior = None
    category = None
    description = None
    timestamp = None

    def to_dict(self):
        return self.__dict__

    def force_dict(self, sign_dict):
        self.id = sign_dict.get('_id', None)
        self.behavior = sign_dict.get('behavior', None)
        self.category = sign_dict.get('category', None)
        self.description = sign_dict.get('description', None)
        self.timestamp = sign_dict.get('timestamp', None)


class SignStorage:
    def __init__(self):
        from core import mongo_db
        self.__mongo = mongo_db.sign

    def __mongo_dict(self, sign):
        sign_dict = sign.to_dict()
        sign_id = sign_dict.get('id', None)
        if sign_id is not None:
            from core import MONGO_ID_STR
            sign_dict[MONGO_ID_STR] = sign_id
            sign_dict['id'] = None
        return sign_dict

    def create(self, sign):
        assert isinstance(sign, Sign), "Parameter should be the type Sign"
        from datetime import datetime
        sign.timestamp = datetime.now()
        return self.__mongo.insert(sign.to_dict())

    def retrieve(self, sign):
        sign_dict = self.__mongo.find_one(self.__mongo_dict(sign))
        sign = Sign()
        sign.force_dict(sign_dict)
        return sign

    def retrieve_from_to(self, behavior, from_, to):
        retrieve_condition = {'behavior': behavior, 'timestamp': {'$gt': from_, '$lt': to}}
        iterable = self.__mongo.find(retrieve_condition)#.sort({'timestamp': 1})
        size = iterable.count()
        if size is 1:
            return [iterable[0]]
        if size > 1:
            return [iterable[0], iterable[size-1]]
        else:
            return []

    def update(self, sign):
        self.__mongo.update(self.__mongo_dict(sign))

    def delete(self, sign):
        self.__mongo.delete(self.__mongo_dict(sign))
