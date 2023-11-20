import unittest
from flask import Flask
from flask.testing import FlaskClient
from app import create_app
from app.views.pessoa_view import pessoa_bp  # Importe o blueprint da sua aplicação
from app import db

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


if __name__ == '__main__':
    unittest.main()