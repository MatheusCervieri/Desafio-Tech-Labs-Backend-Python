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

def atualizar_db():
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def deletar_pessoa_db(pessoa):
    try:
        db.session.delete(pessoa)
        db.session.commit()
        return True  

    except Exception as e:
        print(f'Erro ao deletar pessoa: {str(e)}')
        db.session.rollback()
        return False  
