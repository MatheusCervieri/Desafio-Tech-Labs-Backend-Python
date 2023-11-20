from flask import Blueprint, request, jsonify
from app.controllers.pessoa_controller import cadastrar_pessoa , atualizar_db , deletar_pessoa_db
from app.views.validation_utils import validar_cpf, validar_data_nascimento , validar_estado_civil
from app.models.pessoa import Pessoa
from app import logger


pessoa_bp = Blueprint('pessoa', __name__)


@pessoa_bp.route('/pessoas/adicionar', methods=['POST'])
def cadastrar():
    try:
        data = request.get_json()

        required_fields = ['nome_completo', 'data_nascimento', 'endereco', 'cpf', 'estado_civil']
        for field in required_fields:
            if field not in data or not data[field]:
                error_message = f'O campo {field} é obrigatório.'
                logger.error(error_message)
                return jsonify({'error': error_message}), 400

    
        if not validar_cpf(data['cpf']):
            error_message = 'CPF inválido.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400

        if not validar_data_nascimento(data['data_nascimento']):
            error_message = 'Data de nascimento inválida. Use o formato YYYY-MM-DD.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400
        
        if not validar_estado_civil(data['estado_civil']):
            error_message = 'Estado civil inválido.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400

       
        if Pessoa.query.filter_by(cpf=data['cpf']).first():
            error_message = 'CPF já cadastrado.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400


        nome_completo = data['nome_completo']
        data_nascimento = data['data_nascimento']
        endereco = data['endereco']
        cpf = data['cpf']
        estado_civil = data['estado_civil']


        nova_pessoa = cadastrar_pessoa(
            nome_completo=nome_completo,
            data_nascimento=data_nascimento,
            endereco=endereco,
            cpf=cpf,
            estado_civil=estado_civil
        )

        logger.info('Pessoa cadastrada com sucesso.')
        return jsonify({
            'message': 'Pessoa cadastrada com sucesso.',
            'id': nova_pessoa.id,
            'nome_completo': nova_pessoa.nome_completo,
            'data_nascimento': nova_pessoa.data_nascimento,
            'endereco': nova_pessoa.endereco,
            'cpf': nova_pessoa.cpf,
            'estado_civil': nova_pessoa.estado_civil
        }), 201  


    except Exception as e:
        logger.error(f'Erro no cadastro de pessoa: {str(e)}')
        return jsonify({'error': 'Ocorreu um erro interno no servidor. Tente novamente mais tarde.'}), 500
    

@pessoa_bp.route('/pessoas/edit/id/<int:pessoa_id>', methods=['PUT'])
def atualizar_pessoa_por_id(pessoa_id):
    try:
  
        data = request.get_json()

       
        if 'campo' not in data or not data['campo'] or 'novo_valor' not in data or not data['novo_valor']:
            error_message = 'Os campos "campo" e "novo_valor" são obrigatórios.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400


        pessoa = Pessoa.query.get(pessoa_id)

       
        if not pessoa:
            error_message = 'Pessoa não encontrada.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 404

        campo = data.get('campo')
        novo_valor = data.get('novo_valor')

      
        if not hasattr(pessoa, campo):
            error_message = f'O campo {campo} não é um atributo válido da entidade Pessoa.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400

        
        if campo == 'data_nascimento' and not validar_data_nascimento(novo_valor):
            error_message = 'Data de nascimento inválida. Use o formato YYYY-MM-DD.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400
        elif campo == 'estado_civil' and not validar_estado_civil(novo_valor):
            error_message = 'Estado civil inválido.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400
        elif campo == 'cpf' and not validar_cpf(novo_valor):
            error_message = 'CPF inválido.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400

        
        setattr(pessoa, campo, novo_valor)

        
        atualizar_db()

        success_response = {
            'message': 'Pessoa atualizada com sucesso.',
            'id': pessoa.id,
            'nome_completo': pessoa.nome_completo,
            'data_nascimento': pessoa.data_nascimento.strftime('%Y-%m-%d'),
            'endereco': pessoa.endereco,
            'cpf': pessoa.cpf,
            'estado_civil': pessoa.estado_civil
        }
        logger.info('Pessoa atualizada com sucesso.')
        return jsonify(success_response), 200

    except Exception as e:
        error_message = f'Ocorreu um erro interno no servidor. Detalhes: {str(e)}'
        logger.error(f'Erro ao atualizar pessoa por ID: {str(e)}')
        return jsonify({'error': error_message}), 500


@pessoa_bp.route('/pessoas/edit/cpf/<string:pessoa_cpf>', methods=['PUT'])
def atualizar_pessoa_por_cpf(pessoa_cpf):
    try:
        data = request.get_json()

        if 'campo' not in data or not data['campo'] or 'novo_valor' not in data or not data['novo_valor']:
            error_message = 'Os campos "campo" e "novo_valor" são obrigatórios.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400

     
        pessoa = Pessoa.query.filter_by(cpf=pessoa_cpf).first()

  
        if not pessoa:
            error_message = 'Pessoa não encontrada.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 404

    
        campo = data.get('campo')
        novo_valor = data.get('novo_valor')

   
        if not hasattr(pessoa, campo):
            error_message = f'O campo {campo} não é um atributo válido da entidade Pessoa.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400

   
        if campo == 'data_nascimento' and not validar_data_nascimento(novo_valor):
            error_message = 'Data de nascimento inválida. Use o formato YYYY-MM-DD.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400
        elif campo == 'estado_civil' and not validar_estado_civil(novo_valor):
            error_message = 'Estado civil inválido.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400
        elif campo == 'cpf' and not validar_cpf(novo_valor):
            error_message = 'CPF inválido.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400

        
        setattr(pessoa, campo, novo_valor)

     
        atualizar_db()

        success_response = {
            'message': 'Pessoa atualizada com sucesso.',
            'id': pessoa.id,
            'nome_completo': pessoa.nome_completo,
            'data_nascimento': pessoa.data_nascimento.strftime('%Y-%m-%d'),
            'endereco': pessoa.endereco,
            'cpf': pessoa.cpf,
            'estado_civil': pessoa.estado_civil
        }
        logger.info('Pessoa atualizada com sucesso.')
        return jsonify(success_response), 200

    except Exception as e:
        error_message = f'Ocorreu um erro interno no servidor. Detalhes: {str(e)}'
        logger.error(f'Erro ao atualizar pessoa por CPF: {str(e)}')
        return jsonify({'error': error_message}), 500

@pessoa_bp.route('/pessoas', methods=['GET'])
def listar_pessoas():
    try:
        pessoas = Pessoa.query.all()
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
        return jsonify({'pessoas': pessoas_info}), 200
    except Exception as e:
        logger.error(f'Erro ao listar pessoas: {str(e)}')
        return jsonify({'error': f'Ocorreu um erro interno no servidor. Detalhes: {str(e)}'}), 500

@pessoa_bp.route('/pessoas/<string:cpf>', methods=['GET'])
def obter_pessoa_por_cpf(cpf):
    try:
        if not validar_cpf(cpf):
            error_message = 'CPF inválido.'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400
        pessoa = Pessoa.query.filter_by(cpf=cpf).first()
        if pessoa:
            return jsonify({
                'message': 'Pessoa encontrada.',
                'id': pessoa.id,
                'nome_completo': pessoa.nome_completo,
                'data_nascimento': pessoa.data_nascimento.strftime('%Y-%m-%d'),
                'endereco': pessoa.endereco,
                'cpf': pessoa.cpf,
                'estado_civil': pessoa.estado_civil
            })
        else:
            logger.error("Pessoa não encontrada.")
            return jsonify({'error': 'Pessoa não encontrada.'}), 404
    except Exception as e:
        logger.error(f'Erro ao obter pessoa por CPF: {str(e)}')
        return jsonify({'error': f'Ocorreu um erro interno no servidor. Detalhes: {str(e)}'}), 500

@pessoa_bp.route('/pessoas/id/<int:pessoa_id>', methods=['GET'])
def obter_pessoa_por_id(pessoa_id):
    try:
        pessoa = Pessoa.query.get(pessoa_id)
        if pessoa:
            return jsonify({
                'message': 'Pessoa encontrada.',
                'id': pessoa.id,
                'nome_completo': pessoa.nome_completo,
                'data_nascimento': pessoa.data_nascimento.strftime('%Y-%m-%d'),
                'endereco': pessoa.endereco,
                'cpf': pessoa.cpf,
                'estado_civil': pessoa.estado_civil
            })
        else:
            logger.error('Pessoa não encontrada ou id inválido.')
            return jsonify({'error': 'Pessoa não encontrada.'}), 404
    except Exception as e:
        logger.error(f'Erro ao obter pessoa por ID: {str(e)}')
        return jsonify({'error': f'Ocorreu um erro interno no servidor. Detalhes: {str(e)}'}), 500

@pessoa_bp.route('/pessoas/delete/id/<int:pessoa_id>', methods=['DELETE'])
def deletar_pessoa_por_id(pessoa_id):
    try:
        pessoa = Pessoa.query.get(pessoa_id)
        if pessoa:
            if deletar_pessoa_db(pessoa):  
                logger.info('Pessoa deletada com sucesso.')
                return jsonify({'message': 'Pessoa deletada com sucesso.'}), 200
            else:
                logger.error('Erro ao deletar pessoa.')
                return jsonify({'error': 'Erro ao deletar pessoa.'}), 500
        else:
            logger.error('Pessoa não encontrada.')
            return jsonify({'error': 'Pessoa não encontrada.'}), 404
    except Exception as e:
        logger.error(f'Erro ao deletar pessoa por ID: {str(e)}')
        return jsonify({'error': f'Ocorreu um erro interno no servidor. Detalhes: {str(e)}'}), 500

@pessoa_bp.route('/pessoas/delete/cpf/<string:cpf>', methods=['DELETE'])
def deletar_pessoa_por_cpf(cpf):
    try:
        pessoa = Pessoa.query.filter_by(cpf=cpf).first()
        if pessoa:
            if deletar_pessoa_db(pessoa): 
                logger.info('Pessoa deletada com sucesso.')
                return jsonify({'message': 'Pessoa deletada com sucesso.'}), 200
            else:
                logger.error('Erro ao deletar pessoa.')
                return jsonify({'error': 'Erro ao deletar pessoa.'}), 500
        else:
            logger.error('Pessoa não encontrada.')
            return jsonify({'error': 'Pessoa não encontrada.'}), 404
    except Exception as e:
        logger.error(f'Erro ao deletar pessoa por CPF: {str(e)}')
        return jsonify({'error': f'Ocorreu um erro interno no servidor. Detalhes: {str(e)}'}), 500
