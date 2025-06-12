import os
from auxiliar import load_json, save_json, TURMAS_JSON_PATH, LISTAS_DE_EXERCICIOS_DIR

def cria_exercicio(exercicios_lista: list, tema: str, enunciado: str, alternativas: list, nome_lista_json: str) -> list:
    """
    Função que adiciona um novo exercício a uma lista de exercícios e salva a lista em um arquivo JSON.

    Args:
        exercicios_lista (list): A lista existente de exercícios à qual o novo exercício será adicionado.
        tema (str): O tema do exercício.
        enunciado (str): O enunciado do exercício.
        alternativas (list): Uma lista de alternativas (A, B, C).
        nome_lista_json (str): O nome do arquivo JSON (ex: "matematica.json") onde a lista será salva.
                               O arquivo será salvo no diretório LISTAS_DE_EXERCICIOS_DIR.

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

    # Constrói o caminho completo do arquivo para salvar a lista de exercícios
    output_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_lista_json)
    save_json(exercicios_lista, output_path)

    return exercicios_lista

def cria_turma(nome_turma: str):
    """
    Função que cria no JSON uma turma, sendo o nome dela a chave
    e um dicionário com 'alunos' e 'listas' como valor.

    Args:
        nome_turma (str): Nome da turma a ser criada.
    """
    turmas_data = load_json(TURMAS_JSON_PATH, {})

    if nome_turma in turmas_data:
        print(f"A turma '{nome_turma}' já existe.")
    else:
        turmas_data[nome_turma] = {
            "alunos": [],
            "listas": []
        }
        save_json(turmas_data, TURMAS_JSON_PATH)
        print(f"Turma '{nome_turma}' criada com sucesso.")

def insere_aluno(nome_turma: str, matricula: int):
    """
    Função para inserir um aluno em uma turma. Busca a turma no JSON
    e insere a matrícula do aluno na lista de alunos que é seu valor.

    Args:
        nome_turma (str): Nome da turma onde o aluno será inserido.
        matricula (int): Matrícula do aluno a ser inserido.
    """
    turmas_data = load_json(TURMAS_JSON_PATH, {})

    if nome_turma not in turmas_data:
        print(f"Erro: Turma '{nome_turma}' não encontrada.")
        return

    # Garante que a estrutura da turma é um dicionário com 'alunos' e 'listas'
    if not isinstance(turmas_data[nome_turma], dict) or "alunos" not in turmas_data[nome_turma]:
        print(f"Aviso: Estrutura da turma '{nome_turma}' inválida ou antiga. Tentando corrigir.")
        turmas_data[nome_turma] = {"alunos": [], "listas": []} # Reinicia a estrutura

    if matricula in turmas_data[nome_turma]["alunos"]:
        print(f"Matrícula {matricula} já existe na turma '{nome_turma}'.")
    else:
        turmas_data[nome_turma]["alunos"].append(matricula)
        save_json(turmas_data, TURMAS_JSON_PATH)
        print(f"Aluno com matrícula {matricula} inserido na turma '{nome_turma}'.")

def passa_lista(nome_lista_json: str, turma: str):
    """
    Função que recebe o nome de um arquivo JSON de lista, busca esse arquivo,
    e com o nome da turma adiciona o nome do arquivo da lista ao JSON das turmas.

    Args:
        nome_lista_json (str): O nome do arquivo JSON da lista de exercícios (ex: "matematica.json").
        turma (str): O nome da turma à qual a lista será associada.
    """
    turmas_data = load_json(TURMAS_JSON_PATH, {})

    # 1. Verificar se a turma existe
    if turma not in turmas_data:
        print(f"Erro: Turma '{turma}' não encontrada. Crie a turma primeiro.")
        return
    
    # Garante que a estrutura da turma é um dicionário com 'alunos' e 'listas'
    if not isinstance(turmas_data[turma], dict) or "listas" not in turmas_data[turma]:
        print(f"Aviso: Estrutura da turma '{turma}' inválida ou antiga. Tentando corrigir.")
        turmas_data[turma] = {"alunos": [], "listas": []}

    # 2. Constrói o caminho completo para verificar a existência do arquivo da lista
    lista_full_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_lista_json)
    if not os.path.exists(lista_full_path):
        print(f"Erro: O arquivo de lista de exercícios '{nome_lista_json}' não foi encontrado no diretório '{LISTAS_DE_EXERCICIOS_DIR}'.")
        return

    # 3. Adicionar o nome do arquivo da lista à lista de listas da turma
    if nome_lista_json in turmas_data[turma]["listas"]:
        print(f"A lista '{nome_lista_json}' já está associada à turma '{turma}'.")
    else:
        turmas_data[turma]["listas"].append(nome_lista_json)
        save_json(turmas_data, TURMAS_JSON_PATH)
        print(f"Lista '{nome_lista_json}' associada com sucesso à turma '{turma}'.")

# --- Exemplo de Uso (para testar em professor.py, mas não faça isso no arquivo final) ---
if __name__ == "__main__":
    print("--- Testando funcionalidades de professor.py ---")

    # (Opcional) Limpeza para um teste limpo
    # if os.path.exists(TURMAS_JSON_PATH): os.remove(TURMAS_JSON_PATH)
    # if os.path.exists(LISTAS_DE_EXERCICIOS_DIR):
    #     for f in os.listdir(LISTAS_DE_EXERCICIOS_DIR):
    #         os.remove(os.path.join(LISTAS_DE_EXERCICIOS_DIR, f))
    #     os.rmdir(LISTAS_DE_EXERCICIOS_DIR)

    # 1. Criar uma nova lista de exercícios e salvá-la
    minha_lista_mat = []
    cria_exercicio(
        minha_lista_mat,
        "Matemática",
        "Quanto é 10 dividido por 2?",
        ["2", "5", "10"],
        "matematica_basica.json" # Nome do arquivo JSON
    )

    minha_lista_port = []
    cria_exercicio(
        minha_lista_port,
        "Português",
        "Qual a classe gramatical de 'muito' em 'Ele come muito'?",
        ["Substantivo", "Adjetivo", "Advérbio"],
        "portugues_avancado.json" # Nome do arquivo JSON
    )
    print("\nListas de exercícios criadas e salvas em 'listas_de_exercicios/'.")


    # 2. Criar turmas
    cria_turma("Turma Alfa")
    cria_turma("Turma Beta")
    print("\nTurmas após criação:", load_json(TURMAS_JSON_PATH))

    # 3. Inserir alunos
    insere_aluno("Turma Alfa", 1001)
    insere_aluno("Turma Alfa", 1002)
    insere_aluno("Turma Beta", 2001)
    insere_aluno("Turma Inexistente", 3001)
    print("\nTurmas após inserção de alunos:", load_json(TURMAS_JSON_PATH))

    # 4. Passar listas para turmas
    passa_lista("matematica_basica.json", "Turma Alfa")
    passa_lista("portugues_avancado.json", "Turma Alfa")
    passa_lista("matematica_basica.json", "Turma Beta") # Passando a mesma lista para outra turma
    passa_lista("lista_inexistente.json", "Turma Alfa") # Tentando passar lista que não existe
    print("\nTurmas após associação de listas:", load_json(TURMAS_JSON_PATH))

    print("\nFim dos testes. Verifique os arquivos 'turmas.json' e a pasta 'listas_de_exercicios'.")