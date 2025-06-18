import os  # Importa o módulo 'os' para interagir com o sistema operacional (e.g., criar diretórios).
import sys # Importa o módulo 'sys' para funções relacionadas ao sistema, como 'sys.exit()' para encerrar o programa.

# Importa todas as funções e variáveis diretamente dos módulos auxiliares.
# Este é o padrão de organização para encapsulamento sem classes no fluxo principal:
# cada módulo é um serviço, e o 'main' orquestra chamadas e interações com o usuário.
import auxiliar
import cadastro
import professor
import aluno

def setup_initial_environment():
    """
    Objetivo: Garante que os diretórios e arquivos JSON essenciais para o funcionamento do sistema existam.
    Isso previne erros FileNotFoundError ao tentar ler ou escrever dados.

    Returns:
        None: A função não retorna valor, apenas configura o ambiente e imprime uma mensagem de confirmação.
    """
    # Cria o diretório base para as listas de exercícios, se ele já não existir.
    # O diretório 'json/' será criado implicitamente quando o primeiro arquivo for salvo lá,
    # mas garantir a pasta de listas_de_exercicios explicitamente é bom.
    os.makedirs(auxiliar.LISTAS_DE_EXERCICIOS_DIR, exist_ok=True)
    
    # Carrega (ou cria se não existirem) os arquivos JSON principais, inicializando-os vazios.
    # Isso garante que as funções subsequentes não encontrem erros ao tentar acessá-los.
    auxiliar.load_json(auxiliar.TURMAS_JSON_PATH, {})       # Garante que 'turmas.json' exista e seja um objeto vazio se novo.
    auxiliar.load_json(auxiliar.USUARIOS_JSON_PATH, {})     # Garante que 'usuarios.json' exista e seja um objeto vazio se novo.
    auxiliar.load_json(auxiliar.PROGRESO_ALUNOS_JSON_PATH, {}) # Garante que 'progresso_alunos.json' exista e seja um objeto vazio se novo.
    
    print("Ambiente de arquivos JSON configurado.")

def professor_menu(logged_in_user: dict):
    """
    Objetivo: Exibe o menu de opções para um usuário logado como 'professor' e gerencia suas interações.

    Args:
        logged_in_user (dict): O dicionário contendo os dados do professor atualmente logado.

    Returns:
        None: A função não retorna valor; o loop continua até o professor escolher sair.
    """
    while True: # Loop principal do menu do professor, que continua até o professor escolher sair.
        print("\n--- Menu do Professor ---")
        print("1. Criar Exercício")
        print("2. Criar Turma")
        print("3. Inserir Aluno em Turma")
        print("4. Remover Aluno de Turma")
        print("5. Visualizar Turma e Desempenho")
        print("6. Passar Lista para Turma")
        print("7. Sair")

        choice = input("Escolha uma opção: ") # Coleta a escolha do professor.

        if choice == '1': # Opção para criar um novo exercício.
            nome_lista = input("Nome do arquivo da lista onde o exercício será adicionado (ex: matematica.json): ")
            # Constrói o caminho completo para a lista de exercícios.
            lista_path = os.path.join(auxiliar.LISTAS_DE_EXERCICIOS_DIR, nome_lista)
            # Carrega a lista existente ou inicializa uma nova lista vazia se o arquivo não existir.
            exercicios_existente = auxiliar.load_json(lista_path, []) 
            
            while True: # Loop para permitir adicionar múltiplos exercícios à mesma lista.
                tema = input("Tema do exercício (ou digite 'sair' para finalizar): ")
                if tema.lower() == 'sair': # Condição para sair do loop de criação de exercícios.
                    print(f"Finalizando a adição de exercícios à lista '{nome_lista}'.")
                    break

                enunciado = input("Enunciado do exercício: ")
                alternativas = []
                for i in range(3): # Solicita 3 alternativas (A, B, C).
                    alt = input(f"Alternativa {chr(65+i)}: ")
                    alternativas.append(alt)
                
                # Exibe as alternativas novamente para que o professor possa escolher a correta.
                print("Alternativas disponíveis:")
                for i, alt in enumerate(alternativas):
                    print(f"{chr(65+i)}) {alt}")
                
                resposta_correta_letra = "" # Variável para armazenar a letra da resposta correta.
                while resposta_correta_letra not in ('A', 'B', 'C'): # Loop para validar a entrada da resposta correta.
                    resposta_correta_letra = input("Digite a letra da alternativa correta (A, B ou C): ").upper()
                    if resposta_correta_letra not in ('A', 'B', 'C'):
                        print("Opção inválida. Digite A, B ou C.")

                # Chama a função de criação de exercício do módulo 'professor', passando todos os dados coletados.
                # Esta função retorna um dicionário de status e mensagem.
                resultado = professor.cria_exercicio(exercicios_existente, tema, enunciado, alternativas, resposta_correta_letra, nome_lista)
                
                # Verifica o status retornado e imprime a mensagem apropriada para o usuário.
                if resultado["status"] == "sucesso":
                    print(resultado["mensagem"])
                else:
                    print(f"Erro ao criar exercício: {resultado['mensagem']}")
                
                # Pergunta se o professor deseja adicionar outro exercício à mesma lista.
                continuar = input("Adicionar outro exercício a ESTA lista? (s/n): ").lower()
                if continuar != 's':
                    print(f"Finalizando a adição de exercícios à lista '{nome_lista}'.")
                    break

        elif choice == '2': # Opção para criar uma nova turma.
            nome_turma = input("Nome da nova turma: ")
            # Chama a função de criação de turma do módulo 'professor' e imprime o resultado.
            resultado = professor.cria_turma(nome_turma)
            print(resultado["mensagem"])

        elif choice == '3': # Opção para inserir um aluno em uma turma.
            nome_turma = input("Nome da turma onde o aluno será inserido: ")
            matricula_aluno_str = input("Matrícula do aluno a ser inserido (7 dígitos): ")
            if matricula_aluno_str.isdigit(): # Valida se a matrícula é numérica.
                matricula_aluno = int(matricula_aluno_str)
                # Chama a função de inserção de aluno do módulo 'professor' e imprime o resultado.
                resultado = professor.insere_aluno(nome_turma, matricula_aluno)
                print(resultado["mensagem"])
            else:
                print("Matrícula inválida. Por favor, digite apenas números.")
        
        elif choice == '4': # Opção para remover um aluno de uma turma.
            nome_turma = input("Nome da turma de onde o aluno será removido: ")
            matricula_aluno_str = input("Matrícula do aluno a ser removido (7 dígitos): ")
            if matricula_aluno_str.isdigit(): # Valida se a matrícula é numérica.
                matricula_aluno = int(matricula_aluno_str)
                # Chama a função de remoção de aluno do módulo 'professor' e imprime o resultado.
                resultado = professor.remove_aluno(nome_turma, matricula_aluno)
                print(resultado["mensagem"])
            else:
                print("Matrícula inválida. Por favor, digite apenas números.")

        elif choice == '5': # Opção para visualizar detalhes de uma turma e desempenho.
            # Obtém e exibe as turmas existentes para sugerir ao professor.
            turmas_existentes = professor.get_turmas_existentes()
            print("\n--- Turmas Existentes ---")
            if turmas_existentes:
                for nome_turma_existente in turmas_existentes:
                    print(f"- {nome_turma_existente}")
            else:
                print("Nenhuma turma criada ainda.")

            nome_turma = input("Digite o nome da turma que deseja visualizar: ")
            # Chama a função de visualização de turma do módulo 'professor'.
            # Esta função retorna um dicionário com os detalhes da turma ou uma mensagem de erro.
            resultado = professor.visualiza_turma(nome_turma)
            
            # Formata e imprime os detalhes da turma com base no resultado.
            if resultado["status"] == "sucesso":
                print(f"\n--- Detalhes da Turma: {resultado['nome_turma']} ---")
                print("\nAlunos:")
                if resultado["alunos"]: # Verifica se há alunos para listar.
                    for aluno_detalhe in resultado["alunos"]:
                        print(f"- Matrícula: {aluno_detalhe['matricula']}, Nome: {aluno_detalhe['nome']}")
                else:
                    print("Nenhum aluno nesta turma.")

                print("\nListas de Exercícios Associadas:")
                if resultado["listas"]: # Verifica se há listas associadas para listar.
                    for lista_detalhe in resultado["listas"]:
                        print(f"\nLista: {lista_detalhe['nome_lista']}")
                        print(f"  Índice de Acerto da Turma: {lista_detalhe['indice_acerto']}")
                        print(f"  {lista_detalhe['msg_acerto']}") # Mensagem detalhada sobre os acertos.
                else:
                    print("Nenhuma lista de exercícios associada a esta turma.")
                print("-" * (len(nome_turma) + 20)) # Linha decorativa.
            else:
                print(resultado["mensagem"]) # Imprime mensagem de erro se a turma não for encontrada.

        elif choice == '6': # Opção para associar uma lista de exercícios a uma turma.
            # Obtém e exibe as turmas existentes para sugestão.
            turmas_existentes = professor.get_turmas_existentes()
            print("\n--- Turmas Existentes ---")
            if turmas_existentes:
                for nome_turma_existente in turmas_existentes:
                    print(f"- {nome_turma_existente}")
            else:
                print("Nenhuma turma encontrada. Crie uma turma primeiro.")
            
            nome_turma = input("Nome da turma para associar a lista: ")

            # Obtém e exibe as listas de exercícios existentes para sugestão.
            listas_existentes = professor.get_listas_existentes()
            print("\n--- Listas de Exercícios Existentes ---")
            if listas_existentes:
                for lista_nome in listas_existentes:
                    print(f"- {lista_nome}")
            else:
                print("Nenhuma lista de exercícios encontrada. Crie exercícios primeiro.")

            nome_lista = input("Nome do arquivo da lista de exercícios (ex: matematica_basica.json): ")
            
            # Chama a função de associar lista do módulo 'professor' e imprime o resultado.
            resultado = professor.passa_lista(nome_lista, nome_turma)
            print(resultado["mensagem"])

        elif choice == '7': # Opção para sair do menu do professor.
            print("Saindo do menu do professor.")
            break # Sai do loop do menu do professor.
        else:
            print("Opção inválida. Tente novamente.") # Mensagem para escolha inválida.

def aluno_menu(logged_in_user: dict):
    """
    Objetivo: Exibe o menu de opções para um usuário logado como 'aluno' e gerencia suas interações.

    Args:
        logged_in_user (dict): O dicionário contendo os dados do aluno atualmente logado.

    Returns:
        None: A função não retorna valor; o loop continua até o aluno escolher sair.
    """
    while True: # Loop principal do menu do aluno, que continua até o aluno escolher sair.
        print("\n--- Menu do Aluno ---")
        print("1. Abrir/Responder Lista de Exercícios")
        print("2. Revisar Listas Respondidas")
        print("3. Sair")

        choice = input("Escolha uma opção: ") # Coleta a escolha do aluno.

        if choice == '1': # Opção para abrir ou responder uma lista de exercícios.
            # Chama a função 'abrir_lista' do módulo 'aluno', passando a matrícula do aluno logado.
            aluno.abrir_lista(logged_in_user['matricula'])
        elif choice == '2': # Opção para revisar listas respondidas.
            # Chama a função 'revisar_lista' do módulo 'aluno', passando a matrícula do aluno logado.
            aluno.revisar_lista(logged_in_user['matricula'])
        elif choice == '3': # Opção para sair do menu do aluno.
            print("Saindo do menu do aluno.")
            break # Sai do loop do menu do aluno.
        else:
            print("Opção inválida. Tente novamente.") # Mensagem para escolha inválida.

def main():
    """
    Objetivo: Função principal do sistema. Gerencia o fluxo de criação de conta/login
              e direciona o usuário para o menu apropriado (professor ou aluno) após o login.

    Returns:
        None: A função não retorna valor; ela orquestra a execução do programa.
    """
    # Configura o ambiente inicial (cria pastas e arquivos JSON se necessário).
    setup_initial_environment()

    logged_in_user = None # Variável para armazenar os dados do usuário logado; inicialmente None.

    print("Bem-vindo ao Sistema Educacional!")

    # Loop para o processo de login ou criação de conta.
    # Continua até que um usuário seja logado com sucesso.
    while logged_in_user is None:
        entra = input("Digite 'criar' para criar uma conta ou 'entrar' para acessar uma conta existente: ").lower()
        while entra not in ["criar", "entrar"]: # Valida a entrada.
            entra = input("Comando não reconhecido. Digite 'criar' ou 'entrar': ").lower()

        if entra == "criar": # Se o usuário escolheu criar uma conta.
            logged_in_user = cadastro.cria_usuario() # Chama a função de criação de usuário.
            if logged_in_user is None: # Se a criação falhou (ex: matrícula duplicada), o loop continua.
                continue

        elif entra == "entrar": # Se o usuário escolheu entrar em uma conta existente.
            matri = input("Digite sua matrícula: ")
            passw = input("Digite sua senha: ")
            logged_in_user = cadastro.entra_conta(matri, passw) # Tenta logar o usuário.
        
    # Após o login bem-sucedido, verifica o tipo de usuário e direciona para o menu correspondente.
    if logged_in_user: # Verifica se logged_in_user não é None.
        if logged_in_user['tipo'] == 'professor':
            professor_menu(logged_in_user) # Chama o menu do professor, passando os dados do professor logado.
        elif logged_in_user['tipo'] == 'aluno':
            aluno_menu(logged_in_user) # Chama o menu do aluno, passando os dados do aluno logado.
        else: # Caso um tipo de usuário desconhecido seja encontrado (cenário improvável com validação).
            print("Tipo de usuário desconhecido. Encerrando.")
            sys.exit(1) # Encerra o programa com um código de erro.

if __name__ == "__main__":
    # Garante que a função 'main()' seja executada apenas quando o script for rodado diretamente,
    # e não quando for importado como um módulo em outro script (e.g., em testes).
    main()