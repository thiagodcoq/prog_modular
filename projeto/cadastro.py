import os
from auxiliar import load_json, save_json, USUARIOS_JSON_PATH

def cria_usuario() -> dict:
    """
    Função que coleta dados do usuário para criar uma nova conta e a salva em um JSON.
    Retorna o dicionário do usuário criado ou None se a criação falhar (ex: matrícula duplicada).
    """
    usuarios_data = load_json(USUARIOS_JSON_PATH, {})

    nome = input("Digite seu nome: ")

    tipo = input("Digite seu tipo (aluno ou professor): ").lower()
    while tipo not in ["aluno", "professor"]:
        tipo = input("Tipo não reconhecido, digite 'aluno' ou 'professor': ").lower()

    matr = input("Digite sua matrícula (7 dígitos): ")
    while not matr.isdigit() or not (1000000 <= int(matr) <= 9999999):
        matr = input("Matrícula inválida. Digite novamente (7 dígitos numéricos): ")

    if matr in usuarios_data:
        print(f"Uma conta com a matrícula {matr} já existe. Por favor, escolha outra ou entre com a existente.")
        return None

    idade = input("Digite sua idade: ")
    while not idade.isdigit() or int(idade) <= 0:
        idade = input("Idade inválida, digite novamente: ")
    
    pasw = input("Digite sua senha: ")
    pasc = input("Confirme sua senha: ")

    while pasw != pasc:
        print("Senha confirmada diferente da digitada.")
        pasw = input("Digite sua senha novamente: ")
        pasc = input("Confirme novamente: ")

    novo_usuario = {
        'matricula': int(matr),
        'nome': nome,
        'idade': int(idade),
        'tipo': tipo,
        'senha': pasw
    }
    
    usuarios_data[matr] = novo_usuario
    save_json(usuarios_data, USUARIOS_JSON_PATH)
    print("Conta criada com sucesso!")
    return novo_usuario

def entra_conta(matricula_str: str, senha_digitada: str) -> dict:
    """
    Função para fazer login. Verifica a matrícula e senha e retorna os dados do usuário logado.
    Retorna o dicionário do usuário logado ou None se o login falhar.
    """
    usuarios_data = load_json(USUARIOS_JSON_PATH, {})
    
    if matricula_str not in usuarios_data:
        print("Matrícula não encontrada.")
        return None

    usuario = usuarios_data[matricula_str]

    if usuario['senha'] != senha_digitada:
        print("Senha incorreta.")
        return None
    
    print(f"Você entrou com sucesso, {usuario['nome']}!")
    return usuario