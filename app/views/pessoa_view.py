from flask import Blueprint, request, jsonify
from app.controllers.pessoa_controller import cadastrar_pessoa
from app.views.validation_utils import validar_cpf, validar_data_nascimento , validar_estado_civil
from app.models.pessoa import Pessoa


pessoa_bp = Blueprint('pessoa', __name__)


@pessoa_bp.route('/pessoas/adicionar', methods=['POST'])
def cadastrar():
    print("Chegou aqui")
    try:
        data = request.get_json()

        # Validar campos obrigatórios
        required_fields = ['nome_completo', 'data_nascimento', 'endereco', 'cpf', 'estado_civil']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'O campo {field} é obrigatório.'}), 400

        # Validar formato de CPF e data de nascimento
        if not validar_cpf(data['cpf']):
            return jsonify({'error': 'CPF inválido.'}), 400

        if not validar_data_nascimento(data['data_nascimento']):
            return jsonify({'error': 'Data de nascimento inválida. Use o formato YYYY-MM-DD.'}), 400
        
        if not validar_estado_civil(data['estado_civil']):
            return jsonify({'error': 'Estado civil inválido.'}), 400

        # Checar na database se o cpf já existe
        if Pessoa.query.filter_by(cpf=data['cpf']).first():
            return jsonify({'error': 'CPF já cadastrado.'}), 400

        #Checar na database se o cpf já existe. 

        # Extrair dados
        nome_completo = data['nome_completo']
        data_nascimento = data['data_nascimento']
        endereco = data['endereco']
        cpf = data['cpf']
        estado_civil = data['estado_civil']

        # Cadastrar pessoa
        nova_pessoa = cadastrar_pessoa(
            nome_completo=nome_completo,
            data_nascimento=data_nascimento,
            endereco=endereco,
            cpf=cpf,
            estado_civil=estado_civil
        )

        # Resposta de sucesso
        return jsonify({
            'id': nova_pessoa.id,
            'nome_completo': nova_pessoa.nome_completo,
            'data_nascimento': nova_pessoa.data_nascimento,
            'endereco': nova_pessoa.endereco,
            'cpf': nova_pessoa.cpf,
            'estado_civil': nova_pessoa.estado_civil
        }), 201  # 201 Created é apropriado para criação de recursos

    except Exception as e:
        # Imprimir detalhes do erro no console
        print(f'Erro no cadastro de pessoa: {str(e)}')

        # Retornar detalhes do erro na resposta JSON
        return jsonify({'error': f'Ocorreu um erro interno no servidor. Detalhes: {str(e)}'}), 500