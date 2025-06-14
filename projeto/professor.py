import os
from auxiliar import load_json, save_json, TURMAS_JSON_PATH, LISTAS_DE_EXERCICIOS_DIR, USUARIOS_JSON_PATH

def cria_exercicio(exercicios_lista: list, tema: str, enunciado: str, alternativas: list, nome_lista_json: str) -> list:
    """
    Função que adiciona um novo exercício a uma lista de exercícios e salva a lista em um arquivo JSON.
    Agora inclui a resposta correta, que é solicitada ao professor e tratada como case-insensitive.
    """
    if len(alternativas) < 3:
        raise ValueError("São necessárias pelo menos 3 alternativas.")

    print("Alternativas disponíveis:")
    for i, alt in enumerate(alternativas):
        print(f"{chr(65+i)}) {alt}")

    while True:
        resposta_correta_letra = input("Digite a letra da alternativa correta (A, B ou C): ").upper()
        if resposta_correta_letra in ('A', 'B', 'C'):
            resposta_correta_indice = ord(resposta_correta_letra) - ord('A')
            resposta_correta_texto = alternativas[resposta_correta_indice]
            break
        else:
            print("Opção inválida. Digite A, B ou C.")

    novo_exercicio = {
        'Tema': tema,
        'Enunciado': enunciado,
        'Alternativa A': alternativas[0],
        'Alternativa B': alternativas[1],
        'Alternativa C': alternativas[2],
        'RespostaCorreta': resposta_correta_texto.lower()
    }
    exercicios_lista.append(novo_exercicio)

    output_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_lista_json)
    save_json(exercicios_lista, output_path)

    return exercicios_lista

def cria_turma(nome_turma: str):
    """Função para criar turmas."""
    turmas_data = load_json(TURMAS_JSON_PATH, {})
    if nome_turma in turmas_data:
        print(f"A turma '{nome_turma}' já existe.")
    else:
        turmas_data[nome_turma] = {"alunos": [], "listas": []}
        save_json(turmas_data, TURMAS_JSON_PATH)
        print(f"Turma '{nome_turma}' criada com sucesso.")

def insere_aluno(nome_turma: str, matricula: int):
    """Função para inserir aluno em turma."""
    turmas_data = load_json(TURMAS_JSON_PATH, {})
    usuarios_data = load_json(USUARIOS_JSON_PATH, {})
    if nome_turma not in turmas_data:
        print(f"Erro: Turma '{nome_turma}' não encontrada.")
        return
    matricula_str = str(matricula)
    if matricula_str not in usuarios_data or usuarios_data[matricula_str].get('tipo') != 'aluno':
        print(f"Erro: Matrícula {matricula} não encontrada ou não corresponde a um aluno cadastrado.")
        return
    if not isinstance(turmas_data[nome_turma], dict) or "alunos" not in turmas_data[nome_turma]:
        print(f"Aviso: Estrutura da turma '{nome_turma}' inválida. Tentando corrigir.")
        turmas_data[nome_turma] = {"alunos": [], "listas": []}
    if matricula in turmas_data[nome_turma]["alunos"]:
        print(f"Matrícula {matricula} já existe na turma '{nome_turma}'.")
    else:
        turmas_data[nome_turma]["alunos"].append(matricula)
        save_json(turmas_data, TURMAS_JSON_PATH)
        print(f"Aluno com matrícula {matricula} inserido na turma '{nome_turma}'.")

def remove_aluno(nome_turma: str, matricula: int):
    """
    Função para remover um aluno de uma turma.

    Args:
        nome_turma (str): Nome da turma da qual o aluno será removido.
        matricula (int): Matrícula do aluno a ser removido.
    """
    turmas_data = load_json(TURMAS_JSON_PATH, {})

    if nome_turma not in turmas_data:
        print(f"Erro: Turma '{nome_turma}' não encontrada.")
        return
    
    # Garante que a estrutura da turma é um dicionário com 'alunos' e 'listas'
    if not isinstance(turmas_data[nome_turma], dict) or "alunos" not in turmas_data[nome_turma]:
        print(f"Aviso: Estrutura da turma '{nome_turma}' inválida. Alunos não podem ser removidos.")
        return

    if matricula not in turmas_data[nome_turma]["alunos"]:
        print(f"A matrícula {matricula} não está na turma '{nome_turma}'.")
    else:
        turmas_data[nome_turma]["alunos"].remove(matricula)
        save_json(turmas_data, TURMAS_JSON_PATH)
        print(f"Aluno com matrícula {matricula} removido da turma '{nome_turma}'.")

def visualiza_turma(nome_turma: str):
    """
    Função para visualizar os detalhes de uma turma (alunos e listas).

    Args:
        nome_turma (str): Nome da turma a ser visualizada.
    """
    turmas_data = load_json(TURMAS_JSON_PATH, {})
    usuarios_data = load_json(USUARIOS_JSON_PATH, {}) # Para buscar nomes dos alunos

    if nome_turma not in turmas_data:
        print(f"Erro: Turma '{nome_turma}' não encontrada.")
        return

    dados_turma = turmas_data[nome_turma]
    print(f"\n--- Detalhes da Turma: {nome_turma} ---")

    # Visualizar Alunos
    alunos_na_turma = dados_turma.get("alunos", [])
    print("\nAlunos:")
    if alunos_na_turma:
        for matricula in alunos_na_turma:
            aluno_info = usuarios_data.get(str(matricula)) # Matrícula é chave string no usuarios.json
            nome_aluno = aluno_info.get('nome', 'Nome Desconhecido') if aluno_info else 'Nome Desconhecido'
            print(f"- Matrícula: {matricula}, Nome: {nome_aluno}")
    else:
        print("Nenhum aluno nesta turma.")

    # Visualizar Listas
    listas_da_turma = dados_turma.get("listas", [])
    print("\nListas de Exercícios Associadas:")
    if listas_da_turma:
        for nome_lista in listas_da_turma:
            print(f"- {nome_lista}")
    else:
        print("Nenhuma lista de exercícios associada a esta turma.")
    print("-" * (len(nome_turma) + 20)) # Linha de separação para estética

def passa_lista(nome_lista_json: str, turma: str):
    """Função para passar uma lista para uma turma, com sugestões de turmas e listas."""
    turmas_data = load_json(TURMAS_JSON_PATH, {})

    print("\n--- Turmas Existentes ---")
    if turmas_data:
        for nome_turma_existente in turmas_data.keys():
            print(f"- {nome_turma_existente}")
    else:
        print("Nenhuma turma encontrada. Crie uma turma primeiro.")

    if turma not in turmas_data:
        print(f"Erro: Turma '{turma}' não encontrada. Crie a turma primeiro.")
        return

    print("\n--- Listas de Exercícios Existentes ---")
    listas_no_diretorio = [f for f in os.listdir(LISTAS_DE_EXERCICIOS_DIR) if f.endswith(".json")]
    if listas_no_diretorio:
        for filename in listas_no_diretorio:
             print(f"- {filename}")
    else:
        print("Nenhuma lista de exercícios encontrada. Crie exercícios primeiro.")

    lista_full_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_lista_json)
    if not os.path.exists(lista_full_path):
        print(f"Erro: O arquivo de lista de exercícios '{nome_lista_json}' não foi encontrado no diretório '{LISTAS_DE_EXERCICIOS_DIR}'.")
        return

    if not isinstance(turmas_data[turma], dict) or "listas" not in turmas_data[turma]:
        print(f"Aviso: Estrutura da turma '{turma}' inválida ou antiga. Tentando corrigir.")
        turmas_data[turma] = {"alunos": [], "listas": []}

    if nome_lista_json in turmas_data[turma]["listas"]:
        print(f"A lista '{nome_lista_json}' já está associada à turma '{turma}'.")
    else:
        turmas_data[turma]["listas"].append(nome_lista_json)
        save_json(turmas_data, TURMAS_JSON_PATH)
        print(f"Lista '{nome_lista_json}' associada com sucesso à turma '{turma}'.")