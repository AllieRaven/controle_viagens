# Importação das bibliotecas utilizadas no sistema
from pathlib import Path
from datetime import datetime

# Importação das classes do projeto
from servidor import Servidor
from viagem import Viagem

# Biblioteca Rich para melhorar a interface do terminal
from rich.panel import Panel
from rich import print
from rich.prompt import Prompt

# Lista que armazena todas as viagens cadastradas
viagens = []

# Lista utilizada para guardar viagens removidas
historico_remocoes = []


def carregar_dados():
    """
    Lê o arquivo agencia.txt e recria os objetos
    Servidor e Viagem armazenados anteriormente.
    """
    dados = {}
    
    arquivo = Path("agencia.txt")
    
    # Caso o arquivo não exista, retorna um dicionário vazio
    if not arquivo.is_file():
        return dados
    
    arquivo = open("agencia.txt", "r", encoding="utf-8")
    for linha in arquivo:
        partes = linha.strip().split(" : ")

        # Registro de servidor
        if partes[0] == "S":
            _, cpf, nome, tel = partes
            dados[cpf] = Servidor(cpf, nome, tel)
        
        # Registro de viagem
        elif partes[0] == "V":
            _, cpf, destino, inicio, fim, valor = partes
            viagens.append(Viagem(cpf, destino, inicio, fim, float(valor)))
       
        
    arquivo.close()
    return dados


def salvar_dados(dados):
    """
    Salva todos os servidores e viagens
    no arquivo agencia.txt.
    """

    arquivo = open("agencia.txt", "w", encoding="utf-8")
    
    # Salva os servidores
    for servidor in dados.values():
        arquivo.write(f"{servidor.linha_armazenamento()}\n")
    
    # Salva as viagens
    for viagem in viagens:
        arquivo.write(f"{viagem.linha_armazenamento()}\n")

    arquivo.close()


def menu():
    """
    Exibe o menu principal e valida a opção escolhida.
    """

    print("\nAgência de viagens")
    print("[bold][1.] :bust_in_silhouette: Cadastro de servidores[/]")
    print("[bold][2.] :airplane_departure: Cadastro de viagens[/]")
    print("[bold][3.] :wastebasket: Remover viagem[/]")
    print("[bold][4.] :mag: Buscar viagem por servidor[/]")
    print("[bold][5.] :clipboard: Listar viagens[/]")
    print("[bold][6.] :door: Sair[/]\n")

    op = input("Escolha uma opção: ")

    if op.isdigit() and 1 <= int(op) <= 6: 
        return op
    else:
        print("Opção inválida. Você deve escolher uma opção entre 1 e 6.")
        return menu()


def cadastrar_servidor(dados):
    print(Panel((":bust_in_silhouette: Cadastro de servidores"), expand=False))
    print()
    while True:
        cpf = Prompt.ask("[bold] :page_facing_up: Digite o CPF (somente números): \n->[/bold]").strip()

        if not cpf:
            print("[bold yellow]:warning: CPF é obrigatório. Tente novamente[/]")
        elif not cpf.isdigit() or len(cpf) != 11:
            print("[bold yellow]:warning: CPF inválido. Tente novamente[/]")
        else:
            break

    nome = Prompt.ask("[bold] :bust_in_silhouette: Digite o nome: \n->[/bold]").strip()

    while not nome:
        print("[bold yellow]:warning: Nome é obrigatório. Tente novamente[/]")
        nome = Prompt.ask("[bold] :bust_in_silhouette: Digite o nome: \n->[/bold]").strip()

    while True:
        tel = Prompt.ask("[bold] :telephone_receiver: Digite o telefone(DD NNNNNNNNN): \n ->[/bold]").strip().replace(" ","")

        if not tel.isdigit() or len(tel) != 11:
            print("[bold yellow]:warning: Telefone inválido. Tente novamente[/]")
        else:
            break

    if validar_cpf(cpf, dados):
        dados[cpf] = Servidor(cpf, nome, tel)
        return "[bold green]:white_check_mark: Servidor cadastrado com sucesso![/]"
    else:
        return "[bold yellow]:warning: O Servidor já existe[/]"


def validar_cpf(cpf, dados):
    """
    Verifica se o CPF ainda não está cadastrado.
    Retorna True se estiver disponível.
    """

    return cpf not in dados


def validar_data(data):
    """
    Verifica se a data informada existe
    e está no formato dd/mm/aaaa.
    """

    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def periodo_valido(inicio, fim):
    """
    Verifica se a data final é posterior
    à data inicial da viagem.
    """

    data_inicio = datetime.strptime(inicio, "%d/%m/%Y")
    data_fim = datetime.strptime(fim, "%d/%m/%Y")

    return data_fim > data_inicio


def adicionar_viagem(dados):

    print(Panel((":bust_in_silhouette: Cadastro de viagens"), expand=False))
    print()

    cpf = Prompt.ask("[bold]:page_facing_up: Digite o CPF (somente números):\n->[/]").strip()

    if cpf not in dados:
        return "[bold red]❌ Servidor não encontrado.[/]"

    destino = Prompt.ask("[bold]:round_pushpin: Destino:\n->[/]").strip()

    while True:
        inicio = Prompt.ask("[bold]📅 Data de início (dd/mm/aaaa):\n->[/]").strip()
        fim = Prompt.ask("[bold]📅 Data de fim (dd/mm/aaaa):\n->[/]").strip()

        if not validar_data(inicio) or not validar_data(fim):
            print("[bold yellow]:warning: Data inválida.[/]")
            continue

        if not periodo_valido(inicio, fim):
            print("[bold yellow]:warning: A data final deve ser posterior à inicial.[/]")
            continue

        break

    while True:
        try:
            valor = float(Prompt.ask("[bold]💰 Valor das diárias:\n->[/]"))
            break
        except ValueError:
            print("[bold yellow]:warning: Digite um valor numérico válido.[/]")

    viagens.append(Viagem(cpf, destino, inicio, fim, valor))

    return "[bold green]:white_check_mark: Viagem cadastrada com sucesso![/]"


def remover_viagem():
    print(Panel((":bust_in_silhouette: Remoção de viagens"), expand=False))
    print()
    if len(viagens) == 0:
        return "[bold yellow] :warning: Nenhuma viagem cadastrada.[/]"

    for i, viagem in enumerate(viagens, start=1):
        print (
            f"{i} - [bold]:round_pushpin: Destino: {viagem.destino} | [/]"
            f"[bold]📅 Data de início:  {viagem.inicio} | [/]"
            f"[bold]📅 Data de fim: {viagem.fim} [/]"
        )

    while True:
        try:
            indice = int(input("[bold]Informe o número da viagem: [/]")) - 1

            if 0 <= indice < len(viagens):
                historico_remocoes.append(viagens[indice])
                viagens.pop(indice)
                print("[bold green]:white_check_mark: Viagem removida com sucesso! [/]")
                break

            else:
                print("[bold yellow]:warning: Número inválido.[/]")

        except ValueError:
            print("[bold yellow] :warning: Valor inválido![/]")
            continue


def listar_viagens():
    print(Panel((":bust_in_silhouette: Listar viagens"), expand=False))
    print()
    if len(viagens) == 0:
        return "[bold yellow] :warning: Nenhuma viagem cadastrada.[/]"

    ordenadas = sorted(
        viagens,
        key=lambda v: datetime.strptime(v.inicio, "%d/%m/%Y"))

    texto = ""

    for viagem in ordenadas:
        texto += (
            f"[bold]:page_facing_up: CPF:[/] {viagem.cpf} | "
            f"[bold]:round_pushpin: Destino:[/] {viagem.destino} | "
            f"[bold]📅 Data de início:[/]  {viagem.inicio} | "
            f"[bold]📅 Data de fim:[/] {viagem.fim} | "
            f"[bold]💰 Valor das diárias:[/] R$ {viagem.valor:.2f}"
            f"\n"
        )

    return texto


def buscar_viagens_cpf():
    print(Panel((":bust_in_silhouette: Buscar Viagens por Servidos: "), expand=False))
    print()
    cpf = input("Digite o cpf(apenas números): ").strip()
    texto = ""

    ordenadas = sorted(
        viagens,
        key=lambda v: datetime.strptime(v.inicio, "%d/%m/%Y"))

    for viagem in ordenadas:
        if viagem.cpf == cpf:
            texto += (f"[bold]:round_pushpin: Destino: {viagem.destino} | [/]"
                    f"[bold]📅 Data de início:  {viagem.inicio} | [/]"
                    f"[bold]📅 Data de fim: {viagem.fim} [/]"
                    f"[bold]💰 Valor das diárias: R${viagem.valor} [/] |"
                    f"[bold]💰 Valor total das diárias: R$ {total_diarias(viagem)} [/]"
                    f"\n"
            )

    if texto:
        return texto
    
    return "Nenhuma viagem encontrada para este CPF."


def total_diarias(viagem):
    inicio = datetime.strptime(viagem.inicio, "%d/%m/%Y")
    fim = datetime.strptime(viagem.fim, "%d/%m/%Y")

    dias = (fim - inicio).days + 1
    total = dias * viagem.valor

    return f"{total:.2f}"


# ==========================
# Programa principal
# ==========================

# Exibe o menu inicial
op = menu()

# Carrega os dados salvos no arquivo
dados = carregar_dados()

# Executa o sistema até o usuário escolher sair
while op != "6":

    # Seleciona a funcionalidade escolhida
    match op:

        # Cadastro de servidor
        case "1":
            print(cadastrar_servidor(dados))

        # Cadastro de viagem
        case "2":
            print(adicionar_viagem(dados))

        # Remoção de viagem
        case "3":
            print(remover_viagem())

        # Busca por CPF
        case "4":
            print(buscar_viagens_cpf())

        # Listagem de viagens
        case "5":
            print(listar_viagens())

    # Salva as alterações realizadas
    salvar_dados(dados)

    # Retorna ao menu principal
    op = menu()