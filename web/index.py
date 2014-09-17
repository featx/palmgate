# -*- coding: utf-8 -*-
from pyramid.view import view_config


class IndexView:
    def __init__(self, request):
        self.request = request
        from core.account import AccountService
        self.__account_service = AccountService()
        self.__log_user = None

    @view_config(route_name='index', renderer='templates/index.pt')
    def index(self):
        username = 'palmtale'
        from hashlib import md5
        password = md5(bytes('123456789', 'utf8')).hexdigest().upper()
        account = self.__account_service.find_out_account(username, password)
        if account is None:
            return {}
        self.request.session['login_user'] = account
        from datetime import datetime
        now = datetime.now()

        from core.sign import SignStorage
        signs = SignStorage().retrieve_from_to(account.email, now.replace(hour=5, minute=0, second=0),
                                               now.replace(hour=23, minute=59, second=59))
        sign_time = ''
        if len(signs) > 0:
            sign_time = signs[0].get('timestamp')
        if isinstance(sign_time, datetime):
            sign_time = sign_time.strftime('%H:%M:%S')
        return {'login_user':{'display_name':account.display_name,
                                  'sign_in_time':sign_time}}