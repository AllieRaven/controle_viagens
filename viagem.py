from pathlib import Path
from servidor import Servidor

def carregar_dados():
    dados = {}
    
    arquivo = Path("agencia.txt")
    
    if not arquivo.is_file():
        return dados
    
    arquivo = open("agencia.txt", "r", encoding="utf-8")
    for linha in arquivo:
        cpf,nome,tel = linha.strip().split(" : ")
        dados[cpf] = Servidor(cpf,nome,tel)
       
        
    arquivo.close()
    return dados

def salvar_dados(dados):
    arquivo = open("agencia.txt", "w", encoding="utf-8")
    
    for servidor in dados:
        arquivo.write(f"{servidor.linha_armazenamento()}\n")
        
    arquivo.close()

def menu():
    print("Agencia de viagens")
    print("1. Cadastro de servidores")
    print("2. Cadastro de viagens")
    print("3. Remover viagem")
    print("4. Buscar viagem por servidor")
    print("5. Listar viagens")
    print("6. Sair")

    op = input("Opção: ")

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
        print("Todos os dados são obrigatórios. Tente novamente")
        return
    
    dados[cpf] = {
        "nome": nome,
        "telefone": tel
        }

    return "Servidor cadastrado com sucesso!"
    

    

    
#Programa principal
op = menu()

dados = carregar_dados()

while op != 6:
    match op:
        case "1":
            print(cadastrar_servidor(dados))
        case "2": 
            print("viagem")
        case "3":
            print("Remover")
        case "4":
            print("Buscar")
        case "5":
            print("Listar")
    
    op = menu()
    
salvar_dados(dados)