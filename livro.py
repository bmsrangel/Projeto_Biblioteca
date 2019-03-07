from database import Database


class Livro:
    def __init__(self, titulo, autor, editora, ano, quantidade):
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.ano = ano
        self.quantidade = quantidade
        self.db = Database()

    def cadastrar_livro(self):
        self.db.conectar()
        self.db.inserir_livro(self.titulo, self.autor, self.editora, self.ano, self.quantidade)
        self.db.desconectar()
    
    def consultar_livro(titulo):
        db = Database()
        db.conectar()
        livro = db.buscar_livro(titulo.title())
        db.desconectar()
        if livro:
            obj_livro = Livro(livro[1], livro[2], livro[3], livro[4], livro[5])
            return obj_livro
        return False
    
    def alterar_quantidade(self, quantidade):
        self.quantidade = quantidade
        self.db.conectar()
        self.db.alterar_quantidade(self.titulo, self.quantidade)
        self.db.desconectar()

    def __repr__(self):
        return f'Titulo: {self.titulo}\nAutor: {self.autor}\nEditora: {self.editora}\nAno: {self.ano}'
        
    def __eq__(self, obj):
        return self.__dict__ == obj.__dict__