class Viagem:
    def __init__(self, cpf, destino, inicio, fim, valor):
        self.cpf = cpf
        self.destino = destino
        self.inicio = inicio
        self.fim = fim
        self.valor = valor

    def linha_armazenamento(self):
        return f'V : {self.cpf} : {self.destino} : {self.inicio} : {self.fim} : {self.valor}'
