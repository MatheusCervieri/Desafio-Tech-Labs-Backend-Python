import unittest
from flask import Flask
from flask.testing import FlaskClient
from app import create_app
from app.views.pessoa_view import pessoa_bp  
from app import db

#python -m unittest ./app/tests/test_cadastrar.py

class TestCadastroPessoa(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')  
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        self.app_context.pop()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_cadastro_pessoa_sucesso(self):
        data = {
            'nome_completo': 'Fulano de Tal',
            'data_nascimento': '1990-01-01',
            'endereco': 'Rua Teste, 123',
            'cpf': '123.456.789-09',
            'estado_civil': 'Solteiro'
        }

        response = self.client.post('/pessoas/adicionar', json=data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.json)
    def test_campos_obrigatorios(self):
        data = {
            'data_nascimento': '1990-01-01',
            'endereco': 'Rua Teste, 123',
            'cpf': '123.456.789-09',
            'estado_civil': 'Solteiro'
        }

        response = self.client.post('/pessoas/adicionar', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'O campo nome_completo é obrigatório.')

    def test_cpf_invalido(self):
        data = {
            'nome_completo': 'Fulano de Tal',
            'data_nascimento': '1990-01-01',
            'endereco': 'Rua Teste, 123',
            'cpf': '123.456.789',  
            'estado_civil': 'Solteiro'
        }

        response = self.client.post('/pessoas/adicionar', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'CPF inválido.')

    def test_data_nascimento_invalida(self):
        data = {
            'nome_completo': 'Fulano de Tal',
            'data_nascimento': '01/01/1990',  
            'endereco': 'Rua Teste, 123',
            'cpf': '123.456.789-09',
            'estado_civil': 'Solteiro'
        }

        response = self.client.post('/pessoas/adicionar', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Data de nascimento inválida. Use o formato YYYY-MM-DD.')

    def test_estado_civil_invalido(self):
        data = {
            'nome_completo': 'Fulano de Tal',
            'data_nascimento': '1990-01-01',
            'endereco': 'Rua Teste, 123',
            'cpf': '123.456.789-09',
            'estado_civil': 'gjhggj',  
        }

        response = self.client.post('/pessoas/adicionar', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Estado civil inválido.')

    def test_cadastro_sucesso(self):
        data = {
            'nome_completo': 'Fulano de Tal',
            'data_nascimento': '1990-01-01',
            'endereco': 'Rua Teste, 123',
            'cpf': '123.456.789-09',
            'estado_civil': 'Solteiro'
        }

        response = self.client.post('/pessoas/adicionar', json=data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.json)
        self.assertIn('id', response.json)
        self.assertIn('nome_completo', response.json)
        self.assertIn('data_nascimento', response.json)
        self.assertIn('endereco', response.json)
        self.assertIn('cpf', response.json)
        self.assertIn('estado_civil', response.json)

if __name__ == '__main__':
    unittest.main()