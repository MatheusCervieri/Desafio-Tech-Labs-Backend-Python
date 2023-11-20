from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
import colorlog

db = SQLAlchemy()

def configure_logger():
    handler = colorlog.StreamHandler()
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s",
        log_colors={'ERROR': 'red'},  
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger

logger = configure_logger()


def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



    db.init_app(app)


    from .views.pessoa_view import pessoa_bp
    app.register_blueprint(pessoa_bp)
    from app.views.teste_view import teste_bp
    app.register_blueprint(teste_bp)
    from app.views.documentation_view import documentation_bp
    app.register_blueprint(documentation_bp)

    with app.app_context():
        db.create_all()


    return app
