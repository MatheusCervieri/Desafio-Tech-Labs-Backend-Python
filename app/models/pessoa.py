from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=True)
    endereco = db.Column(db.String(255), nullable=True)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    estado_civil = db.Column(db.String(20), nullable=True)

    def __init__(self, nome_completo, data_nascimento, endereco, cpf, estado_civil):
        self.nome_completo = nome_completo
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.cpf = cpf
        self.estado_civil = estado_civil