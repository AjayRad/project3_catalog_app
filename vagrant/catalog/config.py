import os
GOOGLE_LOGIN_CLIENT_ID = "83450637791-rob75ftrerqkh3hsohmgndjrhl76ifbh.apps.googleusercontent.com"
GOOGLE_LOGIN_CLIENT_SECRET = "K3-8LX3y9187INWj1mvl04AN"
FB_LOGIN_CLIENT_ID = '470154729788964'
FB_LOGIN_CLIENT_SECRET = '010cc08bd4f51e34f3f3e684fbdea8a7'

OAUTH_CREDENTIALS = {
    'google': {
        'id': GOOGLE_LOGIN_CLIENT_ID,
        'secret': GOOGLE_LOGIN_CLIENT_SECRET
    },
    'facebook': {
        'id': FB_LOGIN_CLIENT_ID,
        'secret': FB_LOGIN_CLIENT_SECRET
    }
}


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'catalogapp/models/catalog.db')
