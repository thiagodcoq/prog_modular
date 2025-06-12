from cadastro import conta


def cria_exercicio(titulo_lista:str,lista_de_exercicio:list)->None:
    """ Funcao que cira json com a lista de exercicios junto de seu titulo

    Args:
        titulo_lista (str): Titulo da lista
        lista_de_exercicio (list): Lista em que cada posicao é uma string com uma questao
    """
    pass

def passa_lista(titulo_lista:str,turma:str)->None:
    """ Funcao que recebe o titulo de uma lista, busca essa lista no json das listas
    e com o nome da turma adiciona essa lista ao json das turmas

    Args:
        titulo_lista (str): _description_
        turma (str): _description_
    """


def cria_turma(nome_turma:str)->None:
    """ Funcao que cria no json uma turma sendo o nome dela a chave
    e a lista da turma o valor

    Args:
        nome_turma (str): Nome da turma
    """
    pass

def insere_aluno(nome_turma:str,matricula:int)->None:
    """ Funcao para inserir um aluno em uma turma, funcao deve buscar a turma no json,
    e inserir a matricula do aluno na lista de alunos que é seu valor.


    Args:
        turma (str): Nome da turma
        matricula (int): Matricula do aluno
    """
    pass
