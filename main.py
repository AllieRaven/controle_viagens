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
from rich.table import Table

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
    
    #Torna o abrir e fechar do arquivo automático, deixando o código mais limpo.
    with open("agencia.txt", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(" : ")

            #Verifica se é Servidor
            if partes[0] == "S":
                _, cpf, nome, tel = partes
                dados[cpf] = Servidor(cpf, nome, tel)

            #Verifica se é Viagem
            elif partes[0] == "V":
                _, cpf, destino, inicio, fim, valor = partes
                viagens.append(
                    Viagem(cpf, destino, inicio, fim, float(valor)))
    return dados


def salvar_dados(dados):
    """
    Salva todos os servidores e viagens
    no arquivo agencia.txt.
    """

    with open("agencia.txt", "w", encoding="utf-8") as arquivo:
        for servidor in dados.values():
            arquivo.write(f"{servidor.linha_armazenamento()}\n")

        for viagem in viagens:
            arquivo.write(f"{viagem.linha_armazenamento()}\n")


def menu():
    while True:
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

        print("Opção inválida. Você deve escolher uma opção entre 1 e 6.")


def cadastrar_servidor(dados):
    print(Panel((":bust_in_silhouette: Cadastro de servidores"), expand=False))
    print()

    #Inicia a função

    #CPF
    while True:
        cpf = Prompt.ask("[bold] :page_facing_up: Digite o CPF (somente números): \n->[/bold]").strip()

        if not cpf: #Se é vazio
            print("[bold yellow]:warning: CPF é obrigatório. Tente novamente[/]")
        elif not cpf.isdigit() or len(cpf) != 11: #Se possui apenas números e a quantidade correta de digitos
            print("[bold yellow]:warning: CPF inválido. Tente novamente[/]")
        else:
            break

    nome = Prompt.ask("[bold] :bust_in_silhouette: Digite o nome: \n->[/bold]").strip()

    while not nome: #Se é vazio
        print("[bold yellow]:warning: Nome é obrigatório. Tente novamente[/]")
        nome = Prompt.ask("[bold] :bust_in_silhouette: Digite o nome: \n->[/bold]").strip()

    while True:
        tel = Prompt.ask("[bold] :telephone_receiver: Digite o telefone(DD NNNNNNNNN): \n ->[/bold]").strip().replace(" ","")

        if not tel.isdigit() or len(tel) != 11: #Se possui apenas números e a quantidade correta de digitos
            print("[bold yellow]:warning: Telefone inválido. Tente novamente[/]")
        else:
            break

    #Após todos os dados preenchidos ele checa se o servidor já está cadastrado
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
    #Se não tivereste cpf -> True
    return cpf not in dados


def validar_data(data):
    """
    Verifica se a data informada existe
    e está no formato dd/mm/aaaa.
    """

    #Valida se a data é valida
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

    #Valida se a data inicial vem antes da data final
    data_inicio = datetime.strptime(inicio, "%d/%m/%Y")
    data_fim = datetime.strptime(fim, "%d/%m/%Y")

    return data_fim > data_inicio


def adicionar_viagem(dados):

    print(Panel((":bust_in_silhouette: Cadastro de viagens"), expand=False))
    print()

    #Chama o cpf para a realização das pesquisas
    cpf = Prompt.ask("[bold]:page_facing_up: Digite o CPF (somente números):\n->[/]").strip()

    if cpf not in dados:
        return "[bold red]❌ Servidor não encontrado.[/]"
    
    while True:
        destino = Prompt.ask("[bold]:round_pushpin: Destino:\n->[/]").strip()
        if(destino == ""):
            print("[bold red]❌ O destino é obrigatório. [/]")
        else:
            break

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


def mascarar_cpf(cpf):
    return cpf[:3] + ".*.*-" + cpf[-2:]


def remover_viagem(dados):
    print(Panel((":bust_in_silhouette: Remoção de viagens"), expand=False))
    print()

    cpf = Prompt.ask(
        "[bold] :page_facing_up: Digite o CPF (somente números): \n ->[/bold]"
    ).strip()

    if cpf not in dados:
        return "[bold red]❌ Servidor não encontrado.[/]"

    if len(viagens) == 0:
        return "[bold yellow]:warning: Nenhuma viagem cadastrada.[/]"

    viagens_cpf = []

    #Adiciona as viagens relacionadas ao cpf informado em uma lista
    for i, viagem in enumerate(viagens):
        if viagem.cpf == cpf:
            viagens_cpf.append(i)

    if len(viagens_cpf) == 0:
        return "[bold yellow]:warning: Este servidor não possui viagens cadastradas.[/]"
    
    tabela = Table(title="Viagens do servidor")
    tabela.add_column("N°")
    tabela.add_column("Destino")
    tabela.add_column("Data de início")
    tabela.add_column("Data de fim")

    
    #Retorna os dados principais de cada viagem do servidor
    for i, indice in enumerate(viagens_cpf, start=1):
        viagem = viagens[indice]
        tabela.add_row(
            str(i),
            viagem.destino,
            viagem.inicio,
            viagem.fim)
        print(tabela)

    while True:
        try:
            #Usuário informa o índice 
            escolha = int(
                Prompt.ask("[bold]Informe o número da viagem: [/]")
            ) - 1

            if 0 <= escolha < len(viagens_cpf):
                indice_real = viagens_cpf[escolha]

                historico_remocoes.append(viagens[indice_real])
                viagens.pop(indice_real)

                return "[bold green]:white_check_mark: Viagem removida com sucesso! :wastebasket:[/]"

            else:
                print("[bold yellow]:warning: Número inválido.[/]")

        except ValueError:
            print("[bold yellow]:warning: Valor inválido![/]")


def listar_viagens():
    print(Panel(":bust_in_silhouette: Listar viagens", expand=False))
    print()

    if len(viagens) == 0:
        return "[bold yellow]:warning: Nenhuma viagem cadastrada.[/]"

    # Ordena por data
    ordenadas = sorted(
        viagens,
        key=lambda v: datetime.strptime(v.inicio, "%d/%m/%Y")
    )

    tabela = Table(title="Viagens cadastradas")

    tabela.add_column("CPF")
    tabela.add_column("Destino")
    tabela.add_column("Data de início")
    tabela.add_column("Data de fim")
    tabela.add_column("Valor das diárias")

    for viagem in ordenadas:
        tabela.add_row(
            mascarar_cpf(viagem.cpf),
            viagem.destino,
            viagem.inicio,
            viagem.fim,
            f"R$ {viagem.valor:.2f}"
        )

    return tabela


def buscar_viagens_cpf():
    print(Panel((":bust_in_silhouette: Buscar Viagens por Servidos: "), expand=False))
    print()
    cpf = Prompt.ask("[bold]:page_facing_up: Digite o cpf(apenas números): [/]").strip()
    texto = ""

    #Ordena as viagens por data
    ordenadas = sorted(
        viagens,
        key=lambda v: datetime.strptime(v.inicio, "%d/%m/%Y"))
    
    tabela = Table(title=f"Viagens do CPF {cpf}")

    tabela.add_column("Destino")
    tabela.add_column("Início")
    tabela.add_column("Fim")
    tabela.add_column("Valor diária")
    tabela.add_column("Total")

    encontrou = False

    for viagem in ordenadas:
        if viagem.cpf == cpf:
            tabela.add_row(
                viagem.destino,
                viagem.inicio,
                viagem.fim,
                f"R$ {viagem.valor:.2f}",
                f"R$ {float(total_diarias(viagem)):.2f}"
            )
            encontrou = True

    if encontrou:
        return tabela

    return "[bold red]:x: Nenhuma viagem encontrada para este CPF.[/]"


def total_diarias(viagem):
    #Função auxilair. 
    # As datas já são verificadas no momento do cadastro da viagem.
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
            print(remover_viagem(dados))

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