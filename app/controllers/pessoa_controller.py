from app.models.pessoa import Pessoa, db

def cadastrar_pessoa(nome_completo, data_nascimento, endereco, cpf, estado_civil):
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