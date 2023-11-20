from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
import colorlog
import sys
from colorama import Fore, Style

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


def create_app(config_name='development'):
    
    
    app = Flask(__name__)
    
    CORS(app)
    
    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teste.db'
        logger.setLevel(logging.CRITICAL)
    else:
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
        # Criação do banco de dados
        db.create_all()
    
    
    
    welcome_message = (
    f"{Fore.GREEN}{Style.BRIGHT}Sua API de cadastro de pessoas está rodando!{Style.RESET_ALL}\n"
    f"{Fore.CYAN}Rotas principais:{Style.RESET_ALL}\n"
    f"{Fore.YELLOW}- http://127.0.0.1:5000/pessoas/adicionar (POST) => Cadastrar uma nova pessoa\n"
    f"{Fore.YELLOW}- http://127.0.0.1:5000/pessoas/edit/id/<int:pessoa_id> (PUT) => Atualizar Pessoa por ID\n"
    f"{Fore.YELLOW}- http://127.0.0.1:5000/pessoas/edit/cpf/<string:pessoa_cpf> (PUT) => Atualizar Pessoa por CPF\n"
    f"{Fore.YELLOW}- http://127.0.0.1:5000/pessoas (GET) => Listar Pessoas\n"
    f"{Fore.YELLOW}- http://127.0.0.1:5000/pessoas/<string:cpf> (GET) => Obter Pessoa por CPF\n"
    f"{Fore.YELLOW}- http://127.0.0.1:5000/pessoas/id/<int:pessoa_id> (GET) => Obter Pessoa por ID\n"
    f"{Fore.YELLOW}- http://127.0.0.1:5000/pessoas/delete/id/<int:pessoa_id> (DELETE) => Deletar Pessoa por ID\n"
    f"{Fore.YELLOW}- http://127.0.0.1:5000/pessoas/delete/cpf/<string:cpf> (DELETE) => Deletar Pessoa por CPF\n"
    f"{Fore.CYAN}Rotas de ajuda:{Style.RESET_ALL}\n"
    f"{Fore.YELLOW}- http://127.0.0.1:5000/teste{Style.RESET_ALL} => Página html que permite fazer requisições para todas as rotas\n"
    f"{Fore.YELLOW}- http://127.0.0.1:5000/documentacao{Style.RESET_ALL} => Documentação de todas as rotas do servidor\n"
    f"{Fore.MAGENTA}Divirta-se explorando as funcionalidades!{Style.RESET_ALL}"
    )
    if not config_name == 'testing':
        print(welcome_message)

    return app
