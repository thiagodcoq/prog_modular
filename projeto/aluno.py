import json  # Módulo para trabalhar com dados JSON (serialização/desserialização)
import os    # Módulo para interagir com o sistema operacional (e.g., caminhos de arquivo)
from auxiliar import load_json, save_json, TURMAS_JSON_PATH, LISTAS_DE_EXERCICIOS_DIR, PROGRESO_ALUNOS_JSON_PATH
# Importa funções auxiliares e caminhos de arquivos JSON de configuração do sistema.

def _get_aluno_turmas_e_listas(matricula_aluno: int) -> dict:
    """
    Função auxiliar interna (indicado pelo '_').
    Objetivo: Buscar as turmas em que um aluno está matriculado e as listas de exercícios associadas a essas turmas.

    Args:
        matricula_aluno (int): A matrícula do aluno para o qual buscar turmas e listas.

    Returns:
        dict: Um dicionário onde as chaves são os nomes das turmas e os valores são listas
              dos nomes dos arquivos JSON das listas de exercícios associadas a cada turma.
              Ex: {'Turma A': ['matematica.json', 'portugues.json'], 'Turma B': []}
    """
    # Carrega todos os dados de turmas do arquivo JSON de turmas.
    turmas_data = load_json(TURMAS_JSON_PATH, {})
    
    # Inicializa um dicionário para armazenar as turmas e listas do aluno específico.
    aluno_listas_por_turma = {}

    # Itera sobre cada turma no dicionário de turmas.
    for nome_turma, dados_turma in turmas_data.items():
        # Verifica se a matrícula do aluno está na lista de alunos da turma atual.
        # Usa .get("alunos", []) para garantir que não haverá erro se a chave 'alunos' não existir.
        if matricula_aluno in dados_turma.get("alunos", []):
            # Se o aluno estiver na turma, adiciona o nome da turma como chave e suas listas como valor.
            # Usa .get("listas", []) para garantir que não haverá erro se a chave 'listas' não existir.
            aluno_listas_por_turma[nome_turma] = dados_turma.get("listas", [])
            
    return aluno_listas_por_turma

def abrir_lista(matricula_aluno: int):
    """
    Objetivo: Permite ao aluno visualizar as listas de exercícios disponíveis ou iniciar/continuar a respondê-las.

    Args:
        matricula_aluno (int): A matrícula do aluno logado.

    Returns:
        None: Esta função não retorna valor; ela interage diretamente com o usuário via console.
    """
    # Obtém as turmas do aluno e as listas associadas a cada turma.
    aluno_listas_por_turma = _get_aluno_turmas_e_listas(matricula_aluno)
    
    listas_disponiveis_para_aluno = [] # Lista para armazenar informações das listas a serem exibidas.
    print("\n--- Listas de Exercício Disponíveis para Você ---")
    
    # Verifica se o aluno está em alguma turma ou se há listas associadas.
    if not aluno_listas_por_turma:
        print("Você não está em nenhuma turma ou não há listas associadas às suas turmas.")
        return

    # Coleta e exibe todas as listas únicas disponíveis para o aluno, indicando a turma de origem.
    lista_idx = 1 # Índice para a escolha do usuário.
    for turma, listas_da_turma in aluno_listas_por_turma.items():
        for nome_arquivo_lista in listas_da_turma:
            listas_disponiveis_para_aluno.append({'nome_arquivo': nome_arquivo_lista, 'turma': turma})
            print(f"{lista_idx} - {nome_arquivo_lista} (Turma: {turma})")
            lista_idx += 1
    
    # Se não houver nenhuma lista após a coleta, informa o usuário.
    if not listas_disponiveis_para_aluno:
        print("Não há listas de exercícios associadas às suas turmas no momento.")
        return

    try:
        # Solicita ao aluno que escolha uma lista pelo número.
        escolha = int(input("Digite o número da lista que deseja abrir (ou 0 para voltar): "))
        if escolha == 0:
            return # Se o aluno digitar 0, retorna ao menu anterior.
        
        # Valida a escolha do aluno.
        if 1 <= escolha <= len(listas_disponiveis_para_aluno):
            # Obtém as informações da lista escolhida.
            lista_escolhida_info = listas_disponiveis_para_aluno[escolha - 1]
            nome_arquivo_lista = lista_escolhida_info['nome_arquivo']
            turma_origem = lista_escolhida_info['turma']
            
            # Constrói o caminho completo para o arquivo JSON da lista de exercícios.
            lista_full_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_arquivo_lista)
            # Carrega os exercícios da lista. Retorna uma lista vazia se o arquivo não for encontrado/válido.
            exercicios = load_json(lista_full_path, [])

            # Verifica se a lista de exercícios está vazia.
            if not exercicios:
                print(f"A lista '{nome_arquivo_lista}' está vazia ou não pôde ser carregada.")
                return

            # Apresenta opções: visualizar ou responder a lista.
            print(f"\nAbrindo lista: {nome_arquivo_lista} (Turma: {turma_origem})")
            print("1. Visualizar Exercícios")
            print("2. Responder Exercícios")
            sub_escolha = input("Escolha uma opção: ")

            if sub_escolha == '1':
                # Opção de apenas visualizar os exercícios.
                print("\n--- Visualizando Exercícios ---")
                for i, ex in enumerate(exercicios):
                    print(f"\nExercício {i+1}:")
                    print(f"Tema: {ex.get('Tema', 'N/A')}")
                    print(f"Enunciado: {ex.get('Enunciado', 'N/A')}")
                    print(f"A) {ex.get('Alternativa A', 'N/A')}")
                    print(f"B) {ex.get('Alternativa B', 'N/A')}")
                    print(f"C) {ex.get('Alternativa C', 'N/A')}")
                input("\nPressione Enter para continuar...") # Pausa para o aluno ler.
            elif sub_escolha == '2':
                # Opção de responder os exercícios, chamando a função específica.
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
              Permite continuar de onde parou ou refazer a lista.
              Permite voltar para a questão anterior.
              Ao final, calcula e exibe o desempenho (acertos, erros, não respondidas).

    Args:
        matricula_aluno (int): Matrícula do aluno.
        nome_lista_json (str): Nome do arquivo JSON da lista de exercícios sendo respondida.
        exercicios (list): A lista de dicionários de exercícios carregada.

    Returns:
        None: Esta função não retorna valor; ela interage diretamente com o usuário.
    """
    # Carrega os dados de progresso de todos os alunos.
    progresso_alunos_data = load_json(PROGRESO_ALUNOS_JSON_PATH, {})
    
    matricula_str = str(matricula_aluno) # Converte a matrícula para string, pois é usada como chave no JSON.

    # Inicializa a estrutura de progresso para o aluno, se não existir.
    if matricula_str not in progresso_alunos_data:
        progresso_alunos_data[matricula_str] = {}
    
    # Inicializa a estrutura de progresso para a lista específica para o aluno, se não existir.
    if nome_lista_json not in progresso_alunos_data[matricula_str]:
        progresso_alunos_data[matricula_str][nome_lista_json] = {
            'progresso': 0, # Índice do próximo exercício a ser respondido (começa em 0).
            'respostas': {}, # Dicionário para armazenar as respostas dadas (chave: índice do exercício, valor: resposta do aluno).
            'status': 'iniciado' # Status da lista para o aluno ('iniciado' ou 'completo').
        }
    
    # Lógica para permitir refazer a lista se ela já estiver completa.
    current_status = progresso_alunos_data[matricula_str][nome_lista_json].get('status', 'iniciado')
    if current_status == 'completo':
        print(f"A lista '{nome_lista_json}' já foi completada por você.")
        refazer = input("Deseja refazer esta lista? (s/n): ").lower() # Entrada case-insensitive.
        if refazer == 's':
            # Reseta o progresso e as respostas para permitir que a lista seja refeita.
            progresso_alunos_data[matricula_str][nome_lista_json]['progresso'] = 0
            progresso_alunos_data[matricula_str][nome_lista_json]['respostas'] = {}
            progresso_alunos_data[matricula_str][nome_lista_json]['status'] = 'iniciado'
            save_json(progresso_alunos_data, PROGRESO_ALUNOS_JSON_PATH)
            print("Lista reiniciada com sucesso!")
        else:
            print("Voltando ao menu do aluno.")
            return # Sai da função se o aluno não quiser refazer.

    # Carrega o ponto de partida (próximo exercício a ser respondido).
    indice_atual = progresso_alunos_data[matricula_str][nome_lista_json]['progresso']
    respostas_dadas = progresso_alunos_data[matricula_str][nome_lista_json]['respostas']

    print(f"\n--- Respondendo Lista: {nome_lista_json} ---")
    # Informa se o aluno está continuando de onde parou.
    if indice_atual > 0 and indice_atual < len(exercicios):
        print(f"Você parou no Exercício {indice_atual + 1}. Continuando a partir daqui.")
    elif indice_atual == len(exercicios): # Caso a lista esteja 'completo' mas não foi reiniciada
        print("Esta lista já foi completada. Para refazê-la, selecione a opção novamente e escolha 's' para refazer.")
        input("Pressione Enter para voltar.")
        return

    # Loop principal para percorrer os exercícios.
    while indice_atual < len(exercicios):
        ex = exercicios[indice_atual] # Obtém o exercício atual.
        print(f"\nExercício {indice_atual + 1} de {len(exercicios)}:")
        print(f"Tema: {ex.get('Tema', 'N/A')}")
        print(f"Enunciado: {ex.get('Enunciado', 'N/A')}")
        
        # Extrai as alternativas do exercício.
        alternativas = [
            ex.get('Alternativa A', 'N/A'),
            ex.get('Alternativa B', 'N/A'),
            ex.get('Alternativa C', 'N/A')
        ]
        
        opcoes_validas = [] # Lista de letras válidas para as opções (e.g., 'a', 'b', 'c').
        # Exibe as alternativas formatadas e preenche as opções válidas.
        for idx_alt, alt_text in enumerate(alternativas):
            if alt_text != 'N/A': # Apenas exibe alternativas que têm conteúdo.
                letra_opcao = chr(65 + idx_alt) # Converte o índice (0, 1, 2) para letra (A, B, C).
                print(f"{letra_opcao}) {alt_text}")
                opcoes_validas.append(letra_opcao.lower()) # Adiciona a letra em minúsculo para validação.

        # Constrói o prompt de entrada, incluindo opções para 'voltar' e 'parar'.
        prompt_opcoes = f"Sua resposta ({'/'.join(opcoes_validas)}"
        if indice_atual > 0: # A opção 'voltar' só aparece se não for o primeiro exercício.
            prompt_opcoes += " ou 'voltar'"
        prompt_opcoes += " ou 'parar' para salvar e sair): "

        # Loop interno para garantir que o aluno insira uma resposta válida ou uma opção de controle.
        while True:
            resposta = input(prompt_opcoes).strip().lower() # Coleta a resposta, remove espaços e padroniza para minúsculas.
            
            if resposta == 'parar':
                # Salva o progresso e as respostas antes de sair.
                progresso_alunos_data[matricula_str][nome_lista_json]['progresso'] = indice_atual # Salva o índice da questão atual.
                save_json(progresso_alunos_data, PROGRESO_ALUNOS_JSON_PATH)
                print("Progresso salvo. Você pode continuar esta lista mais tarde.")
                return # Sai da função.
            
            if resposta == 'voltar' and indice_atual > 0:
                # Permite voltar à questão anterior.
                print("Voltando para a questão anterior...")
                indice_atual -= 1 # Decrementa o índice para retroceder.
                break # Sai do loop interno, o loop externo redesenhará a questão anterior.
            elif resposta == 'voltar' and indice_atual == 0:
                # Impede que o aluno volte além da primeira questão.
                print("Você já está na primeira questão. Não é possível voltar.")
            elif resposta in opcoes_validas:
                # Se a resposta é uma opção válida, salva-a e avança para a próxima questão.
                respostas_dadas[str(indice_atual)] = resposta # Salva a resposta do exercício atual.
                indice_atual += 1 # Incrementa o índice para a próxima questão.
                # Salva o progresso e as respostas após cada resposta para maior segurança.
                progresso_alunos_data[matricula_str][nome_lista_json]['progresso'] = indice_atual
                progresso_alunos_data[matricula_str][nome_lista_json]['respostas'] = respostas_dadas
                save_json(progresso_alunos_data, PROGRESO_ALUNOS_JSON_PATH)
                break # Sai do loop interno para o loop externo prosseguir.
            else:
                print("Opção inválida. Tente novamente.")
        
    # Se o loop 'while indice_atual < len(exercicios)' terminar, significa que todos os exercícios foram respondidos.
    progresso_alunos_data[matricula_str][nome_lista_json]['status'] = 'completo' # Marca a lista como completa.
    save_json(progresso_alunos_data, PROGRESO_ALUNOS_JSON_PATH) # Salva o status final.
    print("\nVocê completou esta lista de exercícios!")

    # --- Cálculo e Exibição dos Resultados Finais ---
    acertos = 0
    erros = 0
    nao_respondidas = 0
    erros_detalhes = [] # Lista para armazenar detalhes dos exercícios errados.

    for i, ex in enumerate(exercicios):
        resposta_aluno = respostas_dadas.get(str(i)) # Resposta que o aluno deu para este exercício (pode ser None se não respondeu).
        resposta_correta = ex.get('RespostaCorreta', '').lower() # A resposta correta (letra em minúsculo) salva no JSON.

        # Obtém as opções válidas (letras 'a', 'b', 'c') para este exercício, para ajudar na exibição do texto.
        opcoes_validas_ex = []
        for idx_alt, alt_text in enumerate([ex.get('Alternativa A', 'N/A'), ex.get('Alternativa B', 'N/A'), ex.get('Alternativa C', 'N/A')]):
            if alt_text != 'N/A':
                opcoes_validas_ex.append(chr(65+idx_alt).lower())

        if resposta_aluno is None:
            nao_respondidas += 1
        elif resposta_aluno == resposta_correta: # Compara a letra da resposta do aluno com a letra da resposta correta.
            acertos += 1
        else:
            erros += 1
            # Para exibir o texto completo da alternativa, não apenas a letra, recriamos a lista de textos.
            alternativas_ex_text = [ex.get('Alternativa A', ''), ex.get('Alternativa B', ''), ex.get('Alternativa C', '')]
            
            # Converte a letra da resposta do aluno para o texto da alternativa para exibição.
            sua_resposta_texto_detalhe = "N/A"
            if resposta_aluno in opcoes_validas_ex:
                idx_resp_aluno = opcoes_validas_ex.index(resposta_aluno)
                sua_resposta_texto_detalhe = alternativas_ex_text[idx_resp_aluno].upper()
            elif resposta_aluno == "não respondida": # Caso a resposta seja explicitamente 'não respondida'
                sua_resposta_texto_detalhe = "Não Respondida"
            else: # Caso de alguma resposta inválida salva (muito improvável agora, mas para robustez)
                sua_resposta_texto_detalhe = "Inválida"

            # Converte a letra da resposta correta para o texto da alternativa para exibição.
            resposta_correta_texto_detalhe = "N/A"
            if resposta_correta in opcoes_validas_ex:
                idx_resp_correta = opcoes_validas_ex.index(resposta_correta)
                resposta_correta_texto_detalhe = alternativas_ex_text[idx_resp_correta].upper()

            # Adiciona os detalhes do erro à lista de erros.
            erros_detalhes.append({
                'exercicio': i + 1,
                'tema': ex.get('Tema', 'N/A'),
                'enunciado': ex.get('Enunciado', 'N/A'),
                'sua_resposta': sua_resposta_texto_detalhe,
                'resposta_correta': resposta_correta_texto_detalhe
            })

    # Imprime o resumo dos resultados.
    print("\n--- Resultados Finais ---")
    print(f"Total de Questões: {len(exercicios)}")
    print(f"Acertos: {acertos}")
    print(f"Erros: {erros}")
    print(f"Não Respondidas: {nao_respondidas}")

    # Se houver erros, imprime os detalhes de cada um.
    if erros > 0:
        print("\n--- Detalhes dos Erros ---")
        for erro in erros_detalhes:
            print(f"\nExercício {erro['exercicio']}:")
            print(f"Tema: {erro['tema']}")
            print(f"Enunciado: {erro['enunciado']}")
            print(f"Sua Resposta: {erro['sua_resposta']}")
            print(f"Resposta Correta: {erro['resposta_correta']}")
            
    input("\nPressione Enter para continuar...") # Pausa para o aluno ler os resultados.


def revisar_lista(matricula_aluno: int):
    """
    Objetivo: Permite ao aluno revisar uma lista de exercícios que já respondeu (total ou parcialmente).
              Exibe a questão, a resposta dada pelo aluno, a resposta correta e o status (correta/incorreta/não respondida).

    Args:
        matricula_aluno (int): Matrícula do aluno.

    Returns:
        None: Esta função não retorna valor; interage diretamente com o usuário.
    """
    print("\n--- Revisar Lista ---")
    # Carrega os dados de progresso de todos os alunos.
    progresso_alunos_data = load_json(PROGRESO_ALUNOS_JSON_PATH, {})
    matricula_str = str(matricula_aluno)

    # Verifica se o aluno tem algum progresso registrado.
    if matricula_str not in progresso_alunos_data or not progresso_alunos_data[matricula_str]:
        print("Você ainda não respondeu nenhuma lista.")
        return
    
    print("Suas listas respondidas/em progresso:")
    listas_do_aluno = [] # Lista para exibir as opções de revisão.
    idx = 1 # Índice para a escolha do usuário.
    # Itera sobre as listas que o aluno iniciou ou completou.
    for nome_lista, dados_progresso in progresso_alunos_data[matricula_str].items():
        # Determina o status da lista para exibição.
        status = "Completo" if dados_progresso.get('status') == 'completo' else "Em Progresso"
        print(f"{idx} - {nome_lista} ({status})")
        listas_do_aluno.append({'nome_lista': nome_lista, 'dados': dados_progresso})
        idx += 1
    
    if not listas_do_aluno:
        print("Nenhuma lista encontrada para revisão.")
        return

    try:
        # Solicita a escolha da lista para revisão.
        escolha = int(input("Digite o número da lista para revisar (ou 0 para voltar): "))
        if escolha == 0:
            return # Volta ao menu do aluno.
        
        if 1 <= escolha <= len(listas_do_aluno):
            # Obtém as informações da lista escolhida para revisão.
            lista_info = listas_do_aluno[escolha - 1]
            nome_lista_json = lista_info['nome_lista']
            respostas_aluno = lista_info['dados'].get('respostas', {}) # Respostas dadas pelo aluno.

            # Carrega os exercícios da lista para ter o enunciado e as alternativas corretas.
            lista_full_path = os.path.join(LISTAS_DE_EXERCICIOS_DIR, nome_lista_json)
            exercicios = load_json(lista_full_path, [])

            if not exercicios:
                print(f"Não foi possível carregar os exercícios para a lista '{nome_lista_json}'.")
                return

            print(f"\n--- Revisão da Lista: {nome_lista_json} ---")
            # Itera sobre cada exercício para exibir a revisão.
            for i, ex in enumerate(exercicios):
                resposta_dada = respostas_aluno.get(str(i), "Não respondida") # Resposta do aluno.
                resposta_correta = ex.get('RespostaCorreta', '').lower() # Resposta correta do exercício.

                print(f"\nExercício {i+1}:")
                print(f"Tema: {ex.get('Tema', 'N/A')}")
                print(f"Enunciado: {ex.get('Enunciado', 'N/A')}")
                
                # Exibe as alternativas completas do exercício.
                alternativas_ex = [
                    ex.get('Alternativa A', 'N/A'),
                    ex.get('Alternativa B', 'N/A'),
                    ex.get('Alternativa C', 'N/A')
                ]
                print(f"A) {alternativas_ex[0]}")
                print(f"B) {alternativas_ex[1]}")
                print(f"C) {alternativas_ex[2]}")
                
                # Para converter a letra da resposta para o texto da alternativa para exibição.
                opcoes_validas_ex = [chr(65+j).lower() for j, alt_text in enumerate(alternativas_ex) if alt_text != 'N/A']

                # Formata a resposta do aluno para exibição (letra para texto da alternativa).
                sua_resposta_texto = "Não respondida"
                if resposta_dada in opcoes_validas_ex:
                    sua_resposta_texto = alternativas_ex[opcoes_validas_ex.index(resposta_dada)].upper()
                elif resposta_dada == "não respondida":
                    sua_resposta_texto = resposta_dada.upper()
                else:
                    sua_resposta_texto = "Resposta Inválida: " + resposta_dada.upper()

                # Formata a resposta correta para exibição (letra para texto da alternativa).
                resposta_correta_texto_ex = "Não Definida"
                if resposta_correta in opcoes_validas_ex:
                    resposta_correta_texto_ex = alternativas_ex[opcoes_validas_ex.index(resposta_correta)].upper()

                print(f"Sua Resposta: {sua_resposta_texto}")
                if resposta_correta: # Verifica se a resposta correta foi definida para o exercício.
                    print(f"Resposta Correta: {resposta_correta_texto_ex}")
                    # Compara a resposta do aluno (letra) com a resposta correta (letra).
                    if resposta_dada == resposta_correta:
                         print("Status: Correta")
                    elif resposta_dada == "não respondida":
                         print("Status: Não Respondida")
                    else:
                         print("Status: Incorreta")
                else:
                    print("Status: Resposta correta não definida para este exercício.")
            input("\nPressione Enter para continuar...") # Pausa para o aluno ler a revisão.
        else:
            print("Opção inválida.")
    except ValueError:
        print("Entrada inválida. Digite um número válido.")