import datetime
from flask import Blueprint, request, jsonify
from app.controllers.pessoa_controller import cadastrar_pessoa , atualizar_pessoa_db
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
    

# Preciso checar se o objeto que é recebido na requisição possui algum dos campos que eu quero atualizar.
# Se sim, eu preciso fazer a validação e ver se o valor que está no objeto é um valor válido para ser atualizado. 
# Se sim, eu atualizo o valor do objeto pessoa com o valor que está no objeto recebido na requisição.
# Se não, eu retorno um erro apropiado. Ou eu falo que a requisição não enviou um objeto correto ou explico o que está errado na atualização do campo. 
@pessoa_bp.route('/pessoas/id/<int:pessoa_id>', methods=['PUT'])
def atualizar_pessoa_por_id(pessoa_id):
    try:
        # Obter os dados da solicitação JSON
        data = request.get_json()

        # Buscar a pessoa no banco de dados
        pessoa = Pessoa.query.get(pessoa_id)

        # Verificar se a pessoa foi encontrada
        if not pessoa:
            return jsonify({'error': 'Pessoa não encontrada.'}), 404

        # Imprimir os dados recebidos na requisição
        print(data)

        # Obter os nomes dos campos da instância Pessoa
        campos_validos = [column.key for column in Pessoa.__table__.columns]
    
        # Atualizar os campos no objeto pessoa
    
        for campo in campos_validos:
            if campo in data:
                novo_valor = data[campo]
                if campo == 'cpf':
                    if not validar_cpf(novo_valor):
                        return jsonify({'error': 'CPF inválido.'}), 400
                elif campo == 'data_nascimento':
                    if not validar_data_nascimento(novo_valor):
                        return jsonify({'error': 'Data de nascimento inválida. Use o formato YYYY-MM-DD.'}), 400
                    novo_valor = datetime.strptime(novo_valor, '%Y-%m-%d').date()
                elif campo == 'estado_civil':
                    if not validar_estado_civil(novo_valor):
                        return jsonify({'error': 'Estado civil inválido.'}), 400
        if(novo_valor):
            setattr(pessoa, campo, novo_valor)

            # Atualizar a instância no banco de dados
            atualizar_pessoa_db(pessoa)

            # Resposta de sucesso
            return jsonify({
                'id': pessoa.id,
                'nome_completo': pessoa.nome_completo,
                'data_nascimento': pessoa.data_nascimento.strftime('%Y-%m-%d'),
                'endereco': pessoa.endereco,
                'cpf': pessoa.cpf,
                'estado_civil': pessoa.estado_civil
            }), 200
        else : 
                return jsonify({'error': 'Requisição inválida. O objeto passado não possui nenhum campo válido. Ele precisa ter pelo menos um campo igual ao fornecido pelo objeto'}), 400

    except Exception as e:
        print(f'Erro ao atualizar pessoa por ID: {str(e)}')

        return jsonify({'error': f'Ocorreu um erro interno no servidor. Detalhes: {str(e)}'}), 500
