"""
Gerenciador de Senhas

Este programa permite ao usuário gerar senhas aleatórias, armazená-las em um banco de dados MongoDB,
visualizar senhas salvas, deletar senhas e atualizar senhas existentes. O programa utiliza dois módulos:
- gerencias_senha.py: Contém a classe Senha para gerar senhas aleatórias e realizar hash.
- db_controller.py: Contém a classe DbController para controlar as operações no banco de dados.

Autor: Pedro H Macedo Corrêa e Castro
Data de Criação: 2023-09-27
"""

from gerenciar_senha import Senha as gs
from db_controller import DbController as dc
import os

# Constante
DB_CONTROLLER = dc("mongodb://localhost:27017/", "pessoal", "senhas")

def gerar_senha() -> None:
    """
    Gera uma nova senha e a salva no banco de dados MongoDB.

    Solicita informações ao usuário, como o serviço, usuário, tamanho da senha
    e se deseja salvar a senha com hash. Em seguida, gera a senha, opcionalmente
    gera o hash e a salva no banco de dados MongoDB.

    Returns:
        None
    """
    os.system("cls")  # Limpa a tela do console

    # Solicita informações ao usuário
    servico = input("Para qual serviço gostaria de gerar uma senha?\n")
    usuario = input("Qual o usuário do serviço?\n")
    tamanho_senha = input("Qual o tamanho da senha que gostaria de gerar?\n")
    hash_ = input("Deseja salvar a senha com hash? [S/N] (O padrão é NÃO)")

    # Gerando senha
    senha = gs.gerar_senha(tamanho_senha)

    # Gerando hash se necessário
    salt = None
    if hash_.upper() == "S":
        salt, senha = gs.gerar_hash(senha)

    # Objeto/Dicionário para salvar no MongoDB
    obj = {
        "serviço": servico,
        "usuário": usuario,
        "senha": senha,
    }

    if hash_.upper() == "S":
        obj["salt"] = salt

    # Salvando no banco de dados
    resultado = DB_CONTROLLER.salvar(obj)
    print("Senha gerada e salva com sucesso!")
    input("Pressione Enter para continuar...")

def ver_senha() -> None:
    """
    Exibe senhas salvas no banco de dados MongoDB.

    Permite ao usuário selecionar um serviço e exibe as senhas salvas
    correspondentes a esse serviço.

    Returns:
        None
    """
    os.system("cls")  # Limpa a tela do console

    # Busca os serviços no banco de dados
    resultados = DB_CONTROLLER.find()
    servicos = set([resultado.get('serviço') for resultado in resultados])

    if not servicos:
        print("Nenhuma senha encontrada.")
        input("Pressione Enter para continuar...")
        return

    print("Serviços disponíveis:")
    for i, servico in enumerate(servicos, start=1):
        print(f"{i}. {servico}")

    escolha = input("Escolha o número do serviço para ver a senha correspondente: ")

    try:
        escolha = int(escolha)
        if escolha < 1 or escolha > len(servicos):
            print("Escolha inválida. Tente novamente.")
            input("Pressione Enter para continuar...")
        else:
            servico_escolhido = list(servicos)[escolha - 1]
            os.system("cls")  # Limpa a tela do console

            # Busca a senha no banco de dados com base no serviço escolhido
            resultado = DB_CONTROLLER.find(servico=servico_escolhido)
            if resultado:
                print("Senhas Salvas:")
                print("-" * 40)
                for senha in resultado:
                    print(f"Serviço: {senha.get('serviço')}")
                    print(f"Usuário: {senha.get('usuário')}")
                    print(f"Senha: {senha.get('senha')}")
                    # print(f"Salt: {senha.get('salt')}")
                    print("-" * 40)
                input("Pressione Enter para continuar...")
            else:
                print("Nenhuma senha encontrada para o serviço escolhido.")
                input("Pressione Enter para continuar.")

    except ValueError:
        print("Escolha inválida. Tente novamente.")
        input("Pressione Enter para continuar...")

def deletar_senha() -> None:
    """
    Exclui senhas salvas no banco de dados MongoDB.

    Permite ao usuário escolher uma senha da lista de senhas disponíveis
    e confirmar a exclusão.

    Returns:
        None
    """
    os.system("cls")  # Limpa a tela do console
    resultados = DB_CONTROLLER.find()
    
    if not resultados:
        print("Nenhuma senha encontrada.")
        input("Pressione Enter para continuar...")
        return

    print("Senhas disponíveis:")
    for i, resultado in enumerate(resultados, start=1):
        servico = resultado.get('serviço')
        usuario = resultado.get('usuário')
        print(f"{i}. Serviço: {servico}, Usuário: {usuario}")

    escolha = input("Escolha o número da senha que deseja deletar: ")

    try:
        escolha = int(escolha)
        if escolha < 1 or escolha > len(resultados):
            print("Escolha inválida. Tente novamente.")
            input("Pressione Enter para continuar...")
        else:
            os.system("cls")  # Limpa a tela do console
            senha_a_deletar = resultados[escolha - 1]
            servico = senha_a_deletar.get('serviço')
            usuario = senha_a_deletar.get('usuário')

            # Exibe os dados da senha selecionada
            print("Senha selecionada para deletar:")
            print(f"Serviço: {servico}")
            print(f"Usuário: {usuario}")

            c = input("Confirma os dados a serem deletados? [S/N]: ")
            if c.upper() == 'S':
                # Deleta a senha
                DB_CONTROLLER.delete(servico, usuario)
                
            else:
                print("Senha não deletada.")

            input("Pressione Enter para continuar...")

    except ValueError:
        print("Escolha inválida. Tente novamente.")
        input("Pressione Enter para continuar...")

def atualizar_senha() -> None:
    """
    Atualiza a senha de um serviço e usuário no banco de dados MongoDB.

    Permite ao usuário escolher uma senha da lista de senhas disponíveis,
    gerar uma nova senha e atualizar a senha existente.

    Returns:
        None
    """
    os.system("cls")  # Limpa a tela do console
    resultados = DB_CONTROLLER.find()
    
    if not resultados:
        print("Nenhuma senha encontrada.")
        input("Pressione Enter para continuar...")
        return

    print("Senhas disponíveis:")
    for i, resultado in enumerate(resultados, start=1):
        servico = resultado.get('serviço')
        usuario = resultado.get('usuário')
        print(f"{i}. Serviço: {servico}, Usuário: {usuario}")

    escolha = input("Escolha o número da senha que deseja alterar: ")

    try:
        escolha = int(escolha)
        if escolha < 1 or escolha > len(resultados):
            print("Escolha inválida. Tente novamente.")
            input("Pressione Enter para continuar...")
        else:
            os.system("cls")  # Limpa a tela do console
            senha_a_alterar = resultados[escolha - 1]
            servico = senha_a_alterar.get('serviço')
            usuario = senha_a_alterar.get('usuário')

            # Exibe os dados da senha selecionada
            print("Senha selecionada para alterar:")
            print(f"Serviço: {servico}")
            print(f"Usuário: {usuario}")

            c = input("Confirma os dados a serem alterados? [S/N]: ")
            if c.upper() == 'S':
                # Altera a senha
                tamanho_senha = int(input("Qual o tamanho da senha que gostaria de gerar?\n"))
                senha = gs.gerar_senha(tamanho_senha)
                os.system("cls")
                DB_CONTROLLER.update_password(servico, usuario, senha)
            else:
                print("Senha não alterada.")

            input("Pressione Enter para continuar...")

    except ValueError:
        print("Escolha inválida. Tente novamente.")
        input("Pressione Enter para continuar...")

def main():
    """
    Função principal que exibe um menu de opções para o usuário.

    O usuário pode escolher entre gerar uma nova senha, ver senhas salvas,
    deletar senha, atualizar senha ou sair do programa.

    Returns:
        None
    """
    opcoes = {
        "1": gerar_senha,
        "2": ver_senha,
        "3": deletar_senha,
        "4": atualizar_senha,
        "5": exit
    }

    while True:
        os.system("cls")  # Limpa a tela do console
        print("Gerenciador de Senhas")
        print("Menu de Opções:")
        print("1. Gerar nova senha")
        print("2. Ver senhas salvas")
        print("3. Deletar senha")
        print("4. Atualizar senha")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha in opcoes:
            opcoes[escolha]()
            if escolha == "5":
                break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
