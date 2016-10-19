#!/usr/bin/env python
from sqlalchemy import create_engine
from flask import Flask,session, make_response,send_file
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
#from passlib.apps import custom_app_context as pwd_context
from passlib.apps import * 
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPTokenAuth
from datetime import datetime, timedelta
from flask_mail import Mail,Message
from apscheduler.scheduler import Scheduler
import random
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://blog:blog@localhost:5432/recycles'
auth = HTTPTokenAuth(scheme='Token')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.secret_key = 'Hello@AmoogliCamSmallworld$Cambodia&*&'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
#template is the url of selected template 
ALLOWED_EXTENSIONS = set(['pdf','csv','docx','zip','rar','jpg','png','jpeg'])
#upload url for feature images
app.config['UPLOAD_FOLDER'] = 'static/images/images/'
app.config['UPLOAD_FOLDER_DONATE'] = 'static/images/'
expire_date = datetime.now()
expire_date = expire_date + timedelta(days=90)

SECRET_KEY="Hello@AmoogliCamSmallworld$Cambodia&*&"
def init_db():
    import BLOG.models
    Base.metadata.create_all(bind=engine)	