import unittest
import os
import shutil
from backend.controller.contato_controller import ContatoController
from backend.models.contato import Contato

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Configurar ambiente de teste
        self.test_db_path = 'test_data/contatos.json'
        os.makedirs('test_data', exist_ok=True)
        
        # Inicializar controller com caminho de teste (hack para teste)
        self.controller = ContatoController()
        # Forçar o uso do arquivo de teste
        self.controller.db.data_file = self.test_db_path
        self.controller.db.contatos = []
        self.controller.db.ultimo_id = 0
        self.controller.db._salvar_dados()

    def tearDown(self):
        # Limpar ambiente de teste
        if os.path.exists('test_data'):
            shutil.rmtree('test_data')

    def test_fluxo_completo(self):
        # 1. Adicionar contato
        sucesso, msg = self.controller.criar_contato(
            nome_completo="Teste Silva",
            email="teste@exemplo.com",
            telefone="1199999999"
        )
        self.assertTrue(sucesso)
        self.assertIn("adicionado com sucesso", msg)

        # 2. Verificar se foi salvo
        contatos = self.controller.obter_todos_contatos()
        self.assertEqual(len(contatos), 1)
        self.assertEqual(contatos[0].nome_completo, "Teste Silva")
        self.assertEqual(contatos[0].email, "teste@exemplo.com")

        # 3. Buscar por nome
        resultados = self.controller.buscar_contatos_por_nome("Silva")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].nome_completo, "Teste Silva")

        # 4. Modificar contato
        contato_id = contatos[0].id
        sucesso, msg = self.controller.modificar_contato(
            contato_id, 
            telefone="1188888888"
        )
        self.assertTrue(sucesso)
        
        # Verificar modificação
        contato_atualizado = self.controller.obter_contato_por_id(contato_id)
        self.assertEqual(contato_atualizado.telefone, "1188888888")

        # 5. Remover contato
        sucesso, msg = self.controller.remover_contato(contato_id)
        self.assertTrue(sucesso)
        
        # Verificar remoção
        contatos_finais = self.controller.obter_todos_contatos()
        self.assertEqual(len(contatos_finais), 0)

if __name__ == '__main__':
    unittest.main()
