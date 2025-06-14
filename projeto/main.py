import os
from auxiliar import load_json, save_json, LISTAS_DE_EXERCICIOS_DIR, TURMAS_JSON_PATH, USUARIOS_JSON_PATH, PROGRESO_ALUNOS_JSON_PATH
from professor import cria_exercicio, cria_turma, insere_aluno, remove_aluno, visualiza_turma, passa_lista # Certifique-se de importar visualiza_turma
from cadastro import cria_usuario, entra_conta
from aluno import abrir_lista, revisar_lista

def setup_initial_environment():
    """
    Garante que os diretórios e arquivos JSON iniciais existam.
    Isso previne FileNotFoundError ao tentar ler ou escrever.
    """
    os.makedirs(LISTAS_DE_EXERCICIOS_DIR, exist_ok=True)
    
    load_json(TURMAS_JSON_PATH, {})
    load_json(USUARIOS_JSON_PATH, {})
    load_json(PROGRESO_ALUNOS_JSON_PATH, {})

def professor_menu():
    """Menu de opções para usuários do tipo 'professor'."""
    while True:
        print("\n--- Menu do Professor ---")
        print("1. Criar Exercício")
        print("2. Criar Turma")
        print("3. Inserir Aluno em Turma")
        print("4. Remover Aluno de Turma")
        print("5. Visualizar Turma e Desempenho") # Atualizado o nome da opção
        print("6. Passar Lista para Turma")
        print("7. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            nome_lista = input("Nome do arquivo da lista onde o exercício será adicionado (ex: matematica.json): ")
            lista_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_lista)
            exercicios_existente = load_json(lista_path, []) 
            
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
                
                try:
                    cria_exercicio(exercicios_existente, tema, enunciado, alternativas, nome_lista)
                    print(f"Exercício '{tema}' adicionado e lista '{nome_lista}' atualizada.")
                except ValueError as e:
                    print(f"Erro ao criar exercício: {e}.")
                
                continuar = input("Adicionar outro exercício a ESTA lista? (s/n): ").lower()
                if continuar != 's':
                    print(f"Finalizando a adição de exercícios à lista '{nome_lista}'.")
                    break

        elif choice == '2':
            nome_turma = input("Nome da nova turma: ")
            cria_turma(nome_turma)

        elif choice == '3':
            nome_turma = input("Nome da turma onde o aluno será inserido: ")
            matricula_aluno = input("Matrícula do aluno a ser inserido (7 dígitos): ")
            if matricula_aluno.isdigit():
                insere_aluno(nome_turma, int(matricula_aluno))
            else:
                print("Matrícula inválida. Por favor, digite apenas números.")
        
        elif choice == '4':
            nome_turma = input("Nome da turma de onde o aluno será removido: ")
            matricula_aluno = input("Matrícula do aluno a ser removido (7 dígitos): ")
            if matricula_aluno.isdigit():
                remove_aluno(nome_turma, int(matricula_aluno))
            else:
                print("Matrícula inválida. Por favor, digite apenas números.")

        elif choice == '5': # Opção para visualizar turma e desempenho
            turmas_data = load_json(TURMAS_JSON_PATH, {})
            print("\n--- Turmas Existentes ---")
            if turmas_data:
                for nome_turma_existente in turmas_data.keys():
                    print(f"- {nome_turma_existente}")
                nome_turma = input("Digite o nome da turma que deseja visualizar: ")
                visualiza_turma(nome_turma)
            else:
                print("Nenhuma turma criada ainda.")

        elif choice == '6':
            nome_lista = input("Nome do arquivo da lista de exercícios (ex: matematica_basica.json): ")
            nome_turma = input("Nome da turma para associar a lista: ")
            passa_lista(nome_lista, nome_turma)

        elif choice == '7':
            print("Saindo do menu do professor.")
            break
        else:
            print("Opção inválida. Tente novamente.")

def aluno_menu(matricula_aluno: int):
    """Menu de opções para usuários do tipo 'aluno'."""
    while True:
        print("\n--- Menu do Aluno ---")
        print("1. Abrir/Responder Lista de Exercícios")
        print("2. Revisar Listas Respondidas")
        print("3. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            abrir_lista(matricula_aluno)
        elif choice == '2':
            revisar_lista(matricula_aluno)
        elif choice == '3':
            print("Saindo do menu do aluno.")
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    """Função principal que inicia a aplicação."""
    setup_initial_environment()

    logged_in_user = None

    while logged_in_user is None:
        entra = input("Digite 'criar' para criar uma conta ou 'entrar' para acessar uma conta existente: ").lower()
        while entra not in ["criar", "entrar"]:
            entra = input("Comando não reconhecido. Digite 'criar' ou 'entrar': ").lower()

        if entra == "criar":
            logged_in_user = cria_usuario()
            if logged_in_user is None:
                continue

        elif entra == "entrar":
            matri = input("Digite sua matrícula: ")
            passw = input("Digite sua senha: ")
            logged_in_user = entra_conta(matri, passw)
    
    if logged_in_user:
        if logged_in_user['tipo'] == 'professor':
            professor_menu()
        elif logged_in_user['tipo'] == 'aluno':
            aluno_menu(logged_in_user['matricula']) 
        else:
            print("Tipo de usuário desconhecido.")

if __name__ == "__main__":
    main()