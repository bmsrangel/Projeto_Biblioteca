from database import Database

class Pessoa:
    def __init__(self, nome, cpf, data_nascimento, multa=0.0):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.multa = multa
        self.db = Database()
    
    def cadastrar(self):
        self.db.conectar()
        self.db.inserir_pessoa(self.nome, self.cpf, self.data_nascimento)
        self.db.desconectar()
    
    def excluir_pessoa(self):
        self.db.conectar()
        self.db.excluir_pessoa(self.cpf)
        self.db.desconectar()

    def multar(self, valor_multa):
        self.multa = valor_multa
        self.db.conectar()
        self.db.definir_multa(self.cpf, self.multa)
        self.db.desconectar()
    
    def pagar_multa(self):
        self.db.conectar()
        self.multa = 0.0
        self.db.definir_multa(self.cpf, self.multa)
        self.db.desconectar()

    def consultar_pessoa(cpf):
        db = Database()
        db.conectar()
        pessoa = db.buscar_pessoa(cpf)
        db.desconectar()
        if pessoa:
            obj_pessoa = Pessoa(pessoa[1], pessoa[2], pessoa[3], pessoa[4])
            return obj_pessoa
        return False

    def __repr__(self):
        return (f'Nome: {self.nome}\nCPF: {self.cpf}\nData de nascimento: {self.data_nascimento}')
        
    def __eq__(self, obj):
        return self.__dict__ == obj.__dict__
