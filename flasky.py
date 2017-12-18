#/usr/bin/env python
#-*- coding:utf8 -*-
from flask import Flask,render_template,url_for,session,redirect,flash
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import InputRequired

## 插件
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy


class myform(FlaskForm):
    username = StringField(u'用户名',validators=[InputRequired()])
    password = PasswordField(u'密码',validators=[InputRequired()])
    submit = SubmitField(u'提交')

## 数据库表格





myflask = Flask(__name__)
myflask.config['SECRET_KEY'] = '123456'
myflask.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flasktest:Flask1204.@172.18.26.210/flasktest'
# myflask.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\AIT-003\\Envs\\flask\\project\\db\\test.db'
Bootstrap(myflask)
Moment(myflask)
manage = Manager(myflask)
db = SQLAlchemy(myflask)

class Role(db.Model):
    __tablename__= 'roles'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),unique = True)
    users = db.relationship('User',backref = 'role')


    def __repr__(self):
        return '< Role {} >'.format(self.name)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64),unique = True, index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return '< User {} >'.format(self.username)






@myflask.route('/',methods=['GET','POST'])
def index():
    form = myform()
    if form.validate_on_submit():
        if not form.username.data == '111':
            flash(u'需要输入一些内容')
        session['username'] = form.username.data
        session['password'] = form.password.data
        return redirect(url_for('index'))
    return render_template('index.html',current_time = datetime.utcnow(),
                            username = session.get('username'),password = session.get('password'),
                            form = form)

if __name__ == '__main__':
    manage.run()
