import unittest
from flask import Flask, jsonify
from app.models.pessoa import Pessoa
from app import create_app, db
from datetime import datetime

class TestPessoaRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()

        with self.app.app_context():
            # Crie o objeto pessoa_exemplo aqui e torne-o uma variável de instância
            self.pessoa_exemplo = Pessoa(
                nome_completo='Exemplo Pessoa',
                data_nascimento=datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
                endereco='Rua Exemplo, 123',
                cpf='123.456.789-09',
                estado_civil='Solteiro'
            )

            # Adicione ao banco de dados e faça o commit
            db.session.add(self.pessoa_exemplo)
            db.session.commit()

    

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_listar_pessoas(self):
        response = self.client.get('/pessoas')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('pessoas', data)
        self.assertIsInstance(data['pessoas'], list)
        # Adicione mais asserções conforme necessário para verificar o conteúdo da resposta.

    def test_obter_pessoa_por_cpf(self):
        response = self.client.get(f'/pessoas/{self.pessoa_exemplo.cpf}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Pessoa encontrada.')
        self.assertIn('nome_completo', data)
        # Adicione mais asserções conforme necessário para verificar o conteúdo da resposta.

    def test_obter_pessoa_por_id(self):
        response = self.client.get(f'/pessoas/id/{self.pessoa_exemplo.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Pessoa encontrada.')
        self.assertIn('nome_completo', data)
        # Adicione mais asserções conforme necessário para verificar o conteúdo da resposta.

    def test_deletar_pessoa_por_id(self):
        response = self.client.delete(f'/pessoas/delete/id/{self.pessoa_exemplo.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Pessoa deletada com sucesso.')
        # Adicione mais asserções conforme necessário para verificar o conteúdo da resposta.

    def test_deletar_pessoa_por_cpf(self):
        response = self.client.delete(f'/pessoas/delete/cpf/{self.pessoa_exemplo.cpf}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Pessoa deletada com sucesso.')
        # Adicione mais asserções conforme necessário para verificar o conteúdo da resposta.

if __name__ == '__main__':
    unittest.main()