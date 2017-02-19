# -*- coding: utf-8-*-
from app import create_app,db
from app.models import Post,Category,Administrator
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand
import os


app=create_app(os.getenv('FLASK_CONFIG') or 'default')

manager=Manager(app)
migrate=Migrate(app,db)

def make_shell_context():
    return dict(app=app, db=db, Post=Post, Category=Category,Administrator=Administrator)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


# 启动分析器,在请求分析器的监视下运行程序
@manager.command
# 使用 python manage.py profile 启动程序后,终端会显示每条请求的分析数据,其中包含运行最慢的 25 个函数。--length 选项可以修改报告中显示的函数数量
# 如果指定了--profile-dir 选项,每条请求的分析数据就会保存到指定目录下的一个文件中
def profile(length=25, profile_dir=None):
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run()


if __name__ == '__main__':
    manager.run()