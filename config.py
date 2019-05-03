import os
SECRET_KEY = os.urandom(24)

DEBUG = True

DB_USERNAME = 'root'
DB_PASSWORD = ''
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'zlbbs'

# PERMANENT_SESSION_LIFETIME =

DB_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8'

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = 'LGF'
FRONT_USER_ID = 'ABC'

MAIL_SERVER = "smtp.qq.com"
###  SSL: 465    TSL:587
MAIL_PORT = '465'
# MAIL_USE_TLS = default False
MAIL_USE_SSL = True
# MAIL_DEBUG = default app.debug
MAIL_USERNAME = os.environ.get('QEmail')
MAIL_PASSWORD = os.environ.get('QEmailPassword')
MAIL_DEFAULT_SENDER = MAIL_USERNAME

# 阿里云大于发送验证码的配置
ALIDAYU_ACCESSKEY_ID = os.environ.get('AccessKeyID')
ALIDAYU_ACCESSKEY_SECRET = os.environ.get('AccessKeySecret')
ALIDAYU_SIGN_NAME = "BBS论坛LGF"
ALIDAYU_TEMPLATE_CODE = os.environ.get('TEMPLATE_CODE')

# 配置UEditor
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "M4zCEW4f9XPanbMN-Lb9O0S8j893f0e1ezAohFVL"
UEDITOR_QINIU_SECRET_KEY = "7BKV7HeEKM3NDJk8_l_C89JI3SMmeUlAIatzl9d4"
UEDITOR_QINIU_BUCKET_NAME = "hyvideo"
UEDITOR_QINIU_DOMAIN = "http://7xqenu.com1.z0.glb.clouddn.com/"

# Flask - pagination
PER_PAGE = 10

# Celery 配置
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
