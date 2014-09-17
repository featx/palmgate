# -*- coding: utf-8 -*-
__author__ = 'palmtale'
import uuid
from core import MONGO_ID_STR


class TokenSurface:
    def __init__(self, request):
        self.request = request
        self.__token_service = AccessTokenService()

    def _check_token(self):
        token = self.request.params.get('token', None)
        result = Check()
        if token is None:
            result.Pass = False
            result.object = {'result': {'error': '', 'msg': 'Missing token!'}}
            return result
        access_token = self.__token_service.find_out_access_token(token)
        import datetime
        duration = datetime.timedelta(hours=access_token.duration)
        if access_token.start_at + duration < datetime.datetime.now():
            result.Pass = False
            result.object = {'result': {'error': '', 'msg': 'Token time out, please re-get one'}}
            return result
        result.Pass = True
        result.object = access_token.behavior
        return result


class Check:
    Pass = False
    object = None


class AccessToken:
    id = None
    token = None
    behavior = None
    start_at = None
    duration = None

    def to_dict(self):
        return self.__dict__

    def force_dict(self, token_dict):
        self.id = token_dict.get('id', None)
        self.token = token_dict.get('token', None)
        self.behavior = token_dict.get('behavior', None)
        self.start_at = token_dict.get('start_at', None)
        self.duration = token_dict.get('duration', None)


class AccessTokenService:
    def __init__(self):
        self.__storage = AccessTokenStorage()

    def achieve_access_token(self, behavior, hours=1):
        assert behavior is not None, "Did not provide the behavior for the access token"
        access_token = AccessToken()
        access_token.behavior = behavior
        access_token = self.__storage.retrieve(access_token)
        import datetime
        if access_token is None:
            access_token = AccessToken()
            access_token.behavior = behavior
        access_token.token = uuid.uuid1()
        access_token.start_at = datetime.datetime.now()
        access_token.duration = hours
        self.__storage.create_or_update(access_token)
        return str(access_token.token)

    def find_out_access_token(self, token):
        assert token is not None and token.strip() is not "", "Token should not be blank"
        access_token = AccessToken()
        import uuid as _uuid
        access_token.token = _uuid.UUID(token)
        access_token = self.__storage.retrieve(access_token)
        return access_token


class AccessTokenStorage:

    def __init__(self):
        from core import mongo_db
        self.__mongo = mongo_db.access_token

    def to_dict(self):
        return self.__dict__

    def create(self, access_token):
        assert isinstance(access_token, AccessToken), "Parameter 'access_token' should be the type AccessToken"
        _dict = access_token.to_dict()
        self.__mongo.insert(_dict)
        access_token.id = _dict.get(MONGO_ID_STR, None)

    def retrieve(self, access_token):
        assert isinstance(access_token, AccessToken), "Parameter 'access_token' should be the type AccessToken"
        mongo_dict = self.__mongo.find_one(access_token.to_dict())
        if mongo_dict is None:
            return None
        mongo_dict['id'] = mongo_dict.get(MONGO_ID_STR, None)
        del mongo_dict[MONGO_ID_STR]
        access_token = AccessToken()
        access_token.force_dict(mongo_dict)
        return access_token

    def update(self, access_token):
        assert isinstance(access_token, AccessToken), "Parameter 'access_token' should be type AccessToken"
        _dict = access_token.to_dict()
        if access_token.id is not None:
            _dict[MONGO_ID_STR] = access_token.id
            del _dict['id']
        self.__mongo.update(_dict)
        access_token.id = _dict.get(MONGO_ID_STR, None)

    def create_or_update(self, access_token):
        assert isinstance(access_token, AccessToken), "Parameter 'access_token' should be type AccessToken"
        _dict = access_token.to_dict()
        if _dict.get('id') is not None:
            _dict[MONGO_ID_STR] = _dict['id']
            del _dict['id']
            self.__mongo.update({MONGO_ID_STR: _dict[MONGO_ID_STR]}, _dict)
        else:
            self.__mongo.insert(_dict)
        access_token.id = _dict.get(MONGO_ID_STR, None)

    def delete(self, access_token):
        assert isinstance(access_token, AccessToken), "Parameter 'access_token' should be type AccessToken"
        self.__mongo.delete(access_token.to_dict())