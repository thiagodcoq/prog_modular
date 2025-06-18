import os
from auxiliar import load_json, save_json, TURMAS_JSON_PATH, LISTAS_DE_EXERCICIOS_DIR, USUARIOS_JSON_PATH, PROGRESO_ALUNOS_JSON_PATH

def cria_exercicio(exercicios_lista: list, tema: str, enunciado: str, alternativas: list, resposta_correta_letra: str, nome_lista_json: str) -> dict:
    """
    Adiciona um novo exercício a uma lista e a salva.
    Não lida com input/print, recebe a letra da resposta correta diretamente.
    Retorna um dicionário com status e mensagem/dados.
    """
    if len(alternativas) < 3:
        return {"status": "erro", "mensagem": "São necessárias pelo menos 3 alternativas."}

    if resposta_correta_letra.upper() not in ('A', 'B', 'C'):
        return {"status": "erro", "mensagem": "Letra da alternativa correta inválida. Digite A, B ou C."}

    # Transforma a letra da resposta correta para minúsculo para consistência
    resposta_correta_para_salvar = resposta_correta_letra.lower()
    
    novo_exercicio = {
        'Tema': tema,
        'Enunciado': enunciado,
        'Alternativa A': alternativas[0],
        'Alternativa B': alternativas[1],
        'Alternativa C': alternativas[2],
        'RespostaCorreta': resposta_correta_para_salvar
    }
    exercicios_lista.append(novo_exercicio)

    output_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_lista_json)
    save_json(exercicios_lista, output_path)

    return {"status": "sucesso", "mensagem": f"Exercício '{tema}' adicionado e lista '{nome_lista_json}' atualizada.", "lista_atualizada": exercicios_lista}

def cria_turma(nome_turma: str) -> dict:
    """
    Cria uma nova turma.
    Retorna um dicionário com status e mensagem.
    """
    turmas_data = load_json(TURMAS_JSON_PATH, {})
    if nome_turma in turmas_data:
        return {"status": "erro", "mensagem": f"A turma '{nome_turma}' já existe."}
    else:
        turmas_data[nome_turma] = {"alunos": [], "listas": []}
        save_json(turmas_data, TURMAS_JSON_PATH)
        return {"status": "sucesso", "mensagem": f"Turma '{nome_turma}' criada com sucesso."}

def insere_aluno(nome_turma: str, matricula: int) -> dict:
    """
    Insere um aluno em uma turma.
    Retorna um dicionário com status e mensagem.
    """
    turmas_data = load_json(TURMAS_JSON_PATH, {})
    usuarios_data = load_json(USUARIOS_JSON_PATH, {})

    if nome_turma not in turmas_data:
        return {"status": "erro", "mensagem": f"Turma '{nome_turma}' não encontrada."}
    
    matricula_str = str(matricula)
    if matricula_str not in usuarios_data or usuarios_data[matricula_str].get('tipo') != 'aluno':
        return {"status": "erro", "mensagem": f"Matrícula {matricula} não encontrada ou não corresponde a um aluno cadastrado."}
    
    if not isinstance(turmas_data[nome_turma], dict) or "alunos" not in turmas_data[nome_turma]:
        turmas_data[nome_turma] = {"alunos": [], "listas": []}
        save_json(turmas_data, TURMAS_JSON_PATH)
        return {"status": "aviso", "mensagem": f"Aviso: Estrutura da turma '{nome_turma}' inválida. Tentando corrigir e inserir aluno."}

    if matricula in turmas_data[nome_turma]["alunos"]:
        return {"status": "erro", "mensagem": f"Matrícula {matricula} já existe na turma '{nome_turma}'."}
    else:
        turmas_data[nome_turma]["alunos"].append(matricula)
        save_json(turmas_data, TURMAS_JSON_PATH)
        return {"status": "sucesso", "mensagem": f"Aluno com matrícula {matricula} inserido na turma '{nome_turma}'."}

def remove_aluno(nome_turma: str, matricula: int) -> dict:
    """
    Remove um aluno de uma turma.
    Retorna um dicionário com status e mensagem.
    """
    turmas_data = load_json(TURMAS_JSON_PATH, {})

    if nome_turma not in turmas_data:
        return {"status": "erro", "mensagem": f"Turma '{nome_turma}' não encontrada."}
    
    if not isinstance(turmas_data[nome_turma], dict) or "alunos" not in turmas_data[nome_turma]:
        return {"status": "erro", "mensagem": f"Aviso: Estrutura da turma '{nome_turma}' inválida. Alunos não podem ser removidos."}

    if matricula not in turmas_data[nome_turma]["alunos"]:
        return {"status": "erro", "mensagem": f"A matrícula {matricula} não está na turma '{nome_turma}'."}
    else:
        turmas_data[nome_turma]["alunos"].remove(matricula)
        save_json(turmas_data, TURMAS_JSON_PATH)
        return {"status": "sucesso", "mensagem": f"Aluno com matrícula {matricula} removido da turma '{nome_turma}'."}

def get_turmas_existentes() -> list:
    """Retorna uma lista dos nomes das turmas existentes."""
    turmas_data = load_json(TURMAS_JSON_PATH, {})
    return list(turmas_data.keys())

def get_listas_existentes() -> list:
    """Retorna uma lista dos nomes dos arquivos de listas de exercícios existentes."""
    return [f for f in os.listdir(LISTAS_DE_EXERCICIOS_DIR) if f.endswith(".json")]

def visualiza_turma(nome_turma: str) -> dict:
    """
    Retorna os detalhes de uma turma (alunos, listas e índice de acertos).
    Não lida com input/print, retorna os dados para serem exibidos.
    """
    turmas_data = load_json(TURMAS_JSON_PATH, {})
    usuarios_data = load_json(USUARIOS_JSON_PATH, {})
    progresso_alunos_data = load_json(PROGRESO_ALUNOS_JSON_PATH, {})

    if nome_turma not in turmas_data:
        return {"status": "erro", "mensagem": f"Erro: Turma '{nome_turma}' não encontrada."}

    dados_turma = turmas_data[nome_turma]
    
    # Detalhes dos Alunos
    alunos_na_turma_detalhes = []
    alunos_na_turma_ids = dados_turma.get("alunos", [])
    if alunos_na_turma_ids:
        for matricula in alunos_na_turma_ids:
            aluno_info = usuarios_data.get(str(matricula))
            nome_aluno = aluno_info.get('nome', 'Nome Desconhecido') if aluno_info else 'Nome Desconhecido'
            alunos_na_turma_detalhes.append({"matricula": matricula, "nome": nome_aluno})

    # Detalhes das Listas e Índice de Acertos
    listas_associadas_detalhes = []
    listas_da_turma_nomes = dados_turma.get("listas", [])
    
    if listas_da_turma_nomes:
        for nome_lista in listas_da_turma_nomes:
            lista_detalhe = {"nome_lista": nome_lista, "indice_acerto": "N/A", "msg_acerto": "", "num_alunos_contribuintes": 0}
            
            lista_full_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_lista)
            exercicios_da_lista = load_json(lista_full_path, [])
            
            if not exercicios_da_lista:
                lista_detalhe["msg_acerto"] = "(Lista vazia ou não carregada)"
                listas_associadas_detalhes.append(lista_detalhe)
                continue

            total_acertos_geral = 0
            total_respostas_contabilizadas_geral = 0
            total_alunos_que_responderam = 0

            for matricula_aluno in alunos_na_turma_ids:
                matricula_str = str(matricula_aluno)
                aluno_progresso = progresso_alunos_data.get(matricula_str, {}).get(nome_lista, {})
                
                if aluno_progresso.get('status') == 'completo' or aluno_progresso.get('progresso', 0) > 0:
                    total_alunos_que_responderam += 1
                    respostas_dadas_aluno = aluno_progresso.get('respostas', {})
                    
                    for idx_ex, ex_data in enumerate(exercicios_da_lista):
                        resp_correta = ex_data.get('RespostaCorreta', '').lower()
                        if resp_correta:
                            total_respostas_contabilizadas_geral += 1
                            resp_dada = respostas_dadas_aluno.get(str(idx_ex), '').lower()
                            if resp_dada == resp_correta:
                                total_acertos_geral += 1

            if total_respostas_contabilizadas_geral > 0:
                indice_acerto = (total_acertos_geral / total_respostas_contabilizadas_geral) * 100
                lista_detalhe["indice_acerto"] = f"{indice_acerto:.2f}%"
                lista_detalhe["msg_acerto"] = f"({total_acertos_geral} acertos em {total_respostas_contabilizadas_geral} respostas válidas de questões com resposta correta definida.)"
                lista_detalhe["num_alunos_contribuintes"] = total_alunos_que_responderam
            else:
                lista_detalhe["msg_acerto"] = "Nenhum aluno respondeu a esta lista ainda ou as questões não têm resposta correta definida."
            
            listas_associadas_detalhes.append(lista_detalhe)
    
    return {
        "status": "sucesso",
        "nome_turma": nome_turma,
        "alunos": alunos_na_turma_detalhes,
        "listas": listas_associadas_detalhes
    }


def passa_lista(nome_lista_json: str, turma: str) -> dict:
    """
    Associa uma lista de exercícios a uma turma.
    Não lida com input/print, retorna status e mensagem.
    """
    turmas_data = load_json(TURMAS_JSON_PATH, {})

    if turma not in turmas_data:
        return {"status": "erro", "mensagem": f"Turma '{turma}' não encontrada."}

    lista_full_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_lista_json)
    if not os.path.exists(lista_full_path):
        return {"status": "erro", "mensagem": f"O arquivo de lista de exercícios '{nome_lista_json}' não foi encontrado no diretório '{LISTAS_DE_EXERCICIOS_DIR}'."}

    if not isinstance(turmas_data[turma], dict) or "listas" not in turmas_data[turma]:
        turmas_data[turma] = {"alunos": [], "listas": []}
        save_json(turmas_data, TURMAS_JSON_PATH)
        return {"status": "aviso", "mensagem": f"Aviso: Estrutura da turma '{turma}' inválida. Tentando corrigir e associar lista."}

    if nome_lista_json in turmas_data[turma]["listas"]:
        return {"status": "erro", "mensagem": f"A lista '{nome_lista_json}' já está associada à turma '{turma}'."}
    else:
        turmas_data[turma]["listas"].append(nome_lista_json)
        save_json(turmas_data, TURMAS_JSON_PATH)
        return {"status": "sucesso", "mensagem": f"Lista '{nome_lista_json}' associada com sucesso à turma '{turma}'."}