# -*- coding: utf-8 -*-
__author__ = 'palmtale'
import hashlib
from core import MONGO_ID_STR
from pyramid.view import view_config


class AccountSurface:
    def __init__(self, request):
        self.request = request
        self.__service = AccountService()

    @view_config(route_name='register_token', renderer='json')
    def assign_token(self):
        user_identity = self.request.params.get('username', None)
        if user_identity is None or user_identity.strip() is "":
            return {'result': {'error': '', 'msg': 'Missing parameter username'}}
        password = self.request.params.get('password', None)
        if password is None or password.strip() is "":
            return {'result': {'error': '', 'msg': 'Missing parameter password'}}
        password = hashlib.md5(bytes(password, 'utf-8')).hexdigest().upper()
        account = self.__service.find_out_account(user_identity, password)
        if account.id is None:
            return {'result': {'error': '', 'msg': 'No account found'}}
        else:
            if account.email is None:
                return {'result': {'error': '', 'msg': 'Did not set email for account ' + account.id}}
            from core.access_token import AccessTokenService
            return {'result': {'token': AccessTokenService().achieve_access_token(account.email)}}


class AccountService:
    def __init__(self):
        self.__storage = AccountStorage()

    def find_out_account(self, user_identity, password):
        user_identities = [{'username': user_identity},
                           {'email': user_identity},
                           {'cell_phone_number': user_identity}]
        dict_condition = {'password': password, '$or': user_identities}
        return self.__storage.retrieve_as_dict_condition(dict_condition)


class Account:
    id = None
    work_id = None
    username = None
    password = None
    display_name = None
    first_name = None
    last_name = None
    gender = None
    age = None
    email = None
    cell_phone_number = None
    civil_id = None
    title = None
    position = None
    create_at = None
    update_at = None

    def to_dict(self):
        return self.__dict__

    def force_dict(self, account_dict):
        self.id = account_dict.get('id', None)
        self.work_id = account_dict.get('work_id', None)
        self.username = account_dict.get('username', None)
        self.password = account_dict.get('password', None)
        self.display_name = account_dict.get('display_name', None)
        self.first_name = account_dict.get('first_name', None)
        self.last_name = account_dict.get('last_name', None)
        self.gender = account_dict.get('gender', None)
        self.age = account_dict.get('age', None)
        self.email = account_dict.get('email', None)
        self.cell_phone_number = account_dict.get('cell_phone_number', None)
        self.civil_id = account_dict.get('civil_id', None)
        self.title = account_dict.get('title', None)
        self.position = account_dict.get('position', None)
        self.create_at = account_dict.get('create_at', None)
        self.update_at = account_dict.get('update_at', None)


#Mongo:
class AccountStorage:
    def __init__(self):
        from core import mongo_db
        self.__mongo = mongo_db.account

    def create(self, account):
        assert not self.exist_same_unique_attr(account), "Some serialize field is existed"
        import time
        account.id = None
        account.create_at = time.time()
        account.update_at = account.create_at
        return self.__mongo.insert(account.to_dict())

    def exist_same_unique_attr(self, account):
        conditions = []
        conditions.append({'work_id': account.work_id})
        conditions.append({'username': account.username})
        conditions.append({'email': account.email})
        conditions.append({'cell_phone_number': account.cell_phone_number})
        if self.__mongo.find_one({'$or': conditions}) is None:
            return False
        else:
            return True

    def __mongo_dict(self, account):
        account_dict = account.to_dict()
        if account.id is not None:
            account_dict[MONGO_ID_STR] = account.id
            del account_dict['id']
        return account_dict

    def retrieve(self, account):
        assert isinstance(account, Account), "Parameter account is incorrect type, should be Account"
        account_dict = self.__mongo.find_one(self.__mongo_dict(account))
        if account_dict is not None:
            account_dict['id'] = account_dict.get('_id')
            del account_dict['_id']
            account = Account()
            account.force_dict(account_dict)
            return account
        return None

    def retrieve_as_dict_condition(self, dict_conditioin):
        assert isinstance(dict_conditioin, dict), "Parameter dict_condition should be type dict"
        account_dict = self.__mongo.find_one(dict_conditioin)
        if account_dict is not None:
            account_dict['id'] = account_dict.get('_id')
            del account_dict['_id']
            account = Account()
            account.force_dict(account_dict)
            return account
        return None

    def delete(self, account):
        assert isinstance(account, Account), "Parameter account is incorrect type, should be Account"
        return self.__mongo.remove(self.__mongo_dict(account))

    def update(self, account):
        assert isinstance(account, Account), "Parameter account is incorrect type, should be Account"
        import time
        account.update_at = time.time()
        return self.__mongo.update(self.__mongo_dict(account))
