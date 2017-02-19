import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    WTF_CSRF_ENABLED = True
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #跟踪修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_POSTS_PER_PAGE = 5
    # 缓慢查询设为0.5 秒
    FLASKY_SLOW_DB_QUERY_TIME = 0.5
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    PASSWORD='ZHANG'
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    @classmethod
    def init_app(cls,app):
        Config.init_app(app)
        # 输出到 stderr,日志级别为警告
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)

        app.logger.addHandler(file_handler)

#部署后添加部署配置
config = {
    'development': DevelopmentConfig,
    'default':DevelopmentConfig

}
