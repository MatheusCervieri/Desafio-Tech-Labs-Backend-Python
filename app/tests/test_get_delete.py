import unittest
from flask import Flask, jsonify
from app.models.pessoa import Pessoa
from app import create_app, db
from datetime import datetime

import unittest
from flask import Flask, jsonify
from app.models.pessoa import Pessoa
from app import create_app, db
from datetime import datetime

class TestGetDeletePessoa(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')  
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.pessoa_exemplo = Pessoa(
            nome_completo='Exemplo Pessoa',
            data_nascimento=datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
            endereco='Rua Exemplo, 123',
            cpf='123.456.789-09',
            estado_civil='Solteiro'
        )


        with self.app.app_context():
            db.create_all()
            db.session.add(self.pessoa_exemplo)
            db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_listar_pessoas(self):
        response = self.client.get('/pessoas')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('pessoas', data)
        self.assertTrue(len(data['pessoas']) > 0)

    def test_obter_pessoa_por_id(self):
        pessoa_id = 1
        response = self.client.get(f'/pessoas/id/{pessoa_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Pessoa encontrada.')

    def test_deletar_pessoa_por_id(self):
        with self.app.app_context():
            pessoa_id = 1
            response = self.client.delete(f'/pessoas/delete/id/{pessoa_id}')
            data = response.get_json()

            self.assertIn(response.status_code, [200, 404, 500])

            if response.status_code == 200:
                self.assertIn('message', data)
                self.assertEqual(data['message'], 'Pessoa deletada com sucesso.')
            elif response.status_code == 404:
                self.assertIn('error', data)
                self.assertEqual(data['error'], 'Pessoa não encontrada.')
            elif response.status_code == 500:
                self.assertIn('error', data)
                self.assertEqual(data['error'], 'Erro ao deletar pessoa.')

if __name__ == '__main__':
    unittest.main()