# encoding: utf-8
import os

DEBUG = True

SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:malizhi123.@127.0.0.1:3306/myblog?charset=utf8?"

SQLALCHEMY_TRACK_MODIFICATIONS=False

