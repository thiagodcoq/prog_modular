entra = input("Digite 'criar' se quiser criar uma conta e 'entrar' se quiser entrar na sua conta já criada: ")

while entra != "criar" and entra != "entrar":
    entra = input("Comando não reconhecido, tente novamente: ")

"""
Sistema simples de cadastro e login de usuários com validações básicas.
Permite criação de conta para 'aluno' ou 'professor', além de login por matrícula e senha.
"""

def criaAluno():
    """
    Função que coleta dados de um novo usuário (aluno ou professor) via input,
    valida os dados inseridos (tipo, matrícula, idade e senha) e retorna um dicionário
    representando o novo usuário.

    Returns:
        dict: Dados do novo usuário com as chaves: 'matricula', 'nome', 'idade', 'tipo', 'senha'.
    """
    nome = input("Digite seu nome: ")

    tipo = input("Digite seu tipo (aluno ou professor): ")
    while tipo != "aluno" and tipo != "professor":
        tipo = input("Tipo não reconhecido, tente novamente: ")

    matr = input("Digite sua matrícula (7 dígitos): ")
    while not matr.isdigit() or int(matr) > 9999999 or int(matr) < 1000000:
        matr = input("Matrícula inválida, digite novamente (7 dígitos): ")
    
    idade = input("Digite sua idade: ")
    while not idade.isdigit() or int(idade) <= 0:
        idade = input("Idade inválida, digite novamente: ")

    pasw = input("Digite sua senha: ")
    pasc = input("Confirme sua senha: ")
    while pasw != pasc:
        pasw = input("Senha confirmada diferente da digitada, digite novamente: ")
        pasc = input("Confirme novamente: ")

    aluno = {
        'matricula': int(matr),
        'nome': nome,
        'idade': int(idade),
        'tipo': tipo,
        'senha': pasw
    }
    
    return aluno

def entra_conta(matr, senha):
    """
    Função que realiza o processo de login de um usuário.
    Solicita a senha até que seja correta ou informa se a matrícula não foi encontrada.

    Args:
        matr (str): Matrícula do usuário.
        senha (str): Senha digitada inicialmente.
    """
    matr = int(matr)
    encontrado = False

    for aluno in lista_alunos:
        if aluno['matricula'] == matr:
            encontrado = True
            while aluno['senha'] != senha:
                senha = input("Senha incorreta, tente novamente: ")
            print(f"Você entrou com sucesso, {aluno['nome']}!")
            return
    
    if not encontrado:
        print("Matrícula não encontrada.")

lista_alunos = [
    {'matricula': 20190202, 'nome': 'andré', 'idade': 20, 'tipo': 'aluno', 'senha': 'Dede2005'},
    {'matricula': 2014433, 'nome': 'flavio', 'idade': 22, 'tipo': 'professor', 'senha': 'flafla03'},
    {'matricula': 2015555, 'nome': 'ana', 'idade': 25, 'tipo': 'aluno', 'senha': 'aninha25'}
]

entra = input("Digite 'criar' se quiser criar uma conta e 'entrar' se quiser entrar na sua conta já criada: ")
while entra != "criar" and entra != "entrar":
    entra = input("Comando não reconhecido, tente novamente: ")

if entra == "criar":
    novo_aluno = criaAluno()
    lista_alunos.append(novo_aluno)
    print("Conta criada com sucesso!")
    print(lista_alunos)

if entra == "entrar":
    matri = input("Digite sua matrícula: ")
    passw = input("Digite sua senha: ")
    entra_conta(matri, passw)
