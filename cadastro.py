from dataclasses import dataclass

@dataclass
class Conta:
    nome: str
    matricula: int
    tipo: str
    senha: str

def criaConta():
    name = input("digite seu nome: ")
    matr = input("digite sua matricula: ")
    while not matr.isdigit() or matr >9999999 or matr<1000000:
        matr = input("matricula inválida, digite novamente: ")
    tipo = input("digite 1 se você for um aluno e 2 se for um professor ")
    while tipo !='1' and tipo != '2':
        tipo = input("tipo de conta não reconhecida, tente novamente: ")
    pasw = input("digite sua senha: ")
    pasc = input("digite novamente sua senha para confirmar: ")

    
    while pasw != pasc:
        pasw = input("as senhas sao diferentes, tente novamente: ")
        pasc  = input("digite novamente sua senha para confirmar: ")
    if tipo == '1':
        novaConta = Conta(name, int(matr), 'aluno', pasw)
    else:
        novaConta = Conta(name, int(matr), 'professor', str(pasw))
    return novaConta


novaPessoa = criaConta()


print(novaPessoa.nome)
print(novaPessoa.matricula)
print(novaPessoa.tipo)
print(novaPessoa.senha)
