class Servidor:
    def __init__ (self, cpf, nome, tel):
        self.nome = nome
        self.cpf = cpf
        self.tel = tel
    
    def linha_armazenamento (self):
        return f'S : {self.cpf} : {self.nome} : {self.tel}'
