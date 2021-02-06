from flask import Flask
from project_string.config import firebase
import os

def create_app(config_class = firebase):
    app = Flask(__name__)
    app.config.from_object(firebase)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
#     app.config.update(dict(
#     SECRET_KEY = os.environ.get('SECRET_KEY'),
#     WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY')
# ))
    #csrf.init_app(app)

    from project_string.users.routes import users
    from project_string.main.routes import main
    from project_string.errors.error_handlers import errors
    
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
