import os
import sys

# Importa todas as funções diretamente dos módulos
import auxiliar
import cadastro
import professor
import aluno

def setup_initial_environment():
    """
    Garante que os diretórios e arquivos JSON iniciais existam.
    Isso previne FileNotFoundError ao tentar ler ou escrever.
    """
    os.makedirs(auxiliar.LISTAS_DE_EXERCICIOS_DIR, exist_ok=True)
    
    auxiliar.load_json(auxiliar.TURMAS_JSON_PATH, {})
    auxiliar.load_json(auxiliar.USUARIOS_JSON_PATH, {})
    auxiliar.load_json(auxiliar.PROGRESO_ALUNOS_JSON_PATH, {})
    print("Ambiente de arquivos JSON configurado.")

def professor_menu(logged_in_user):
    """Menu de opções para usuários do tipo 'professor'."""
    while True:
        print("\n--- Menu do Professor ---")
        print("1. Criar Exercício")
        print("2. Criar Turma")
        print("3. Inserir Aluno em Turma")
        print("4. Remover Aluno de Turma")
        print("5. Visualizar Turma e Desempenho")
        print("6. Passar Lista para Turma")
        print("7. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            nome_lista = input("Nome do arquivo da lista onde o exercício será adicionado (ex: matematica.json): ")
            lista_path = os.path.join(auxiliar.LISTAS_DE_EXERCICIOS_DIR, nome_lista)
            exercicios_existente = auxiliar.load_json(lista_path, []) 
            
            while True:
                tema = input("Tema do exercício (ou digite 'sair' para finalizar): ")
                if tema.lower() == 'sair':
                    print(f"Finalizando a adição de exercícios à lista '{nome_lista}'.")
                    break

                enunciado = input("Enunciado do exercício: ")
                alternativas = []
                for i in range(3): 
                    alt = input(f"Alternativa {chr(65+i)}: ")
                    alternativas.append(alt)
                
                # Exibir alternativas para o professor escolher a correta (agora no main.py)
                print("Alternativas disponíveis:")
                for i, alt in enumerate(alternativas):
                    print(f"{chr(65+i)}) {alt}")
                
                resposta_correta_letra = ""
                while resposta_correta_letra not in ('A', 'B', 'C'):
                    resposta_correta_letra = input("Digite a letra da alternativa correta (A, B ou C): ").upper()
                    if resposta_correta_letra not in ('A', 'B', 'C'):
                        print("Opção inválida. Digite A, B ou C.")

                # Chamar a função do professor com todos os dados coletados
                resultado = professor.cria_exercicio(exercicios_existente, tema, enunciado, alternativas, resposta_correta_letra, nome_lista)
                
                if resultado["status"] == "sucesso":
                    print(resultado["mensagem"])
                else:
                    print(f"Erro ao criar exercício: {resultado['mensagem']}")
                
                continuar = input("Adicionar outro exercício a ESTA lista? (s/n): ").lower()
                if continuar != 's':
                    print(f"Finalizando a adição de exercícios à lista '{nome_lista}'.")
                    break

        elif choice == '2':
            nome_turma = input("Nome da nova turma: ")
            resultado = professor.cria_turma(nome_turma)
            print(resultado["mensagem"])

        elif choice == '3':
            nome_turma = input("Nome da turma onde o aluno será inserido: ")
            matricula_aluno_str = input("Matrícula do aluno a ser inserido (7 dígitos): ")
            if matricula_aluno_str.isdigit():
                matricula_aluno = int(matricula_aluno_str)
                resultado = professor.insere_aluno(nome_turma, matricula_aluno)
                print(resultado["mensagem"])
            else:
                print("Matrícula inválida. Por favor, digite apenas números.")
        
        elif choice == '4':
            nome_turma = input("Nome da turma de onde o aluno será removido: ")
            matricula_aluno_str = input("Matrícula do aluno a ser removido (7 dígitos): ")
            if matricula_aluno_str.isdigit():
                matricula_aluno = int(matricula_aluno_str)
                resultado = professor.remove_aluno(nome_turma, matricula_aluno)
                print(resultado["mensagem"])
            else:
                print("Matrícula inválida. Por favor, digite apenas números.")

        elif choice == '5':
            # Obter e exibir turmas existentes para sugestão (agora no main.py)
            turmas_existentes = professor.get_turmas_existentes()
            print("\n--- Turmas Existentes ---")
            if turmas_existentes:
                for nome_turma_existente in turmas_existentes:
                    print(f"- {nome_turma_existente}")
            else:
                print("Nenhuma turma criada ainda.")

            nome_turma = input("Digite o nome da turma que deseja visualizar: ")
            resultado = professor.visualiza_turma(nome_turma)
            
            if resultado["status"] == "sucesso":
                print(f"\n--- Detalhes da Turma: {resultado['nome_turma']} ---")
                print("\nAlunos:")
                if resultado["alunos"]:
                    for aluno_detalhe in resultado["alunos"]:
                        print(f"- Matrícula: {aluno_detalhe['matricula']}, Nome: {aluno_detalhe['nome']}")
                else:
                    print("Nenhum aluno nesta turma.")

                print("\nListas de Exercícios Associadas:")
                if resultado["listas"]:
                    for lista_detalhe in resultado["listas"]:
                        print(f"\nLista: {lista_detalhe['nome_lista']}")
                        print(f"  Índice de Acerto da Turma: {lista_detalhe['indice_acerto']}")
                        print(f"  {lista_detalhe['msg_acerto']}")
                else:
                    print("Nenhuma lista de exercícios associada a esta turma.")
                print("-" * (len(nome_turma) + 20))
            else:
                print(resultado["mensagem"])

        elif choice == '6':
            # Obter e exibir turmas existentes para sugestão (agora no main.py)
            turmas_existentes = professor.get_turmas_existentes()
            print("\n--- Turmas Existentes ---")
            if turmas_existentes:
                for nome_turma_existente in turmas_existentes:
                    print(f"- {nome_turma_existente}")
            else:
                print("Nenhuma turma encontrada. Crie uma turma primeiro.")
            
            nome_turma = input("Nome da turma para associar a lista: ")

            # Obter e exibir listas existentes para sugestão (agora no main.py)
            listas_existentes = professor.get_listas_existentes()
            print("\n--- Listas de Exercícios Existentes ---")
            if listas_existentes:
                for lista_nome in listas_existentes:
                    print(f"- {lista_nome}")
            else:
                print("Nenhuma lista de exercícios encontrada. Crie exercícios primeiro.")

            nome_lista = input("Nome do arquivo da lista de exercícios (ex: matematica_basica.json): ")
            
            resultado = professor.passa_lista(nome_lista, nome_turma)
            print(resultado["mensagem"])

        elif choice == '7':
            print("Saindo do menu do professor.")
            break
        else:
            print("Opção inválida. Tente novamente.")

def aluno_menu(logged_in_user):
    """Menu de opções para usuários do tipo 'aluno'."""
    while True:
        print("\n--- Menu do Aluno ---")
        print("1. Abrir/Responder Lista de Exercícios")
        print("2. Revisar Listas Respondidas")
        print("3. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            aluno.abrir_lista(logged_in_user['matricula'])
        elif choice == '2':
            aluno.revisar_lista(logged_in_user['matricula'])
        elif choice == '3':
            print("Saindo do menu do aluno.")
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    """Função principal que inicia a execução do sistema."""
    setup_initial_environment()

    logged_in_user = None

    print("Bem-vindo ao Sistema Educacional!")

    while logged_in_user is None:
        entra = input("Digite 'criar' para criar uma conta ou 'entrar' para acessar uma conta existente: ").lower()
        while entra not in ["criar", "entrar"]:
            entra = input("Comando não reconhecido. Digite 'criar' ou 'entrar': ").lower()

        if entra == "criar":
            logged_in_user = cadastro.cria_usuario()
            if logged_in_user is None:
                continue

        elif entra == "entrar":
            matri = input("Digite sua matrícula: ")
            passw = input("Digite sua senha: ")
            logged_in_user = cadastro.entra_conta(matri, passw)
        
    if logged_in_user:
        if logged_in_user['tipo'] == 'professor':
            professor_menu(logged_in_user)
        elif logged_in_user['tipo'] == 'aluno':
            aluno_menu(logged_in_user)
        else:
            print("Tipo de usuário desconhecido. Encerrando.")
            sys.exit(1)

if __name__ == "__main__":
    main()