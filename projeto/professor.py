import os  # Importa o módulo 'os' para interagir com o sistema operacional, especialmente para manipulação de caminhos de arquivo.
from auxiliar import load_json, save_json, TURMAS_JSON_PATH, LISTAS_DE_EXERCICIOS_DIR, USUARIOS_JSON_PATH, PROGRESO_ALUNOS_JSON_PATH
# Importa funções auxiliares e variáveis de caminho de outros módulos para gerenciar dados.

def cria_exercicio(exercicios_lista: list, tema: str, enunciado: str, alternativas: list, resposta_correta_letra: str, nome_lista_json: str) -> dict:
    """
    Objetivo: Adicionar um novo exercício a uma lista de exercícios existente ou criar uma nova lista e salvá-la.
    Esta função é uma parte da lógica de negócio do professor e não interage diretamente com o usuário
    (i.e., não usa 'input()' nem 'print()' para exibir mensagens ao usuário).

    Args:
        exercicios_lista (list): A lista de dicionários de exercícios à qual o novo exercício será adicionado.
                                 Esta lista é normalmente carregada do arquivo JSON existente pelo 'main.py'.
        tema (str): O tema do exercício (ex: "Matemática", "História").
        enunciado (str): O enunciado completo do exercício.
        alternativas (list): Uma lista contendo as strings das alternativas disponíveis (ex: ["Opção A", "Opção B", "Opção C"]).
                             Assume-se que haja pelo menos 3 alternativas.
        resposta_correta_letra (str): A letra (maiuscula ou minuscula) da alternativa correta (ex: "A", "b").
                                      Esta entrada é validada antes de ser processada.
        nome_lista_json (str): O nome do arquivo JSON onde a lista de exercícios (com o novo exercício) será salva.
                               O arquivo será salvo no diretório definido por LISTAS_DE_EXERCICIOS_DIR.

    Returns:
        dict: Um dicionário contendo o 'status' da operação ("sucesso" ou "erro"),
              uma 'mensagem' descritiva do resultado, e opcionalmente a 'lista_atualizada'.
    """
    # Valida se há pelo menos 3 alternativas fornecidas, conforme a regra de negócio.
    if len(alternativas) < 3:
        return {"status": "erro", "mensagem": "São necessárias pelo menos 3 alternativas."}

    # Valida se a letra da resposta correta é uma das opções válidas ('A', 'B', 'C').
    if resposta_correta_letra.upper() not in ('A', 'B', 'C'):
        return {"status": "erro", "mensagem": "Letra da alternativa correta inválida. Digite A, B ou C."}

    # Transforma a letra da resposta correta para minúsculo para garantir consistência
    # na comparação posterior com as respostas dos alunos (que são salvas em minúsculo).
    resposta_correta_para_salvar = resposta_correta_letra.lower()
    
    # Cria um novo dicionário representando o exercício, com todas as informações fornecidas.
    novo_exercicio = {
        'Tema': tema,
        'Enunciado': enunciado,
        'Alternativa A': alternativas[0],
        'Alternativa B': alternativas[1],
        'Alternativa C': alternativas[2],
        'RespostaCorreta': resposta_correta_para_salvar # Salva a letra ('a', 'b', 'c') como resposta correta.
    }
    
    # Adiciona o novo exercício à lista de exercícios que foi passada (que pode estar vazia ou já ter exercícios).
    exercicios_lista.append(novo_exercicio)

    # Constrói o caminho completo do arquivo JSON onde a lista de exercícios será salva/atualizada.
    output_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_lista_json)
    
    # Salva a lista de exercícios atualizada no arquivo JSON.
    save_json(exercicios_lista, output_path)

    # Retorna um dicionário de sucesso, indicando que a operação foi bem-sucedida.
    return {"status": "sucesso", "mensagem": f"Exercício '{tema}' adicionado e lista '{nome_lista_json}' atualizada.", "lista_atualizada": exercicios_lista}

def cria_turma(nome_turma: str) -> dict:
    """
    Objetivo: Criar uma nova turma no sistema.
    Esta função manipula os dados das turmas e não interage diretamente com o usuário.

    Args:
        nome_turma (str): O nome da turma a ser criada.

    Returns:
        dict: Um dicionário com o 'status' da operação ("sucesso" ou "erro")
              e uma 'mensagem' descritiva do resultado.
    """
    # Carrega os dados de todas as turmas existentes.
    turmas_data = load_json(TURMAS_JSON_PATH, {})
    
    # Verifica se o nome da turma já existe no sistema.
    if nome_turma in turmas_data:
        return {"status": "erro", "mensagem": f"A turma '{nome_turma}' já existe."}
    else:
        # Se a turma não existe, cria uma nova entrada no dicionário de turmas.
        # Inicializa a turma com listas vazias para alunos e listas de exercícios.
        turmas_data[nome_turma] = {"alunos": [], "listas": []}
        
        # Salva o dicionário de turmas atualizado de volta no arquivo JSON.
        save_json(turmas_data, TURMAS_JSON_PATH)
        
        # Retorna um dicionário de sucesso.
        return {"status": "sucesso", "mensagem": f"Turma '{nome_turma}' criada com sucesso."}

def insere_aluno(nome_turma: str, matricula: int) -> dict:
    """
    Objetivo: Inserir um aluno em uma turma específica.
    Esta função manipula os dados das turmas e não interage diretamente com o usuário.

    Args:
        nome_turma (str): O nome da turma onde o aluno será inserido.
        matricula (int): A matrícula do aluno a ser inserido.

    Returns:
        dict: Um dicionário com o 'status' da operação ("sucesso", "erro" ou "aviso")
              e uma 'mensagem' descritiva do resultado.
    """
    # Carrega os dados de todas as turmas e de todos os usuários.
    turmas_data = load_json(TURMAS_JSON_PATH, {})
    usuarios_data = load_json(USUARIOS_JSON_PATH, {})

    # Verifica se a turma especificada existe.
    if nome_turma not in turmas_data:
        return {"status": "erro", "mensagem": f"Turma '{nome_turma}' não encontrada."}
    
    # Valida se a matrícula corresponde a um usuário existente e se esse usuário é do tipo 'aluno'.
    matricula_str = str(matricula) # Matrículas são chaves como strings no USUARIOS_JSON_PATH.
    if matricula_str not in usuarios_data or usuarios_data[matricula_str].get('tipo') != 'aluno':
        return {"status": "erro", "mensagem": f"Matrícula {matricula} não encontrada ou não corresponde a um aluno cadastrado."}
    
    # Garante que a estrutura da turma é válida (dicionário com chaves 'alunos' e 'listas').
    # Isso lida com possíveis inconsistências em dados antigos ou malformados, tentando corrigi-los.
    if not isinstance(turmas_data[nome_turma], dict) or "alunos" not in turmas_data[nome_turma]:
        turmas_data[nome_turma] = {"alunos": [], "listas": []}
        save_json(turmas_data, TURMAS_JSON_PATH) # Salva a correção na estrutura da turma.
        return {"status": "aviso", "mensagem": f"Aviso: Estrutura da turma '{nome_turma}' inválida. Tentando corrigir e inserir aluno."}

    # Verifica se o aluno já está matriculado na turma.
    if matricula in turmas_data[nome_turma]["alunos"]:
        return {"status": "erro", "mensagem": f"Matrícula {matricula} já existe na turma '{nome_turma}'."}
    else:
        # Adiciona a matrícula do aluno à lista de alunos da turma.
        turmas_data[nome_turma]["alunos"].append(matricula)
        # Salva os dados de turmas atualizados.
        save_json(turmas_data, TURMAS_JSON_PATH)
        # Retorna um dicionário de sucesso.
        return {"status": "sucesso", "mensagem": f"Aluno com matrícula {matricula} inserido na turma '{nome_turma}'."}

def remove_aluno(nome_turma: str, matricula: int) -> dict:
    """
    Objetivo: Remover um aluno de uma turma específica.
    Esta função manipula os dados das turmas e não interage diretamente com o usuário.

    Args:
        nome_turma (str): O nome da turma da qual o aluno será removido.
        matricula (int): A matrícula do aluno a ser removido.

    Returns:
        dict: Um dicionário com o 'status' da operação ("sucesso" ou "erro")
              e uma 'mensagem' descritiva do resultado.
    """
    # Carrega os dados de todas as turmas.
    turmas_data = load_json(TURMAS_JSON_PATH, {})

    # Verifica se a turma especificada existe.
    if nome_turma not in turmas_data:
        return {"status": "erro", "mensagem": f"Turma '{nome_turma}' não encontrada."}
    
    # Garante que a estrutura da turma é válida para permitir a remoção de alunos.
    if not isinstance(turmas_data[nome_turma], dict) or "alunos" not in turmas_data[nome_turma]:
        return {"status": "erro", "mensagem": f"Aviso: Estrutura da turma '{nome_turma}' inválida. Alunos não podem ser removidos."}

    # Verifica se o aluno está realmente na turma.
    if matricula not in turmas_data[nome_turma]["alunos"]:
        return {"status": "erro", "mensagem": f"A matrícula {matricula} não está na turma '{nome_turma}'."}
    else:
        # Remove a matrícula do aluno da lista de alunos da turma.
        turmas_data[nome_turma]["alunos"].remove(matricula)
        # Salva os dados de turmas atualizados.
        save_json(turmas_data, TURMAS_JSON_PATH)
        # Retorna um dicionário de sucesso.
        return {"status": "sucesso", "mensagem": f"Aluno com matrícula {matricula} removido da turma '{nome_turma}'."}

def get_turmas_existentes() -> list:
    """
    Objetivo: Fornecer uma lista de todos os nomes de turmas que existem no sistema.
    Esta função serve como um "getter" de dados, sem interação com o usuário.

    Returns:
        list: Uma lista de strings, onde cada string é o nome de uma turma existente.
    """
    # Carrega os dados de todas as turmas e retorna as chaves (nomes das turmas) como uma lista.
    turmas_data = load_json(TURMAS_JSON_PATH, {})
    return list(turmas_data.keys())

def get_listas_existentes() -> list:
    """
    Objetivo: Fornecer uma lista de todos os nomes de arquivos JSON de listas de exercícios existentes.
    Esta função serve como um "getter" de dados, sem interação com o usuário.

    Returns:
        list: Uma lista de strings, onde cada string é o nome de um arquivo JSON de lista de exercícios.
    """
    # Lista todos os arquivos no diretório de listas de exercícios e filtra os que terminam com '.json'.
    # Isso assume que todos os JSONs neste diretório são listas de exercícios válidas.
    return [f for f in os.listdir(LISTAS_DE_EXERCICIOS_DIR) if f.endswith(".json")]

def visualiza_turma(nome_turma: str) -> dict:
    """
    Objetivo: Retornar uma visão detalhada de uma turma específica, incluindo seus alunos matriculados,
              listas de exercícios associadas e o índice de acertos consolidado para cada lista.
    Esta função é um "getter" de dados complexos, não imprime informações diretamente para o usuário.

    Args:
        nome_turma (str): O nome da turma cujos detalhes serão visualizados.

    Returns:
        dict: Um dicionário com o 'status' da operação ("sucesso" ou "erro"),
              e os detalhes da turma (nome, lista de alunos, e lista de listas com estatísticas de acerto),
              ou uma mensagem de erro se a turma não for encontrada.
    """
    # Carrega os dados de turmas, usuários (para nomes de alunos) e progresso de alunos.
    turmas_data = load_json(TURMAS_JSON_PATH, {})
    usuarios_data = load_json(USUARIOS_JSON_PATH, {})
    progresso_alunos_data = load_json(PROGRESO_ALUNOS_JSON_PATH, {})

    # Verifica se a turma especificada existe.
    if nome_turma not in turmas_data:
        return {"status": "erro", "mensagem": f"Erro: Turma '{nome_turma}' não encontrada."}

    dados_turma = turmas_data[nome_turma]
    
    # --- Detalhes dos Alunos na Turma ---
    alunos_na_turma_detalhes = []
    alunos_na_turma_ids = dados_turma.get("alunos", []) # Obtém a lista de matrículas de alunos na turma.
    if alunos_na_turma_ids:
        for matricula in alunos_na_turma_ids:
            # Para cada matrícula, busca o nome do aluno no USUARIOS_JSON_PATH.
            aluno_info = usuarios_data.get(str(matricula))
            nome_aluno = aluno_info.get('nome', 'Nome Desconhecido') if aluno_info else 'Nome Desconhecido'
            alunos_na_turma_detalhes.append({"matricula": matricula, "nome": nome_aluno})

    # --- Detalhes das Listas de Exercícios e Índice de Acertos ---
    listas_associadas_detalhes = []
    listas_da_turma_nomes = dados_turma.get("listas", []) # Obtém os nomes dos arquivos das listas associadas à turma.
    
    if listas_da_turma_nomes:
        for nome_lista in listas_da_turma_nomes:
            # Inicializa um dicionário para os detalhes de cada lista.
            lista_detalhe = {"nome_lista": nome_lista, "indice_acerto": "N/A", "msg_acerto": "", "num_alunos_contribuintes": 0}
            
            # Carrega os exercícios da lista específica para obter as respostas corretas.
            lista_full_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_lista)
            exercicios_da_lista = load_json(lista_full_path, [])
            
            # Se a lista de exercícios estiver vazia, adiciona uma mensagem e continua para a próxima lista.
            if not exercicios_da_lista:
                lista_detalhe["msg_acerto"] = "(Lista vazia ou não carregada)"
                listas_associadas_detalhes.append(lista_detalhe)
                continue

            total_acertos_geral = 0 # Contador para o total de acertos em todas as respostas da turma para esta lista.
            total_respostas_contabilizadas_geral = 0 # Contador para o total de respostas válidas (questões com resp. correta definida) dadas.
            total_alunos_que_responderam = 0 # Contador de alunos que contribuíram com respostas.

            # Itera sobre cada aluno na turma para somar seus acertos na lista.
            for matricula_aluno in alunos_na_turma_ids:
                matricula_str = str(matricula_aluno)
                # Obtém o progresso específico do aluno para esta lista.
                aluno_progresso = progresso_alunos_data.get(matricula_str, {}).get(nome_lista, {})
                
                # Considera apenas os alunos que iniciaram ou completaram a lista.
                if aluno_progresso.get('status') == 'completo' or aluno_progresso.get('progresso', 0) > 0:
                    total_alunos_que_responderam += 1
                    respostas_dadas_aluno = aluno_progresso.get('respostas', {})
                    
                    # Itera sobre cada exercício da lista para comparar com as respostas do aluno.
                    for idx_ex, ex_data in enumerate(exercicios_da_lista):
                        resp_correta = ex_data.get('RespostaCorreta', '').lower()
                        # Só contabiliza se a questão tiver uma resposta correta definida no JSON.
                        if resp_correta:
                            total_respostas_contabilizadas_geral += 1
                            resp_dada = respostas_dadas_aluno.get(str(idx_ex), '').lower() # Resposta do aluno para esta questão.
                            if resp_dada == resp_correta: # Compara a resposta do aluno (letra) com a correta (letra).
                                total_acertos_geral += 1

            # Calcula o índice de acerto da turma para esta lista, se houver respostas contabilizadas.
            if total_respostas_contabilizadas_geral > 0:
                indice_acerto = (total_acertos_geral / total_respostas_contabilizadas_geral) * 100
                lista_detalhe["indice_acerto"] = f"{indice_acerto:.2f}%" # Formata como porcentagem.
                lista_detalhe["msg_acerto"] = f"({total_acertos_geral} acertos em {total_respostas_contabilizadas_geral} respostas válidas de questões com resposta correta definida.)"
                lista_detalhe["num_alunos_contribuintes"] = total_alunos_que_responderam
            else:
                lista_detalhe["msg_acerto"] = "Nenhum aluno respondeu a esta lista ainda ou as questões não têm resposta correta definida."
            
            # Adiciona os detalhes da lista atual à lista geral de detalhes de listas.
            listas_associadas_detalhes.append(lista_detalhe)
    
    # Retorna um dicionário de sucesso com todos os detalhes coletados da turma.
    return {
        "status": "sucesso",
        "nome_turma": nome_turma,
        "alunos": alunos_na_turma_detalhes,
        "listas": listas_associadas_detalhes
    }


def passa_lista(nome_lista_json: str, turma: str) -> dict:
    """
    Objetivo: Associar uma lista de exercícios a uma turma.
    Esta função manipula os dados das turmas e não interage diretamente com o usuário.

    Args:
        nome_lista_json (str): O nome do arquivo JSON da lista de exercícios a ser associada.
        turma (str): O nome da turma à qual a lista será associada.

    Returns:
        dict: Um dicionário com o 'status' da operação ("sucesso", "erro" ou "aviso")
              e uma 'mensagem' descritiva do resultado.
    """
    # Carrega os dados de todas as turmas.
    turmas_data = load_json(TURMAS_JSON_PATH, {})

    # Verifica se a turma especificada existe.
    if turma not in turmas_data:
        return {"status": "erro", "mensagem": f"Turma '{turma}' não encontrada."}

    # Constrói o caminho completo para o arquivo da lista e verifica se ele existe no diretório.
    lista_full_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_lista_json)
    if not os.path.exists(lista_full_path):
        return {"status": "erro", "mensagem": f"O arquivo de lista de exercícios '{nome_lista_json}' não foi encontrado no diretório '{LISTAS_DE_EXERCICIOS_DIR}'."}

    # Garante que a estrutura da turma é válida para associar listas.
    if not isinstance(turmas_data[turma], dict) or "listas" not in turmas_data[turma]:
        turmas_data[turma] = {"alunos": [], "listas": []}
        save_json(turmas_data, TURMAS_JSON_PATH) # Salva a correção na estrutura da turma.
        return {"status": "aviso", "mensagem": f"Aviso: Estrutura da turma '{turma}' inválida. Tentando corrigir e associar lista."}

    # Verifica se a lista já está associada à turma.
    if nome_lista_json in turmas_data[turma]["listas"]:
        return {"status": "erro", "mensagem": f"A lista '{nome_lista_json}' já está associada à turma '{turma}'."}
    else:
        # Adiciona o nome da lista à lista de listas da turma.
        turmas_data[turma]["listas"].append(nome_lista_json)
        # Salva os dados de turmas atualizados.
        save_json(turmas_data, TURMAS_JSON_PATH)
        # Retorna um dicionário de sucesso.
        return {"status": "sucesso", "mensagem": f"Lista '{nome_lista_json}' associada com sucesso à turma '{turma}'."}