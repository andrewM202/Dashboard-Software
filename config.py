import os
# basedir is set as a relative path from any place we call it to this file
basedir = os.path.abspath(os.path.dirname(__file__))

# Below I create a classes with the configuration settings for all the stages of my product. Config is the default config, ProductionConfig for production, etc.
class Config(object):
    FLASK_DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'wegwerg^#$T34y^#_#$534;^_#$asf63ASF'
    # SEND_FILE_MAX_AGE_DEFAULT makes it so the browser doesn't store any of the CSS or HTML in a cache. It makes for easier development
    SEND_FILE_MAX_AGE_DEFAULT = 0
    # SECURITY_LOGIN_URL = ''


class ProductionConfig(Config):
    FLASK_DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    FLASK_DEBUG = True

class DevelopmentConfig(Config):
    TESTING = True
    FLASK_DEBUG = True
