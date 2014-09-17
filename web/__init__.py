# -*- coding: utf-8 -*-
__author__ = 'palmtale'


def config(config):
    config.include('pyramid_chameleon')
    # static assets
    config.add_static_view('static', 'web:static', cache_max_age=3600)
    # Session Config
    from pyramid.session import SignedCookieSessionFactory
    config.set_session_factory(SignedCookieSessionFactory('secret_key'))
    # routes
    config.add_route('index', '/')
    config.scan()