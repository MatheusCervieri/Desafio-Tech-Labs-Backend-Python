from flask import Blueprint, request, jsonify
from app.controllers.pessoa_controller import cadastrar_pessoa , atualizar_pessoa_db , deletar_pessoa_db
from app.views.validation_utils import validar_cpf, validar_data_nascimento , validar_estado_civil
from app.models.pessoa import Pessoa


pessoa_bp = Blueprint('pessoa', __name__)


@pessoa_bp.route('/pessoas/adicionar', methods=['POST'])
def cadastrar():
    try:
        data = request.get_json()

        # Validar campos obrigatórios
        required_fields = ['nome_completo', 'data_nascimento', 'endereco', 'cpf', 'estado_civil']
        for field in required_fields:
            if field not in data or not data[field]:
                error_message = f'O campo {field} é obrigatório.'
                print(error_message)
                return jsonify({'error': error_message}), 400

        # Validar formato de CPF, data de nascimento e estado civil
        if not validar_cpf(data['cpf']):
            error_message = 'CPF inválido.'
            print(error_message)
            return jsonify({'error': error_message}), 400

        if not validar_data_nascimento(data['data_nascimento']):
            error_message = 'Data de nascimento inválida. Use o formato YYYY-MM-DD.'
            print(error_message)
            return jsonify({'error': error_message}), 400
        
        if not validar_estado_civil(data['estado_civil']):
            error_message = 'Estado civil inválido.'
            print(error_message)
            return jsonify({'error': error_message}), 400

        # Checar na database se o cpf já existe
        if Pessoa.query.filter_by(cpf=data['cpf']).first():
            error_message = 'CPF já cadastrado.'
            print(error_message)
            return jsonify({'error': error_message}), 400

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
    
@pessoa_bp.route('/pessoas', methods=['GET'])
def listar_pessoas():
    try:
        # Consultar todas as pessoas cadastradas
        pessoas = Pessoa.query.all()

        # Criar lista de dicionários com informações sobre cada pessoa
        pessoas_info = []
        for pessoa in pessoas:
            pessoa_info = {
                'id': pessoa.id,
                'nome_completo': pessoa.nome_completo,
                'data_nascimento': pessoa.data_nascimento.strftime('%Y-%m-%d'),
                'endereco': pessoa.endereco,
                'cpf': pessoa.cpf,
                'estado_civil': pessoa.estado_civil
            }
            pessoas_info.append(pessoa_info)

        # Resposta de sucesso
        return jsonify({'pessoas': pessoas_info}), 200

    except Exception as e:
        # Imprimir detalhes do erro no console
        print(f'Erro ao listar pessoas: {str(e)}')

        # Retornar detalhes do erro na resposta JSON
        return jsonify({'error': f'Ocorreu um erro interno no servidor. Detalhes: {str(e)}'}), 500

@pessoa_bp.route('/pessoas/<string:cpf>', methods=['GET'])
def obter_pessoa_por_cpf(cpf):
    try:
        if not validar_cpf(cpf):
            error_message = 'CPF inválido.'
            print(error_message)
            return jsonify({'error': error_message}), 400
        
        pessoa = Pessoa.query.filter_by(cpf=cpf).first()

        if pessoa:
            # Retorna os dados da pessoa
            return jsonify({
                'id': pessoa.id,
                'nome_completo': pessoa.nome_completo,
                'data_nascimento': pessoa.data_nascimento,
                'endereco': pessoa.endereco,
                'cpf': pessoa.cpf,
                'estado_civil': pessoa.estado_civil
            })
        else:
            print("Pessoa não encontrada.")
            return jsonify({'error': 'Pessoa não encontrada.'}), 404

    except Exception as e:
        # Imprimir detalhes do erro no console
        print(f'Erro ao obter pessoa por CPF: {str(e)}')

        # Retornar detalhes do erro na resposta JSON
        
        return jsonify({'error': f'Ocorreu um erro interno no servidor. Detalhes: {str(e)}'}), 500

@pessoa_bp.route('/pessoas/id/<int:pessoa_id>', methods=['GET'])
def obter_pessoa_por_id(pessoa_id):
    try:
        pessoa = Pessoa.query.get(pessoa_id)

        if pessoa:
            # Retorna os dados da pessoa
            return jsonify({
                'id': pessoa.id,
                'nome_completo': pessoa.nome_completo,
                'data_nascimento': pessoa.data_nascimento,
                'endereco': pessoa.endereco,
                'cpf': pessoa.cpf,
                'estado_civil': pessoa.estado_civil
            })
        else:
            # ID não encontrado
            print("Pessoa não encontrada ou id inválido.")
            return jsonify({'error': 'Pessoa não encontrada.'}), 404

    except Exception as e:
        # Imprimir detalhes do erro no console
        print(f'Erro ao obter pessoa por ID: {str(e)}')

        # Retornar detalhes do erro na resposta JSON
        return jsonify({'error': f'Ocorreu um erro interno no servidor. Detalhes: {str(e)}'}), 500
    

#Preciso receber um objeto com campo que será modificado e valor.
#Preciso saber se o campo é efetivamente um campo da entidade pessoa.
#Preciso saber se o valor é válido para o campo. Se for modifico, se não for, retorno um erro. 
@pessoa_bp.route('/pessoas/id/<int:pessoa_id>', methods=['PUT'])
def atualizar_pessoa_por_id(pessoa_id):
   return "Hello World"

@pessoa_bp.route('/pessoas/delete/id/<int:pessoa_id>', methods=['DELETE'])
def deletar_pessoa_por_id(pessoa_id):
    try:
        pessoa = Pessoa.query.get(pessoa_id)

        if pessoa:
            if deletar_pessoa_db(pessoa):  
                return jsonify({'message': 'Pessoa deletada com sucesso.'}), 200
            else:
                return jsonify({'error': 'Erro ao deletar pessoa.'}), 500
        else:
            return jsonify({'error': 'Pessoa não encontrada.'}), 404

    except Exception as e:
        print(f'Erro ao deletar pessoa por ID: {str(e)}')
        return jsonify({'error': f'Ocorreu um erro interno no servidor. Detalhes: {str(e)}'}), 500

@pessoa_bp.route('/pessoas/delete/cpf/<string:cpf>', methods=['DELETE'])
def deletar_pessoa_por_cpf(cpf):
    try:
        pessoa = Pessoa.query.filter_by(cpf=cpf).first()

        if pessoa:
            if deletar_pessoa_db(pessoa): 
                return jsonify({'message': 'Pessoa deletada com sucesso.'}), 200
            else:
                return jsonify({'error': 'Erro ao deletar pessoa.'}), 500
        else:
            return jsonify({'error': 'Pessoa não encontrada.'}), 404

    except Exception as e:
        print(f'Erro ao deletar pessoa por CPF: {str(e)}')
        return jsonify({'error': f'Ocorreu um erro interno no servidor. Detalhes: {str(e)}'}), 500

