from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
import colorlog

db = SQLAlchemy()

def configure_logger():
    # Configurar o logger com colorlog
    handler = colorlog.StreamHandler()
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s",
        log_colors={'ERROR': 'red'},  # Defina a cor para mensagens de erro
    )
    handler.setFormatter(formatter)

    # Configurar o logger
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger

logger = configure_logger()


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, methods=["GET", "POST", "PUT", "DELETE"])
    
    # Configurações do aplicativo
    app.config.from_object('config.config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



    # Inicializações
    db.init_app(app)


    # Registra blueprints
    from .views.pessoa_view import pessoa_bp
    app.register_blueprint(pessoa_bp)
    from app.views.teste_view import teste_bp
    app.register_blueprint(teste_bp)

    # Cria as tabelas
    with app.app_context():
        db.create_all()


    return app
