from datetime import datetime
from . import db
import bleach
from markdown import markdown
from flask_login import UserMixin

class Post(db.Model):
    '''
    一个类的实例是一行
    一个类的属性是一列
    提交的文章数据
    '''



    __tablename__ = 'posts'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.Text)
    into=db.Column(db.Text)
    body =db.Column(db.Text)
    body_html=db.Column(db.Text)
    isarticle=db.Column(db.Boolean,default=True)
    timestamp=db.Column(db.DateTime,index=True,default=datetime.utcnow)
    view_times=db.Column(db.Integer)

    #以类别作为外键
    category_id=db.Column(db.Integer,db.ForeignKey('categories.id'))

    @staticmethod
    def on_changed_body(targrt,value,oldvalue,initiator):
        allowed_tags = [
            'a',
            'abbr',
            'acronym',
            'b',
            'blockquote',
            'code',
            'em',
            'i',
            'li',
            'ol',
            'strong',
            'ul',
            'h1',
            'h2',
            'h3',
            'p'
        ]
        targrt.body_html=bleach.linkify(bleach.clean(
            markdown(value,output_format='html'),tags=allowed_tags,strip=True
        ))
    #返回类别名
    @property
    def category_name(self):
        return Category.query.filter_by(id=self.category_id).first().category_name

db.event.listen(Post.body,'set',Post.on_changed_body)

class Category(db.Model):
    __tablename__='categories'
    id=db.Column(db.Integer,primary_key=True)
    category_name=db.Column(db.String(64))

class Administrator(UserMixin,db.Model):
    __tablename__='Administrator'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(64),unique=True,index=True)