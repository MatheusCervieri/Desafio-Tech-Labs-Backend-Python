from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    print("teste")
    app = Flask(__name__)
    CORS(app)
    
    # Configurações do aplicativo
    app.config.from_object('config.config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    print("teste2")

    # Inicializações
    db.init_app(app)
    print("teste3")

    # Registra blueprints
    from .views.pessoa_view import pessoa_bp
    app.register_blueprint(pessoa_bp)

    # Cria as tabelas
    with app.app_context():
        db.create_all()


    return app
