import os  # Importa o módulo 'os' para interagir com o sistema operacional, embora não seja diretamente usado aqui, é comum em projetos que lidam com arquivos.
from auxiliar import load_json, save_json, USUARIOS_JSON_PATH # Importa funções e variáveis do módulo auxiliar para lidar com arquivos JSON.

def cria_usuario() -> dict:
    """
    Função que coleta dados do usuário para criar uma nova conta e a salva em um JSON.

    Esta função guia o usuário através do processo de criação de uma conta, solicitando
    informações como nome, tipo (aluno/professor), matrícula, idade e senha.
    Ela valida algumas entradas e verifica a unicidade da matrícula.

    Returns:
        dict: O dicionário contendo os dados do usuário recém-criado,
              ou None se a criação da conta falhar (por exemplo, matrícula já existente).
    """
    # Carrega todos os dados de usuários existentes do arquivo JSON.
    # Se o arquivo não existir ou estiver vazio, retorna um dicionário vazio como padrão.
    usuarios_data = load_json(USUARIOS_JSON_PATH, {})

    # Solicita o nome do usuário. Não há validação específica para o nome.
    nome = input("Digite seu nome: ")

    # Solicita o tipo de usuário e converte para minúsculas para padronização.
    # Entra em um loop até que um tipo válido ('aluno' ou 'professor') seja inserido.
    tipo = input("Digite seu tipo (aluno ou professor): ").lower()
    while tipo not in ["aluno", "professor"]:
        tipo = input("Tipo não reconhecido, digite 'aluno' ou 'professor': ").lower()

    # Solicita a matrícula do usuário.
    # Valida se a matrícula é composta apenas por dígitos e se possui 7 dígitos (entre 1.000.000 e 9.999.999).
    matr = input("Digite sua matrícula (7 dígitos): ")
    while not matr.isdigit() or not (1000000 <= int(matr) <= 9999999):
        matr = input("Matrícula inválida. Digite novamente (7 dígitos numéricos): ")

    # Verifica se a matrícula inserida já existe nos dados dos usuários carregados.
    # Se sim, informa o usuário e retorna None, impedindo a criação de uma conta duplicada.
    if matr in usuarios_data:
        print(f"Uma conta com a matrícula {matr} já existe. Por favor, escolha outra ou entre com a existente.")
        return None

    # Solicita a idade do usuário.
    # Valida se a idade é um número e se é maior que zero.
    idade = input("Digite sua idade: ")
    while not idade.isdigit() or int(idade) <= 0:
        idade = input("Idade inválida, digite novamente: ")
    
    # Solicita a senha e a confirmação da senha.
    # Entra em um loop até que a senha digitada e a senha de confirmação sejam idênticas.
    pasw = input("Digite sua senha: ")
    pasc = input("Confirme sua senha: ")
    while pasw != pasc:
        print("Senha confirmada diferente da digitada.")
        pasw = input("Digite sua senha novamente: ")
        pasc = input("Confirme novamente: ")

    # Cria um dicionário com os dados do novo usuário.
    # A matrícula é armazenada como um inteiro dentro do dicionário para uso posterior (ex: aluno_menu).
    novo_usuario = {
        'matricula': int(matr),
        'nome': nome,
        'idade': int(idade),
        'tipo': tipo,
        'senha': pasw
    }
    
    # Adiciona o novo usuário ao dicionário de todos os usuários, usando a matrícula (como string) como chave.
    usuarios_data[matr] = novo_usuario
    # Salva os dados de todos os usuários (incluindo o novo) de volta no arquivo JSON.
    save_json(usuarios_data, USUARIOS_JSON_PATH)
    # Informa o usuário sobre o sucesso da criação da conta.
    print("Conta criada com sucesso!")
    # Retorna o dicionário do novo usuário.
    return novo_usuario

def entra_conta(matricula_str: str, senha_digitada: str) -> dict:
    """
    Função para fazer login.

    Esta função tenta autenticar um usuário verificando a matrícula e a senha fornecidas.
    Ela carrega os dados de usuários e compara as credenciais.

    Args:
        matricula_str (str): A matrícula digitada pelo usuário (como string).
        senha_digitada (str): A senha digitada pelo usuário.

    Returns:
        dict: O dicionário contendo os dados do usuário logado,
              ou None se a matrícula não for encontrada ou a senha estiver incorreta.
    """
    # Carrega todos os dados de usuários existentes do arquivo JSON.
    usuarios_data = load_json(USUARIOS_JSON_PATH, {})
    
    # Verifica se a matrícula fornecida existe como uma chave no dicionário de usuários.
    # Se não existir, informa e retorna None.
    if matricula_str not in usuarios_data:
        print("Matrícula não encontrada.")
        return None

    # Recupera o dicionário de dados do usuário correspondente à matrícula.
    usuario = usuarios_data[matricula_str]

    # Compara a senha digitada com a senha armazenada para o usuário.
    # Se as senhas não coincidirem, informa e retorna None.
    if usuario['senha'] != senha_digitada:
        print("Senha incorreta.")
        return None
    
    # Se a matrícula e a senha estiverem corretas, informa o sucesso do login.
    print(f"Você entrou com sucesso, {usuario['nome']}!")
    # Retorna o dicionário de dados do usuário logado.
    return usuario