from flask import Flask
import flask_sqlalchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_babel import Babel
from . util import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# init SQLAlchemy so we can use it later in our models
db = flask_sqlalchemy.SQLAlchemy()
babel = Babel()
config = Config.getConfig().config

def create_app():
    app = Flask(__name__)

    #app.config.from_pyfile('babel.cfg')
    app.config['SECRET_KEY'] = 'zZbHaknEBCqNS6tNBF3A'
    address='mysql+pymysql://root:' + config["DB_PASSWORD"] + '@' + config["DB_HOST"] + ':' + config["DB_PORT"] + '/wedding'
    app.config['SQLALCHEMY_DATABASE_URI'] = address

    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['BABEL_DEFAULT_LOCALE'] = 'se'
    app.config['BABEL_DEFAULT_TIMEZONE']= 'UTC+1'
    # add to your app.config or config.py file
    app.config['LANGUAGES'] = {
        'se': 'Swedish',
        'en': 'English'
    }

    db.init_app(app)
    babel.init_app(app)
    return app


app=create_app()

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["500 per day", "60 per hour"]
)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
