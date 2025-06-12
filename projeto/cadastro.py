entra = input("digite criar se quiser criar uma conta e entrar se quiser entrar na sua conta ja criada: ")

def criaAluno():
    nome = input("Digite seu nome: ")

    tipo = input("digite seu tipo: ")
    while tipo != "aluno" and tipo != "professor":
        tipo = input("tipo não reconhecido, tente novamente: ")

    matr = input("Digite sua matrícula (7 dígitos): ")
    while not matr.isdigit() or int(matr) > 9999999 or int(matr) < 1000000:
        matr = input("Matrícula inválida, digite novamente (7 dígitos): ")
    
    idade = input("Digite sua idade: ")
    while not idade.isdigit() or int(idade) <= 0:
        idade = input("Idade inválida, digite novamente: ")
    
    pasw = input("digite sua senha: ")
    pasc = input("confirme sua senha: ")

    while pasw != pasc:
        pasw = input("Senha confirmada diferente da digitada, digite novamente: ")
        pasc = input("confirme novamente: ")

    aluno = {
        'matricula': int(matr),
        'nome': nome,
        'idade': int(idade),
        'tipo': tipo,
        'senha': pasw
    }
    
    return aluno

if entra == "criar":
    novo_aluno = criaAluno()

# Se quiser começar com a lista existente da imagem:
lista_alunos = [
    {'matricula': 20190202, 'nome': 'andré', 'idade': 20, 'tipo':'aluno', 'senha': 'Dede2005'},
    {'matricula': 2014433, 'nome': 'flavio', 'idade': 22, 'tipo' : 'professor', 'senha': 'flafla03'},
    {'matricula': 2015555, 'nome': 'ana', 'idade': 25, 'tipo' : 'aluno', 'senha':'aninha25'}
]

# Adiciona o novo aluno à lista
lista_alunos.append(novo_aluno)

# Exibe a lista atualizada
print(lista_alunos)
