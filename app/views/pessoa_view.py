from flask import Blueprint, request, jsonify
from app.controllers.pessoa_controller import cadastrar_pessoa

pessoa_bp = Blueprint('pessoa', __name__)

@pessoa_bp.route('/pessoas', methods=['POST'])
def cadastrar():
    data = request.get_json()

    nome_completo = data.get('nome_completo')
    data_nascimento = data.get('data_nascimento')
    endereco = data.get('endereco')
    cpf = data.get('cpf')
    estado_civil = data.get('estado_civil')

    nova_pessoa = cadastrar_pessoa(
        nome_completo=nome_completo,
        data_nascimento=data_nascimento,
        endereco=endereco,
        cpf=cpf,
        estado_civil=estado_civil
    )

    return jsonify({
        'id': nova_pessoa.id,
        'nome_completo': nova_pessoa.nome_completo,
        'data_nascimento': nova_pessoa.data_nascimento,
        'endereco': nova_pessoa.endereco,
        'cpf': nova_pessoa.cpf,
        'estado_civil': nova_pessoa.estado_civil
    })