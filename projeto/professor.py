from cadastro import conta


def cria_exercicio(exercicios_lista: list, tema: str, enunciado: str, alternativas: list) -> list:
    """
    Função que adiciona um novo exercício a uma lista de exercícios.

    Args:
        exercicios_lista (list): A lista existente de exercícios à qual o novo exercício será adicionado.
        tema (str): O tema do exercício.
        enunciado (str): O enunciado do exercício.
        alternativas (list): Uma lista de alternativas (A, B, C).

    Returns:
        list: A lista de exercícios atualizada.
    """
    if len(alternativas) < 3:
        raise ValueError("São necessárias pelo menos 3 alternativas.")

    novo_exercicio = {
        'Tema': tema,
        'Enunciado': enunciado,
        'Alternativa A': alternativas[0],
        'Alternativa B': alternativas[1],
        'Alternativa C': alternativas[2]
    }
    exercicios_lista.append(novo_exercicio)
    return exercicios_lista # Retornar a lista é opcional, pois .append modifica in-place

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
