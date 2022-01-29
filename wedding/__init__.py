from flask import Flask
import flask_sqlalchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_babel import Babel
from . util import Config, EmailHelper
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from logging.config import dictConfig

# init SQLAlchemy so we can use it later in our models
db = flask_sqlalchemy.SQLAlchemy()
babel = Babel()
config = Config.getConfig().config

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def create_app():
    app = Flask(__name__)

    #app.config.from_pyfile('babel.cfg')
    app.config['SECRET_KEY'] = 'zZbHaknEBCqNS6tNBF3A'
    address='mysql+pymysql://root:' + config["DB_PASSWORD"] + '@' + config["DB_HOST"] + ':' + config["DB_PORT"] + '/wedding'
    app.config['SQLALCHEMY_DATABASE_URI'] = address

    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['BABEL_DEFAULT_LOCALE'] = 'sv'
    app.config['BABEL_DEFAULT_TIMEZONE']= 'UTC+1'
    # add to your app.config or config.py file
    app.config['LANGUAGES'] = ["sv", "sv_SV", "en"]

    db.init_app(app)
    babel.init_app(app)
    return app


app=create_app()

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "250 per hour"]
)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
