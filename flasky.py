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
from flask_script import Manager,Shell
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand

class myform(FlaskForm):
    username = StringField(u'用户名',validators=[InputRequired()])
    password = PasswordField(u'密码',validators=[InputRequired()])
    submit = SubmitField(u'提交')

## 数据库表格

myflask = Flask(__name__)
myflask.config['SECRET_KEY'] = '123456'
myflask.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flasktest:Flask1204.@172.18.26.210/flasktest?charset=utf8'
myflask.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
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
        return u'< Role {} >'.format(self.name)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64),unique = True, index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return u'< User {} >'.format(self.username)

@myflask.route('/',methods=['GET','POST'])


def make_shell_context():
    return dict(app=myflask,db=db,User=User,Role=Role)
manage.add_command("shell",Shell(make_context=make_shell_context))

migrate = Migrate(myflask,db)
manage.add_command('db',MigrateCommand)


def index():
    form = myform()
    if form.validate_on_submit():
        # if not form.username.data == '111':
            # flash(u'需要输入一些内容')
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            session['known'] = False
            user = User(username = form.username.data)
            db.session.add(user)
            db.session.commit()
        else:
            session['known'] = True

        session['username'] = form.username.data
        session['password'] = form.password.data
        form.username.data = ''
        form.password.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',current_time = datetime.utcnow(),
                            username = session.get('username'),password = session.get('password'),
                            form = form,known = session.get('known'))

if __name__ == '__main__':
    manage.run()
