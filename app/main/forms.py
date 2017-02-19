from flask_wtf import Form
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length
from flask_pagedown.fields import PageDownField


class PostForm(Form):
    #支持markdown
    title=TextAreaField("编辑文章标题",validators=[DataRequired()])
    into=TextAreaField("文章简介")
    body=PageDownField("文章正文",validators=[DataRequired()])
    category_name=StringField("分类",validators=[Length(0,32)])
    submit=SubmitField('提交')