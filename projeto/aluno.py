import json
import os
from auxiliar import load_json, save_json, TURMAS_JSON_PATH, LISTAS_DE_EXERCICIOS_DIR, PROGRESO_ALUNOS_JSON_PATH

def _get_aluno_turmas_e_listas(matricula_aluno: int) -> dict:
    """
    Retorna as turmas e as listas de exercícios associadas ao aluno.
    Ex:
    {
        'Turma A': ['matematica.json', 'portugues.json'],
        'Turma B': []
    }
    """
    turmas_data = load_json(TURMAS_JSON_PATH, {})
    aluno_listas_por_turma = {}

    for nome_turma, dados_turma in turmas_data.items():
        if matricula_aluno in dados_turma.get("alunos", []):
            aluno_listas_por_turma[nome_turma] = dados_turma.get("listas", [])
    return aluno_listas_por_turma

def abrir_lista(matricula_aluno: int):
    """
    Objetivo: Abrir uma lista de exercícios para o aluno visualizar ou responder.
    Parametros: matricula_aluno (int): A matrícula do aluno logado.
    Retorno: Nenhum
    Descrição: Esta função permite que o aluno escolha uma lista de exercícios para visualizar/responder.
               Ela verifica as listas associadas às turmas do aluno, exibe os títulos e permite a seleção.
    """
    aluno_listas_por_turma = _get_aluno_turmas_e_listas(matricula_aluno)
    
    listas_disponiveis_para_aluno = []
    print("\n--- Listas de Exercício Disponíveis para Você ---")
    
    if not aluno_listas_por_turma:
        print("Você não está em nenhuma turma ou não há listas associadas às suas turmas.")
        return

    # Coleta todas as listas únicas disponíveis para o aluno, com sua turma de origem
    lista_idx = 1
    for turma, listas_da_turma in aluno_listas_por_turma.items():
        for nome_arquivo_lista in listas_da_turma:
            listas_disponiveis_para_aluno.append({'nome_arquivo': nome_arquivo_lista, 'turma': turma})
            print(f"{lista_idx} - {nome_arquivo_lista} (Turma: {turma})")
            lista_idx += 1
    
    if not listas_disponiveis_para_aluno:
        print("Não há listas de exercícios associadas às suas turmas no momento.")
        return

    try:
        escolha = int(input("Digite o número da lista que deseja abrir (ou 0 para voltar): "))
        if escolha == 0:
            return
        
        if 1 <= escolha <= len(listas_disponiveis_para_aluno):
            lista_escolhida_info = listas_disponiveis_para_aluno[escolha - 1]
            nome_arquivo_lista = lista_escolhida_info['nome_arquivo']
            turma_origem = lista_escolhida_info['turma']
            
            lista_full_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_arquivo_lista)
            exercicios = load_json(lista_full_path, [])

            if not exercicios:
                print(f"A lista '{nome_arquivo_lista}' está vazia ou não pôde ser carregada.")
                return

            print(f"\nAbrindo lista: {nome_arquivo_lista} (Turma: {turma_origem})")
            print("1. Visualizar Exercícios")
            print("2. Responder Exercícios")
            sub_escolha = input("Escolha uma opção: ")

            if sub_escolha == '1':
                print("\n--- Visualizando Exercícios ---")
                for i, ex in enumerate(exercicios):
                    print(f"\nExercício {i+1}:")
                    print(f"Tema: {ex.get('Tema', 'N/A')}")
                    print(f"Enunciado: {ex.get('Enunciado', 'N/A')}")
                    print(f"A) {ex.get('Alternativa A', 'N/A')}")
                    print(f"B) {ex.get('Alternativa B', 'N/A')}")
                    print(f"C) {ex.get('Alternativa C', 'N/A')}")
                input("\nPressione Enter para continuar...")
            elif sub_escolha == '2':
                responder_lista(matricula_aluno, nome_arquivo_lista, exercicios)
            else:
                print("Opção inválida.")
        else:
            print("Opção inválida. Digite um número válido.")

    except ValueError:
        print("Entrada inválida. Digite um número válido.")


def responder_lista(matricula_aluno: int, nome_lista_json: str, exercicios: list):
    """
    Objetivo: Permite ao aluno responder a uma lista de exercícios, salvando seu progresso.
    Parametros:
        matricula_aluno (int): Matrícula do aluno.
        nome_lista_json (str): Nome do arquivo JSON da lista de exercícios.
        exercicios (list): A lista de dicionários de exercícios.
    Retorno: Nenhum
    """
    progresso_alunos_data = load_json(PROGRESO_ALUNOS_JSON_PATH, {})
    
    matricula_str = str(matricula_aluno)

    if matricula_str not in progresso_alunos_data:
        progresso_alunos_data[matricula_str] = {}
    
    # Inicializa ou carrega o progresso do aluno para esta lista
    if nome_lista_json not in progresso_alunos_data[matricula_str]:
        progresso_alunos_data[matricula_str][nome_lista_json] = {
            'progresso': 0, # Começa do primeiro exercício (índice 0)
            'respostas': {},
            'status': 'iniciado'
        }
    
    # Lógica para permitir refazer a lista
    current_status = progresso_alunos_data[matricula_str][nome_lista_json].get('status', 'iniciado')
    if current_status == 'completo':
        print(f"A lista '{nome_lista_json}' já foi completada por você.")
        refazer = input("Deseja refazer esta lista? (s/n): ").lower() # Entrada case-insensitive
        if refazer == 's':
            progresso_alunos_data[matricula_str][nome_lista_json]['progresso'] = 0
            progresso_alunos_data[matricula_str][nome_lista_json]['respostas'] = {}
            progresso_alunos_data[matricula_str][nome_lista_json]['status'] = 'iniciado'
            save_json(progresso_alunos_data, PROGRESO_ALUNOS_JSON_PATH)
            print("Lista reiniciada com sucesso!")
        else:
            print("Voltando ao menu do aluno.")
            return

    # Carrega o ponto de partida
    indice_atual = progresso_alunos_data[matricula_str][nome_lista_json]['progresso']
    respostas_dadas = progresso_alunos_data[matricula_str][nome_lista_json]['respostas']

    print(f"\n--- Respondendo Lista: {nome_lista_json} ---")
    if indice_atual > 0 and indice_atual < len(exercicios): # Só informa se realmente está continuando
        print(f"Você parou no Exercício {indice_atual + 1}. Continuando a partir daqui.")
    
    for i in range(indice_atual, len(exercicios)):
        ex = exercicios[i]
        print(f"\nExercício {i+1} de {len(exercicios)}:")
        print(f"Tema: {ex.get('Tema', 'N/A')}")
        print(f"Enunciado: {ex.get('Enunciado', 'N/A')}")
        
        alternativas = [
            ex.get('Alternativa A', 'N/A'),
            ex.get('Alternativa B', 'N/A'),
            ex.get('Alternativa C', 'N/A')
        ]
        
        opcoes_validas = []
        for idx_alt, alt_text in enumerate(alternativas):
            if alt_text != 'N/A':
                letra_opcao = chr(65 + idx_alt)
                print(f"{letra_opcao}) {alt_text}")
                opcoes_validas.append(letra_opcao.lower())

        while True:
            resposta = input(f"Sua resposta ({'/'.join(opcoes_validas)} ou 'parar' para salvar e sair): ").strip().lower() # Entrada case-insensitive
            if resposta == 'parar':
                progresso_alunos_data[matricula_str][nome_lista_json]['progresso'] = i # Salva o índice do exercício atual
                save_json(progresso_alunos_data, PROGRESO_ALUNOS_JSON_PATH)
                print("Progresso salvo. Você pode continuar esta lista mais tarde.")
                return
            if resposta in opcoes_validas:
                respostas_dadas[str(i)] = resposta # Salva a resposta do exercício 'i'
                break
            else:
                print("Opção inválida. Tente novamente.")
        
        progresso_alunos_data[matricula_str][nome_lista_json]['progresso'] = i + 1
        save_json(progresso_alunos_data, PROGRESO_ALUNOS_JSON_PATH)

    progresso_alunos_data[matricula_str][nome_lista_json]['status'] = 'completo'
    save_json(progresso_alunos_data, PROGRESO_ALUNOS_JSON_PATH)
    print("\nVocê completou esta lista de exercícios!")

    # Cálculo dos resultados
    acertos = 0
    erros = 0
    nao_respondidas = 0
    erros_detalhes = []

    for i, ex in enumerate(exercicios):
        resposta_aluno = respostas_dadas.get(str(i))
        resposta_correta = ex.get('RespostaCorreta', '').lower()

        if resposta_aluno is None:
            nao_respondidas += 1
        elif resposta_aluno == resposta_correta:
            acertos += 1
        else:
            erros += 1
            erros_detalhes.append({
                'exercicio': i + 1,
                'tema': ex.get('Tema', 'N/A'),
                'enunciado': ex.get('Enunciado', 'N/A'),
                'sua_resposta': resposta_aluno.upper(),
                'resposta_correta': resposta_correta.upper()
            })

    print("\n--- Resultados Finais ---")
    print(f"Total de Questões: {len(exercicios)}")
    print(f"Acertos: {acertos}")
    print(f"Erros: {erros}")
    print(f"Não Respondidas: {nao_respondidas}")

    if erros > 0:
        print("\n--- Detalhes dos Erros ---")
        for erro in erros_detalhes:
            print(f"\nExercício {erro['exercicio']}:")
            print(f"Tema: {erro['tema']}")
            print(f"Enunciado: {erro['enunciado']}")
            print(f"Sua Resposta: {erro['sua_resposta']}")
            print(f"Resposta Correta: {erro['resposta_correta']}")

    input("\nPressione Enter para continuar...")


def revisar_lista(matricula_aluno: int):
    """Revisa as listas respondidas pelo aluno, mostrando suas respostas e as corretas."""
    print("\n--- Revisar Lista ---")
    progresso_alunos_data = load_json(PROGRESO_ALUNOS_JSON_PATH, {})
    matricula_str = str(matricula_aluno)

    if matricula_str not in progresso_alunos_data or not progresso_alunos_data[matricula_str]:
        print("Você ainda não respondeu nenhuma lista.")
        return
    
    print("Suas listas respondidas/em progresso:")
    listas_do_aluno = []
    idx = 1
    for nome_lista, dados_progresso in progresso_alunos_data[matricula_str].items():
        status = "Completo" if dados_progresso.get('status') == 'completo' else "Em Progresso"
        print(f"{idx} - {nome_lista} ({status})")
        listas_do_aluno.append({'nome_lista': nome_lista, 'dados': dados_progresso})
        idx += 1
    
    if not listas_do_aluno:
        print("Nenhuma lista encontrada para revisão.")
        return

    try:
        escolha = int(input("Digite o número da lista para revisar (ou 0 para voltar): "))
        if escolha == 0:
            return
        if 1 <= escolha <= len(listas_do_aluno):
            lista_info = listas_do_aluno[escolha - 1]
            nome_lista_json = lista_info['nome_lista']
            respostas_aluno = lista_info['dados'].get('respostas', {})

            lista_full_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_lista_json)
            exercicios = load_json(lista_full_path, [])

            if not exercicios:
                print(f"Não foi possível carregar os exercícios para a lista '{nome_lista_json}'.")
                return

            print(f"\n--- Revisão da Lista: {nome_lista_json} ---")
            for i, ex in enumerate(exercicios):
                resposta_dada = respostas_aluno.get(str(i), "Não respondida")
                resposta_correta = ex.get('RespostaCorreta', '').lower()

                print(f"\nExercício {i+1}:")
                print(f"Tema: {ex.get('Tema', 'N/A')}")
                print(f"Enunciado: {ex.get('Enunciado', 'N/A')}")
                print(f"A) {ex.get('Alternativa A', 'N/A')}")
                print(f"B) {ex.get('Alternativa B', 'N/A')}")
                print(f"C) {ex.get('Alternativa C', 'N/A')}")
                
                print(f"Sua Resposta: {resposta_dada.upper()}")
                if resposta_correta: # Se houver uma resposta correta definida
                    print(f"Resposta Correta: {resposta_correta.upper()}")
                    if resposta_dada == resposta_correta:
                         print("Status: Correta")
                    elif resposta_dada == "não respondida":
                         print("Status: Não Respondida")
                    else:
                         print("Status: Incorreta")
                else:
                    print("Status: Resposta correta não definida para este exercício.")
            input("\nPressione Enter para continuar...")
        else:
            print("Opção inválida.")
    except ValueError:
        print("Entrada inválida. Digite um número válido.")