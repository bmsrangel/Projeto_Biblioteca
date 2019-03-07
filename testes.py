import unittest
from livro import Livro
from pessoa import Pessoa
from emprestimo import Emprestimo
from database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.db.conectar()
        self.db.criar_tabelas()
        self.db.desconectar()
    
    def test_00_inclusao_pessoa(self):
        self.db.conectar()
        # self.db.inserir_pessoa('Bruno Rangel', '1234', '17/02/1990')
        # self.db.inserir_pessoa('Edilania Silva', '5678', '25/10/1991')
        self.assertEqual((2, 'Edilania Silva', '5678', '25/10/1991', 0.0), self.db.buscar_pessoa('5678'))
        self.db.desconectar()
    
    def test_01_alterar_multa(self):
        self.db.conectar()
        self.db.definir_multa('1234', 3.0)
        self.assertEqual((1, 'Bruno Rangel', '1234', '17/02/1990', 3.0), self.db.buscar_pessoa('1234'))
        self.db.desconectar()

    def test_02_inclusao_livro(self):
        self.db.conectar()
        # self.db.inserir_livro('origem', 'dan brown', 'doubleday', 2017, 3)
        self.assertEqual((1, 'Origem', 'Dan Brown', 'Doubleday', 2017, 4), self.db.buscar_livro('origem'))
        self.db.desconectar()
    
    def test_03_alterar_quantidade_livros(self):
        self.db.conectar()
        self.db.alterar_quantidade('origem', 4)
        self.assertEqual((1, 'Origem', 'Dan Brown', 'Doubleday', 2017, 4), self.db.buscar_livro('origem'))
        self.db.desconectar()
    
    def test_04_novo_emprestimo(self):
        self.db.conectar()
        # self.db.novo_emprestimo('1234', 'origem')
        self.assertEqual((1, '06/03/2019', 'E', 'Bruno Rangel', 'Origem', 'Dan Brown'), self.db.buscar_emprestimo('1234'))
        self.db.desconectar()
    
    def test_05_alterar_situacao_emprestimo(self):
        self.db.conectar()
        self.db.alterar_situacao_emprestimo(1, 'E')
        self.assertEqual((1, '06/03/2019', 'E', 'Bruno Rangel', 'Origem', 'Dan Brown'), self.db.buscar_emprestimo('1234'))
        self.db.desconectar()


class TestPessoa(unittest.TestCase):
    def setUp(self):
        self.pessoa = Pessoa('Lidia Gandra', '1011', '15/04/1991')
    
    def test_00_cadastrarPessoa(self):
        # self.pessoa.cadastrar()
        # self.assertEqual(self.pessoa, Pessoa.consultar_pessoa('1011'))
        self.assertTrue(self.pessoa == Pessoa.consultar_pessoa('1011'))
    
    def test_01_multar(self):
        self.pessoa.multar(2.5)
        self.assertTrue(self.pessoa == Pessoa.consultar_pessoa('1011'))

    def test_02_pagar_multa(self):
        self.pessoa.pagar_multa()
        self.assertTrue(self.pessoa == Pessoa.consultar_pessoa('1011'))
    
    def test_03_pessoa_inexistente(self):
        self.assertFalse(Pessoa.consultar_pessoa('1213'))


class TestLivro(unittest.TestCase):
    def setUp(self):
        self.livro = Livro('A Cabana', 'William Young', 'Sextante', 2007, 10)
    
    def test_00_cadastrar_livro(self):
        # self.livro.cadastrar_livro()
        self.livro.quantidade = 8
        self.assertTrue(self.livro == Livro.consultar_livro('a cabana'))

    def test_01_alterar_quantidade_livro(self):
        self.livro.alterar_quantidade(8)
        self.assertTrue(self.livro == Livro.consultar_livro('a cabana'))

    def test_02_livro_inexistente(self):
        self.assertFalse(Livro.consultar_livro('madagascar'))


if __name__ == '__main__':
    unittest.main(verbosity=3)
