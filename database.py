import sqlite3
from datetime import datetime


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    def __init__(self, nome='biblioteca.db'):
        self.nome, self.conexao = nome, None

    def conectar(self):
        self.conexao = sqlite3.connect('biblioteca.db')
    
    def desconectar(self):
        try:
            self.conexao.close()
        except AttributeError:
            pass
    
    def criar_tabela_pessoas(self):
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pessoas(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(50) NOT NULL,
                    cpf VARCHAR(15) UNIQUE NOT NULL,
                    data_nascimento VARCHAR(10) NOT NULL,
                    multa FLOAT
                );
            """)
        except AttributeError:
            print('Impossível criar tabelas antes de conectar ao banco de dados!')
    
    def criar_tabela_livros(self):
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS livros(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT UNIQUE NOT NULL,
                    autor VARCHAR(50) NOT NULL,
                    editora TEXT NOT NULL,
                    ano INT NOT NULL,
                    quantidade INT NOT NULL
                );
            """)
        except AttributeError:
            print('Impossível criar tabelas antes de conectar ao banco de dados!')

    def criar_tabela_emprestimos(self):
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS emprestimos(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    data DATE NOT NULL,
                    id_pessoa INT,
                    id_livro INT,
                    situacao TEXT CHECK(situacao IN ('A', 'M', 'E')) NOT NULL DEFAULT 'A',
                    FOREIGN KEY (id_pessoa) REFERENCES pessoas(id),
                    FOREIGN KEY (id_livro) REFERENCES livros(id)
                );
            """)
        except AttributeError:
            print('Impossível criar tabelas antes de conectar ao banco de dados!')
    
    def criar_tabelas(self):
        self.criar_tabela_pessoas()
        self.criar_tabela_livros()
        self.criar_tabela_emprestimos()

    def inserir_pessoa(self, nome, cpf, data_nascimento, multa=0.0):
        try:
            cursor = self.conexao.cursor()
            try:
                cursor.execute("""
                    INSERT INTO pessoas (nome, cpf, data_nascimento, multa) VALUES (?, ?, ?, ?);
                """, (nome.title(), cpf, data_nascimento, multa))
                self.conexao.commit()
            except sqlite3.IntegrityError:
                print(f'O CPF {cpf} já foi registrado!')
        except AttributeError:
            print('Impossível adicionar registros antes de conectar ao banco de dados!')
    
    def buscar_pessoa(self, cpf):
        try:
            cursor = self.conexao.cursor()
            cursor.execute(f"""
                SELECT * FROM pessoas WHERE cpf=?;
            """, (cpf,))
            pessoa = cursor.fetchone()
            if pessoa:
                return pessoa
            else:
                return False
        except AttributeError:
            print('Impossível pesquisar usuário antes de conectar ao banco de dados!')

    def excluir_pessoa(self, cpf):
        try:
            cursor = self.conexao.cursor()
            cursor.execute(f"""
                DELETE FROM pessoas WHERE cpf=?;
            """, (cpf,))
        except AttributeError:
            print('Impossível excluir registro antes de conectar ao banco de dados!')

    def definir_multa(self, cpf, valor_multa):
        try:
            cursor = self.conexao.cursor()
            cursor.execute(f"""
                UPDATE pessoas
                SET multa=?
                WHERE cpf=?;
            """, (valor_multa, cpf))
            self.conexao.commit()
        except AttributeError:
            print('Impossível alterar registros antes de conectar ao banco de dados!')
        
    def inserir_livro(self, titulo, autor, editora, ano, quantidade):
        try:
            cursor = self.conexao.cursor()
            try:
                cursor.execute("""
                    INSERT INTO livros (titulo, autor, editora, ano, quantidade) VALUES (?, ?, ?, ?, ?);
                """, (titulo.title(), autor.title(), editora.title(), ano, quantidade))
                self.conexao.commit()
            except sqlite3.IntegrityError:
                print('Livro já existente na base de dados!')
        except AttributeError:
            print('Impossível adicionar registros antes de conectar ao banco de dados!')
        
    def buscar_livro(self, titulo):
        try:
            cursor = self.conexao.cursor()
            cursor.execute(f"""
                SELECT * FROM livros WHERE titulo=?;
            """, (titulo.title(),))
            livro = cursor.fetchone()
            if livro:
                return livro
            else:
                return False
        except AttributeError:
            print('Impossível pesquisar livro antes de conectar ao banco de dados!')
        
    def obter_quantidade_livros(self, titulo):
        try:
            cursor = self.conexao.cursor()
            cursor.execute(f"""
                SELECT quantidade FROM livros WHERE titulo=?;
            """, (titulo.title(),))
            quantidade = cursor.fetchone()
            if quantidade:
                return quantidade
            else:
                print('Livro não encontrado!')
        except AttributeError:
            print('Impossível pesquisar registro antes de conexar ao banco de dados!')
    
    def alterar_quantidade(self, titulo, quantidade):
        try:
            cursor = self.conexao.cursor()
            cursor.execute(f"""
                UPDATE livros
                SET quantidade=?
                WHERE titulo=?;
            """, (quantidade, titulo.title()))
            self.conexao.commit()
        except AttributeError:
            print('Impossível atualizar registro antes de conectar ao banco de dados!')
    
    def novo_emprestimo(self, cpf, titulo):
        try:
            data = datetime.now()
            data = data.strftime("%d/%m/%Y")
            id_pessoa = self.buscar_pessoa(cpf)[0]
            id_livro = self.buscar_livro(titulo.title())[0]
            cursor = self.conexao.cursor()
            cursor.execute("""
                INSERT INTO emprestimos (data, id_pessoa, id_livro, situacao) VALUES (?, ?, ?, ?);
            """, (data, id_pessoa, id_livro, 'A'))
            self.conexao.commit()
        except AttributeError:
            print('Impossível realizar empréstimo antes de conectar ao banco de dados!')

    def buscar_emprestimo(self, cpf):
        try:
            id_pessoa = self.buscar_pessoa(cpf)[0]
            cursor = self.conexao.cursor()
            cursor.execute(f"""
                SELECT e.id, e.data, e.situacao, p.nome, l.titulo, l.autor FROM emprestimos e
                JOIN pessoas p ON e.id_pessoa = p.id
                JOIN livros l ON e.id_livro = l.id
                WHERE e.id_pessoa = ?;
            """, (id_pessoa,))
            emprestimo = cursor.fetchone()
            if emprestimo:
                return emprestimo
            else:
                print('Empréstimo não localizado!')
        except AttributeError:
            print('Impossível consultar empréstimos antes de conectar ao banco de dados!')
    
    def alterar_situacao_emprestimo(self, id_emprestimo, situacao):
        try:
            cursor = self.conexao.cursor()
            cursor.execute(f"""
                UPDATE emprestimos
                SET situacao=?
                WHERE id=?;
            """, (situacao, id_emprestimo))
            self.conexao.commit()
        except AttributeError:
            print('Impossível atualizar registro antes de conectar ao banco de dados!')
