import os
import sys # Para sys.exit

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
    
    # Chama load_json para cada arquivo para garantir que existam (e sejam inicializados vazios)
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
                
                try:
                    professor.cria_exercicio(exercicios_existente, tema, enunciado, alternativas, nome_lista)
                    print(f"Exercício '{tema}' adicionado e lista '{nome_lista}' atualizada.")
                except ValueError as e:
                    print(f"Erro ao criar exercício: {e}.")
                
                continuar = input("Adicionar outro exercício a ESTA lista? (s/n): ").lower()
                if continuar != 's':
                    print(f"Finalizando a adição de exercícios à lista '{nome_lista}'.")
                    break

        elif choice == '2':
            nome_turma = input("Nome da nova turma: ")
            professor.cria_turma(nome_turma)

        elif choice == '3':
            nome_turma = input("Nome da turma onde o aluno será inserido: ")
            matricula_aluno = input("Matrícula do aluno a ser inserido (7 dígitos): ")
            if matricula_aluno.isdigit():
                professor.insere_aluno(nome_turma, int(matricula_aluno))
            else:
                print("Matrícula inválida. Por favor, digite apenas números.")
        
        elif choice == '4':
            nome_turma = input("Nome da turma de onde o aluno será removido: ")
            matricula_aluno = input("Matrícula do aluno a ser removido (7 dígitos): ")
            if matricula_aluno.isdigit():
                professor.remove_aluno(nome_turma, int(matricula_aluno))
            else:
                print("Matrícula inválida. Por favor, digite apenas números.")

        elif choice == '5':
            turmas_data = auxiliar.load_json(auxiliar.TURMAS_JSON_PATH, {})
            print("\n--- Turmas Existentes ---")
            if turmas_data:
                for nome_turma_existente in turmas_data.keys():
                    print(f"- {nome_turma_existente}")
                nome_turma = input("Digite o nome da turma que deseja visualizar: ")
                professor.visualiza_turma(nome_turma)
            else:
                print("Nenhuma turma criada ainda.")

        elif choice == '6':
            nome_lista = input("Nome do arquivo da lista de exercícios (ex: matematica_basica.json): ")
            nome_turma = input("Nome da turma para associar a lista: ")
            professor.passa_lista(nome_lista, nome_turma)

        elif choice == '7':
            print("Saindo do menu do professor.")
            break
        else:
            print("Opção inválida. Tente novamente.")

def aluno_menu(logged_in_user): # Recebe o usuário logado como argumento
    """Menu de opções para usuários do tipo 'aluno'."""
    while True:
        print("\n--- Menu do Aluno ---")
        print("1. Abrir/Responder Lista de Exercícios")
        print("2. Revisar Listas Respondidas")
        print("3. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            aluno.abrir_lista(logged_in_user['matricula']) # Usa a matrícula do usuário logado
        elif choice == '2':
            aluno.revisar_lista(logged_in_user['matricula']) # Usa a matrícula do usuário logado
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
            professor_menu(logged_in_user) # Passa o usuário logado para o menu do professor
        elif logged_in_user['tipo'] == 'aluno':
            aluno_menu(logged_in_user) # Passa o usuário logado para o menu do aluno
        else:
            print("Tipo de usuário desconhecido. Encerrando.")
            sys.exit(1)

if __name__ == "__main__":
    main()