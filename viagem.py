from pathlib import Path
from servidor import Servidor
from viagemDados import Viagem

viagens = []
historico_remocoes = []

def carregar_dados():
    dados = {}
    
    arquivo = Path("agencia.txt")
    
    if not arquivo.is_file():
        return dados
    
    arquivo = open("agencia.txt", "r", encoding="utf-8")
    for linha in arquivo:
        partes = linha.strip().split(" : ")

        if partes[0] == "S":
            _, cpf, nome, tel = partes
            dados[cpf] = Servidor(cpf, nome, tel)

        elif partes[0] == "V":
            _, cpf, destino, inicio, fim, valor = partes
            viagens.append(Viagem(cpf, destino, inicio, fim, float(valor)))
       
        
    arquivo.close()
    return dados

def salvar_dados(dados):
    arquivo = open("agencia.txt", "w", encoding="utf-8")
    
    for servidor in dados.values():
        arquivo.write(f"{servidor.linha_armazenamento()}\n")
        
    for viagem in viagens:
        arquivo.write(f"V : {viagem.linha_armazenamento()}\n")

    arquivo.close()

def menu():
    print("\nAgência de viagens")
    print("1. Cadastro de servidores")
    print("2. Cadastro de viagens")
    print("3. Remover viagem")
    print("4. Buscar viagem por servidor")
    print("5. Listar viagens")
    print("6. Sair")

    op = input("Escolha uma opção: ")

    if op.isdigit() and 1 <= int(op) <= 6: 
        return op
    else:
        print("Opção inválida. Você deve escolher uma opção entre 1 e 5.")
        return menu()

def cadastrar_servidor(dados):   
    cpf = input("Digite o CPF (somente números): ").strip()
    nome = input("Digite o nome: ").strip()
    tel = input("Digite o telefone: ").strip()


    if nome == "" or tel == "" or cpf == "":
        return "Todos os dados são obrigatórios. Tente novamente"
        
    if validar_cpf(cpf, dados):
        dados[cpf] = Servidor(cpf, nome, tel)

        return "Servidor cadastrado com sucesso!"
    else:
        return "O Servidor já existe"
    
def validar_cpf(cpf, dados):
    return cpf not in dados
    

def adicionar_viagem(dados):
    cpf = input("CPF do servidor: ").strip()

    if cpf not in dados:
        return "Servidor não encontrado."

    destino = input("Destino: ").strip()
    inicio = input("Data de início: ").strip()
    fim = input("Data de fim: ").strip()
    valor = float(input("Valor das diárias: ").strip())

    viagens.append(Viagem(cpf, destino, inicio, fim, valor))

    return "Viagem cadastrada com sucesso."


def remover_viagem():
    if len(viagens) == 0:
        return "Nenhuma viagem cadastrada."

    for i, viagem in enumerate(viagens, start=1):
        print (
            f"{i} - Destino: {viagem.destino} | "
            f"Data de início: {viagem.inicio} | "
            f"Data de fim: {viagem.fim}"
        )

    indice = int(input("Informe o número da viagem: ")) - 1

    if 0 <= indice < len(viagens):
        historico_remocoes.append(viagens[indice])
        viagens.pop(indice)
        return "Viagem removida com sucesso."

    return "Índice inválido."


def listar_viagens():
    
    if len(viagens) == 0:
        return "Nenhuma viagem cadastrada."

    texto = ""

    for indice, viagem in enumerate(viagens, start=1):
        texto += (
            f"{indice}. CPF: {viagem.cpf} | "
            f"Destino: {viagem.destino} | "
            f"Período: {viagem.inicio} até {viagem.fim} | "
            f"Valor: {viagem.valor}\n"
        )

    return texto

    
#Programa principal
op = menu()

dados = carregar_dados()

while op != "6":
    match op:
        case "1":
            print(cadastrar_servidor(dados))
        case "2": 
            print(adicionar_viagem(dados))
        case "3":
            print(remover_viagem())
        case "4":
            print("Buscar")
        case "5":
            print(listar_viagens())

    op = menu()
    
salvar_dados(dados)
