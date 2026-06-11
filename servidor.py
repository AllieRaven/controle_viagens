class Servidor:
    def __init__ (self, cpf, nome, tel):
        self.nome = nome
        self.cpf = cpf
        self.tel = tel
        
    def __str__ (self):
        return f'{self.cpf}: {self.nome}, {self.tel}'
    
    def linha_armazenamento (self):
        return f'{self.cpf} : {self.nome} : {self.tel}'