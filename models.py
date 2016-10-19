#!/usr/bin/env python
from database import *
from sqlalchemy.orm import relationship
from slugify import slugify
from wtforms.widgets import * #TextArea
from wtforms import * #TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField,validators, ValidationError
import wtforms.widgets.core
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
class UserMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100),nullable=True,unique=True)
    password = db.Column(db.String(600))
    password2=db.Column(db.String(200))
    created_at=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    post=db.relationship('Post', backref="user_member", lazy='dynamic')
    def verify_password(self, password):
        #return custom_app_context.encrypt(password) == self.password
        return custom_app_context.verify(password, self.password)
    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.password2 = password
    def add(user):
        db.session.add(user)
        return db.session.commit()
    def update(self):
        return session_commit()
    def delete(user):
        db.session.delete(user)
        return db.session.commit()
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = UserMember.query.get(data['id'])
        return user
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    npo_dn_no =  db.Column(db.String(15),unique=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    slug= db.Column(db.String(50))
    country = db.Column(db.String(50))
    city = db.Column(db.String(50))
    location_code = db.Column(db.String(30),nullable=True)
    org = db.Column(db.String(50),nullable=True)
    url = db.Column(db.String(50),nullable=True)
    phone = db.Column(db.String(50),nullable=True)
    status = db.Column(db.String(50),nullable=True)
    member_type = db.Column(db.String(50))
    credit = db.Column(db.Integer)
    verify_code = db.Column(db.String(50))
    published_at=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    requests=db.relationship('Request', backref="member", lazy='dynamic')
    offers=db.relationship('Offer', backref="member", lazy='dynamic')
    # cashes=db.relationship('Cash', backref="member", lazy='dynamic') #Y or N
    cash_donate = db.Column(db.Integer)
    def __init__(self,npo_dn_no, name,email,country,city,location_code,org,url,phone,status,member_type,credit,cash_donate,verify_code):
        self.npo_dn_no = npo_dn_no
        self.name = name
        self.email = email
        self.slug=slugify(name)
        self.country = country
        self.city = city
        self.location_code = location_code
        self.org = org
        self.url = url
        self.phone = phone
        self.status = status
        self.member_type = member_type
        self.credit = credit
        self.cash_donate = cash_donate
        self.verify_code = verify_code
    def add(member):
        db.session.add(member)
        return db.session.commit()
    def update(self):
        return session_commit()
    def delete(member):
        db.session.delete(member)
        return db.session.commit()
class Faq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question =  db.Column(db.String(200))
    answer = db.Column(db.Text)
    published_at=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    def __init__(self,question,answer):
        self.question = question
        self.answer = answer
    def add(faq):
        db.session.add(faq)
        return db.session.commit()
    def update(self):
        return session_commit()
    def delete(faq):
        db.session.delete(faq)
        return db.session.commit()
class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer,db.ForeignKey('member.id'))
    description =  db.Column(db.Text)
    shipping = db.Column(db.String(1))
    offer_tax = db.Column(db.String(1))
    disapear_day = db.Column(db.Integer,nullable=True)
    scrap  = db.Column(db.String(1))
    status = db.Column(db.Integer) #1,2 or 3
    image =  db.Column(db.Text)
    # offer_deact_date = db.Column(db.TIMESTAMP,nullable=True)
    published_at=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    requests=db.relationship('Request', backref="offer", lazy='dynamic')
    def __init__(self,member_id,description,shipping,offer_tax,disapear_day,scrap,status,image=''):
        self.member_id = member_id
        self.description = description
        self.shipping = shipping
        self.offer_tax = offer_tax
        self.disapear_day = disapear_day
        self.scrap = scrap
        self.status = status
        self.image = image
        # self.offer_deact_date = offer_deact_date
    def add(obj):
        db.session.add(obj)
        return db.session.commit()
    def update(self):
        return session_commit()
    def delete(obj):
        db.session.delete(obj)
        return db.session.commit()

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer,db.ForeignKey('member.id'))
    req_comment =  db.Column(db.Text)
    status = db.Column(db.Integer) #1,2 or 3
    offer_id = db.Column(db.Integer,db.ForeignKey('offer.id'))
    published_at=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    def __init__(self,member_id,req_comment,status,offer_id):
        self.member_id = member_id
        self.req_comment = req_comment
        self.status = status
        self.offer_id = offer_id
    def add(obj):
        db.session.add(obj)
        return db.session.commit()
    def update(self):
        return session_commit()
    def delete(obj):
        db.session.delete(obj)
        return db.session.commit()
# class Cash(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     member_id = db.Column(db.Integer,db.ForeignKey('member.id'))
#     amount =  db.Column(db.Integer)
#     published_at=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
#     def __init__(self,member_id,req_comment,status,offer_id):
#         self.member_id = member_id
#         self.req_comment = req_comment
#         self.status = status
#         self.offer_id = offer_id
#     def add(obj):
#         db.session.add(obj)
#         return db.session.commit()
#     def update(self):
#         return session_commit()
#     def delete(obj):
#         db.session.delete(obj)
#         return db.session.commit()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=  db.Column(db.String(100),nullable=True,unique=True)
    slug= db.Column(db.String(100),nullable=True)
    posts=db.relationship('Post', backref="category", lazy='dynamic')
    is_menu=db.Column(db.Integer,nullable=True,default=0)
    def get_absolute_url(self):
        return ('Category', (), {'slug': self.slug,'id': self.id,})
    def __str__(self):
        return self.name
    def to_Json(self):
        return dict(id=self.id,
            name=self.name,
            slug=self.slug
            )
    def __init__(self, name):
        self.slug=slugify(name)
        self.name =name
    def add(category):
        db.session.add(category)
        return db.session.commit()
    def delete(category):
        db.session.delete(category)
        return db.session.commit()
class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(255),nullable=True,unique=True)
    slug= db.Column(db.String(255),nullable=True)
    description = db.Column(db.Text,nullable=True)
    published_at= db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    is_menu=db.Column(db.Integer,nullable=True,default=0)
    def get_absolute_url(self):
        return ('Page', (), {'slug': self.slug,'id': self.id,})
    def __str__(self):
        return self.title
    def to_Json(self):
        return dict(id=self.id,
            title=self.title,
            slug=self.slug,
            description=self.description,
            published_at="{}".format(self.published_at)
            )
    def __init__(self, title,description):
        self.title = title
        self.slug =slugify(title)
        self.description=description
    def add(page):
        db.session.add(page)
        return db.session.commit()
    def delete(page):
        db.session.delete(page)
        return db.session.commit()
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),nullable=True,unique=True)
    description = db.Column(db.Text,nullable=True)
    feature_image=db.Column(db.Text,nullable=True)
    slug=db.Column(db.String(255),nullable=True,unique=True)
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'),nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user_member.id'))
    file=db.Column(db.String(255),nullable=True)
    published_at=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    views = db.Column(db.Integer, nullable=True)
    images = db.Column(db.Text,nullable=True)
    def to_Json(self):
        return dict(id=self.id,
            title=self.title,
            description=self.description,
            feature_image=self.feature_image,
            slug=self.slug,
            category_id=self.category_id,
            file=self.file,
            published_at="{}".format(self.published_at),
            view=self.view
            )
    def __init__(self, title, description, category_id, feature_image, user_id,file='',views=0,images=''):
        self.title = title
        self.slug =slugify(title)
        self.description = description
        self.feature_image = feature_image
        self.category_id = category_id
        self.file=file
        self.user_id = user_id
        self.views=views
        self.images=images
    def add(post):
        db.session.add(post)
        return db.session.commit()
    def update(self):
        return session_commit()
    def delete(post):
        db.session.delete(post)
        return db.session.commit()

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    firstname  = db.Column(db.String(255), nullable=True)
    lastname  = db.Column(db.String(255), nullable=True)
    published_at = db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    emailgroup=db.relationship('Emailgroup', backref="email", lazy='dynamic')
    def __str__(self):
        return self.name
    def update(self):
        return session_commit()
    def to_Json(self):
        return dict(id=self.id,
            email=self.email,
            name=self.name
            )
    def __init__(self, email,firstname,lastname):
        self.email = email
        self.firstname =firstname
        self.lastname = lastname
    def add(email):
        db.session.add(email)
        return db.session.commit()
    def delete(email):
        db.session.delete(email)
        return db.session.commit()
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(255))
    published_at = db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    emailgroups=db.relationship('Emailgroup', backref='"group"', lazy='dynamic')
    def __str__(self):
        return self.name
    # def update(self):
    #     return session_commit()    
    def to_Json(self):
        return dict(id=self.id,
            name=self.name
            )
    def __init__(self,name):
        self.name =name
    def add(group):
        db.session.add(group)
        return db.session.commit()
    def delete(group):
        db.session.delete(group)
        return db.session.commit()
class Emailgroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_id  = db.Column(db.Integer,db.ForeignKey('email.id'),nullable=True)
    group_id  = db.Column(db.Integer,db.ForeignKey("group.id"),nullable=True)
    published_at=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    def __str__(self):
        return self.email_id
    def to_Json(self):
        return dict(id=self.id,
            email_id=self.email_id,
            group_id=self.group_id
            )
    def __init__(self,email_id,group_id):
        self.email_id =email_id,
        self.group_id =group_id
    def add(emailgroup):
        db.session.add(emailgroup)
        return db.session.commit()
    def delete(emailgroup):
        db.session.delete(emailgroup)
        return db.session.commit()
class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(255))
    slug  = db.Column(db.String(255))
    url  = db.Column(db.String(255),nullable=True)
    feature_image=db.Column(db.Text,nullable=True)
    published_at=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    def __str__(self):
        return self.name
    # def update(self):
    #     return session_commit()    
    def to_Json(self):
        return dict(id=self.id,
            name=self.name,
            slug=self.slug,
            url=self.url,
            feature_image=self.feature_image
            )
    def __init__(self,name,url,feature_image):
        self.name =name
        self.slug = slugify(name)
        self.url =url
        self.feature_image =feature_image
    def add(partner):
        db.session.add(partner)
        return db.session.commit()
    def delete(partner):
        db.session.delete(partner)
        return db.session.commit()
class EmailList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(255))
    email  = db.Column(db.String(255))
    subject = db.Column(db.String(1000))
    description = db.Column(db.Text)
    reply_to = db.Column(db.String(255))
    sending_email = db.Column(db.String(255))
    sending_password = db.Column(db.String(255))
    sending_name    = db.Column(db.String(255))
    published_at=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    def __str__(self):
        return self.name
    # def update(self):
    #     return session_commit()    
    def to_Json(self):
        return dict(id=self.id,
            name=self.name,
            email=self.email,
            subject = self.subject,
            description = self.description,
            reply_top = self.reply_to,
            sending_email=self.sending_email,
            sending_password=self.sending_password,
            sending_name=self.sending_name
            )
    def __init__(self,name,email,subject,description,reply_to,sending_email,sending_password,sending_name):
        self.name =name
        self.email =email
        self.subject = subject
        self.description = description
        self.reply_to = reply_to
        self.sending_email=sending_email
        self.sending_password=sending_password
        self.sending_name=sending_name
    def add(messagelist):
        db.session.add(messagelist)
        return db.session.commit()
    def delete(messagelist):
        db.session.delete(messagelist)
        return db.session.commit()
class EmailSent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    send_to = db.Column(db.String(150))
    subject = db.Column(db.String(1000))
    description = db.Column(db.Text)
    reply_to = db.Column(db.String(255))
    sending_email = db.Column(db.String(255))
    sending_name    = db.Column(db.String(255))
    published_at=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    def __str__(self):
        return self.name
    # def update(self):
    #     return session_commit()    
    def to_Json(self):
        return dict(id=self.id,
            send_to = self.send_to,
            subject = self.subject,
            description = self.description,
            reply_top = self.reply_to,
            sending_email=self.sending_email,
            sending_name=self.sending_name,
            user_id  = self.user_id
            )
    def __init__(self,send_to,subject,description,reply_to,sending_email,sending_name):
        self.send_to= send_to,
        self.subject = subject,
        self.description = description,
        self.reply_to = reply_to,
        self.sending_email=sending_email,
        self.sending_name=sending_name, 
    def add(messagelist):
        db.session.add(messagelist)
        return db.session.commit()
    def delete(messagelist):
        db.session.delete(messagelist)
        return db.session.commit()

if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    # app.config['DEBUG'] = True
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    manager.run()
    app.run()




    # class Offer(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # # member_id = db.Column(db.Integer,db.ForeignKey('member.id'))
    # name = db.Column(db.String(255))
    # email = db.Column(db.String(255))
    # phone = db.Column(db.String(255))
    # city = db.Column(db.String(255))
    # country = db.Column(db.String(255))
    # postal_code = db.Column(db.String(255))
    # website = db.Column(db.String(255))
    # org = db.Column(db.String(255))

    # description =  db.Column(db.Text)
    # shipping = db.Column(db.String(1))
    # offer_tax = db.Column(db.String(1))
    # disapear_day = db.Column(db.Integer,nullable=True)
    # scrap  = db.Column(db.String(1))
    # status = db.Column(db.Integer) #1,2 or 3
    # image =  db.Column(db.Text)
    # # offer_deact_date = db.Column(db.TIMESTAMP,nullable=True)
    # published_at=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    # requests=db.relationship('Request', backref="offer", lazy='dynamic')
    # def __init__(self,name,email,phone,city,country,postal_code,website,org,description,shipping,offer_tax,disapear_day,scrap,status,image=''):
    #     self.name=name
    #     self.email=email
    #     self.phone = phone
    #     self.country=country
    #     self.postal_code=postal_code
    #     self.website=website
    #     self.org=org
    #     # self.member_id = member_id
    #     self.description = description
    #     self.shipping = shipping
    #     self.offer_tax = offer_tax
    #     self.disapear_day = disapear_day
    #     self.scrap = scrap
    #     self.status = status
    #     self.image = image
    #     # self.offer_deact_date = offer_deact_date
    # def add(obj):
    #     db.session.add(obj)
    #     return db.session.commit()
    # def update(self):
    #     return session_commit()
    # def delete(obj):
    #     db.session.delete(obj)
    #     return db.session.commit()