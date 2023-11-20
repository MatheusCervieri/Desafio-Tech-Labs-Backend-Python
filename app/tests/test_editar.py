import unittest
from flask import Flask, jsonify
from app.models.pessoa import Pessoa
from app import create_app, db
from datetime import datetime



class TestAtualizarPessoa(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')  
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Crie o objeto pessoa_exemplo aqui e torne-o uma variável de instância
        self.pessoa_exemplo = Pessoa(
            nome_completo='Exemplo Pessoa',
            data_nascimento=datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
            endereco='Rua Exemplo, 123',
            cpf='123.456.789-09',
            estado_civil='Solteiro'
        )

        # Adicione ao banco de dados e faça o commit
        with self.app.app_context():
            db.session.add(self.pessoa_exemplo)
            db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    

    def test_atualizar_pessoa_por_id_sucesso(self):
        data = {
            'campo': 'endereco',
            'novo_valor': 'Nova Rua, 456'
        }

        response = self.client.put('/pessoas/edit/id/1', json=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)
        self.assertIn('id', response.json)
        self.assertIn('nome_completo', response.json)
        self.assertIn('data_nascimento', response.json)
        self.assertIn('endereco', response.json)
        self.assertIn('cpf', response.json)
        self.assertIn('estado_civil', response.json)
        self.assertEqual(response.json['endereco'], 'Nova Rua, 456')

    def test_atualizar_pessoa_por_cpf_sucesso(self):
        data = {
            'campo': 'estado_civil',
            'novo_valor': 'Casado'
        }

        response = self.client.put('/pessoas/edit/cpf/123.456.789-09', json=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)
        self.assertIn('id', response.json)
        self.assertIn('nome_completo', response.json)
        self.assertIn('data_nascimento', response.json)
        self.assertIn('endereco', response.json)
        self.assertIn('cpf', response.json)
        self.assertIn('estado_civil', response.json)
        self.assertEqual(response.json['estado_civil'], 'Casado')

    def test_campo_novo_valor_obrigatorio(self):
        data = {
            'campo': 'endereco'  # novo_valor não fornecido
        }

        response = self.client.put('/pessoas/edit/id/1', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Os campos "campo" e "novo_valor" são obrigatórios.')

    def test_pessoa_nao_encontrada(self):
        data = {
            'campo': 'endereco',
            'novo_valor': 'Nova Rua, 456'
        }

        response = self.client.put('/pessoas/edit/id/999', json=data)

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Pessoa não encontrada.')

    def test_campo_invalido(self):
        data = {
            'campo': 'email',  
            'novo_valor': 'exemplo@email.com'
        }

        response = self.client.put('/pessoas/edit/id/1', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'O campo email não é um atributo válido da entidade Pessoa.')

    def test_data_nascimento_invalida(self):
        data = {
            'campo': 'data_nascimento',
            'novo_valor': '01/01/1990'  
        }

        response = self.client.put('/pessoas/edit/id/1', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Data de nascimento inválida. Use o formato YYYY-MM-DD.')

if __name__ == '__main__':
    unittest.main()