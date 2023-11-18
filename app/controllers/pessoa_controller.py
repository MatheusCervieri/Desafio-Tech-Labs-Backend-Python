from app.models.pessoa import Pessoa
from app import db
from datetime import datetime

def cadastrar_pessoa(nome_completo, data_nascimento, endereco, cpf, estado_civil):

    data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
    nova_pessoa = Pessoa(
        nome_completo=nome_completo,
        data_nascimento=data_nascimento,
        endereco=endereco,
        cpf=cpf,
        estado_civil=estado_civil
    )

    db.session.add(nova_pessoa)
    db.session.commit()

    return nova_pessoa