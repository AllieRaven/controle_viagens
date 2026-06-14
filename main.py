from pathlib import Path
from datetime import datetime
from servidor import Servidor
from viagem import Viagem


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
    print("7. Sair")

    op = input("Escolha uma opção: ")

    if op.isdigit() and 1 <= int(op) <= 6: 
        return op
    else:
        print("Opção inválida. Você deve escolher uma opção entre 1 e 5.")
        return menu()


def cadastrar_servidor(dados):
    while True:
        cpf = input("Digite o CPF (somente números): ").strip()

        if not cpf:
            print("CPF obrigatório.")
        elif not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido. Digite exatamente 11 números.")
        elif not validar_cpf(cpf, dados):
            print("O servidor já existe.")
        else:
            break

    nome = input("Digite o nome: ").strip()

    while not nome:
        print("Nome obrigatório.")
        nome = input("Digite o nome: ").strip()

    while True:
        tel = input("Digite o telefone: ").strip()

        if not tel.isdigit() or len(tel) != 11:
            print("Telefone inválido.")
        else:
            break

    dados[cpf] = Servidor(cpf, nome, tel)
    return "Servidor cadastrado com sucesso!"

def validar_cpf(cpf, dados):
    return cpf not in dados
    

def adicionar_viagem(dados):
    while True:
        cpf = input("CPF do servidor: ").strip()
        if cpf not in dados:
            return "Servidor não encontrado."
        else:
            break

    destino = input("Destino: ").strip()
    inicio = input("Data de início: ").strip()
    fim = input("Data de fim: ").strip()

    while True:
        try:
            valor = float(input("Valor da diária: ").strip())
            break
        except ValueError:
            print("Digite um valor numérico válido.")

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

    ordenadas = sorted(
        viagens,
        key=lambda v: datetime.strptime(v.inicio, "%d/%m/%Y")
    )

    texto = ""

    for viagem in ordenadas:
        texto += (
            f"CPF: {viagem.cpf} | "
            f"Destino: {viagem.destino} | "
            f"Início: {viagem.inicio} | "
            f"Fim: {viagem.fim} | "
            f"Valor: R$ {viagem.valor:.2f}\n"
        )

    return texto


def buscar_viagens_cpf():
    cpf = input("Digite o cpf(apenas números): ").strip()
    encontrou = False

    for viagem in viagens:
        if validar_cpf == cpf:
            return(f"Destino: {viagem.destino} | "
                    f"Início: {viagem.inicio} | "
                    f"Fim: {viagem.fim} | "
                    f"Valor: {viagem.valor}"
                    f"{total_diarias(cpf)}"
            )
            encontrou = True
    
    if not encontrou:
        return "Nenhuma viagem encontrada para este CPF."


def total_diarias(cpf):
    total = 0

    for viagem in viagens:
        if viagem.cpf == cpf:
            inicio = datetime.strptime(viagem.inicio, "%d/%m/%Y")
            fim = datetime.strptime(viagem.fim, "%d/%m/%Y")

            dias = (fim - inicio).days
            total += dias * viagem.valor

    return f"Total de diárias: R$ {total:.2f}"


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
            print(buscar_viagens_cpf())
        case "5":
            print(listar_viagens())
    op = menu()
    
salvar_dados(dados)
