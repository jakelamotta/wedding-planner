from flask import Flask
import flask_sqlalchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_babel import Babel

# init SQLAlchemy so we can use it later in our models
db = flask_sqlalchemy.SQLAlchemy()
babel = Babel()
#app = Flask(__name__)
def create_app():
    app = Flask(__name__)

    #app.config.from_pyfile('babel.cfg')
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/wedding'
    app.config['BABEL_DEFAULT_LOCALE'] = 'se'
    app.config['BABEL_DEFAULT_TIMEZONE']= 'UTC+1'
    # add to your app.config or config.py file
    app.config['LANGUAGES'] = {
        'se': 'Swedish',
        'en': 'English'
    }

#    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    babel.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
