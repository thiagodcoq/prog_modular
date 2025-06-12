entra = input("Digite 'criar' se quiser criar uma conta e 'entrar' se quiser entrar na sua conta já criada: ")

while entra != "criar" and entra != "entrar":
    entra = input("Comando não reconhecido, tente novamente: ")

def criaAluno():
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

lista_alunos = [
    {'matricula': 20190202, 'nome': 'andré', 'idade': 20, 'tipo': 'aluno', 'senha': 'Dede2005'},
    {'matricula': 2014433, 'nome': 'flavio', 'idade': 22, 'tipo': 'professor', 'senha': 'flafla03'},
    {'matricula': 2015555, 'nome': 'ana', 'idade': 25, 'tipo': 'aluno', 'senha': 'aninha25'}
]

if entra == "criar":
    novo_aluno = criaAluno()
    lista_alunos.append(novo_aluno)
    print("Conta criada com sucesso!")
    print(lista_alunos)

def entra_conta(matr, senha):
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

if entra == "entrar":
    matri = input("Digite sua matrícula: ")
    passw = input("Digite sua senha: ")
    entra_conta(matri, passw)
