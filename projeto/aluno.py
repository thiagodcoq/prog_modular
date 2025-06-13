import json

def abrir_lista():
    try:
        #falta as especificações
        # Lê o arquivo JSON com as listas de exercícios
        with open('listas.json', 'r', encoding='utf-8') as arquivo:
            listas = json.load(arquivo)

        if not listas:
            print("Nenhuma lista de exercícios disponível.")
            return

        # Exibe os títulos das listas disponíveis
        print("Listas de Exercício Disponíveis:")
        for idx, lista in enumerate(listas, start=1):
            print(f"{idx} - {lista['titulo']}")

        # Solicita escolha do aluno
        escolha = int(input("Digite o número da lista que deseja abrir: "))
        if 1 <= escolha <= len(listas):
            lista_escolhida = listas[escolha - 1]
            print(f"\nAbrindo: {lista_escolhida['titulo']}")
            print("Exercícios:")
            for ex in lista_escolhida['exercicios']:
                print(f"- {ex}")
        else:
            print("Opção inválida.")

    except FileNotFoundError:
        print("Arquivo 'listas.json' não encontrado.")
    except json.JSONDecodeError:
        print("Erro ao ler o arquivo JSON.")
    except ValueError:
        print("Entrada inválida. Digite um número válido.")


 
    
    