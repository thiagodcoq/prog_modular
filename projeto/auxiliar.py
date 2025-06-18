import json  # Importa o módulo 'json' para lidar com a serialização e desserialização de dados JSON.
import os    # Importa o módulo 'os' para interagir com o sistema operacional, especialmente para manipulação de caminhos de arquivo e diretórios.

# --- Configuração de Caminhos de Arquivos e Diretórios ---
# Este módulo centraliza a definição dos caminhos para todos os arquivos JSON usados pelo sistema.
# Isso torna a gestão de arquivos mais organizada e fácil de manter.

# Define a pasta base onde todos os arquivos JSON do sistema serão armazenados.
# Por exemplo, se o seu script está em 'projeto/', os JSONs ficarão em 'projeto/json/'.
JSON_BASE_DIR = "json"

# Constrói o caminho completo para o diretório onde as listas de exercícios serão salvas.
# Ex: 'json/listas_de_exercicios/'
LISTAS_DE_EXERCICIOS_DIR = os.path.join(JSON_BASE_DIR, "listas_de_exercicios")

# Constrói o caminho completo para o arquivo JSON que armazena os dados das turmas.
# Ex: 'json/turmas.json'
TURMAS_JSON_PATH = os.path.join(JSON_BASE_DIR, "turmas.json")

# Constrói o caminho completo para o arquivo JSON que armazena os dados dos usuários (alunos e professores).
# Ex: 'json/usuarios.json'
USUARIOS_JSON_PATH = os.path.join(JSON_BASE_DIR, "usuarios.json")

# Constrói o caminho completo para o arquivo JSON que armazena o progresso dos alunos nas listas de exercícios.
# Ex: 'json/progresso_alunos.json'
PROGRESO_ALUNOS_JSON_PATH = os.path.join(JSON_BASE_DIR, "progresso_alunos.json")

# --- Funções Auxiliares para Manipulação de Arquivos ---

def _ensure_dir_exists(path: str):
    """
    Objetivo: Garante que um diretório específico exista. Se o diretório não existir, ele é criado.
    Esta é uma função auxiliar interna (indicada pelo '_') e não deve ser chamada diretamente de fora do módulo.

    Args:
        path (str): O caminho completo para o diretório a ser verificado/criado.

    Returns:
        None: A função não retorna valor; ela executa uma ação (cria o diretório se necessário).
    """
    # Verifica se o 'path' não é uma string vazia. Isso evita tentar criar um diretório com nome vazio,
    # o que pode ocorrer se os.path.dirname() for chamado em um nome de arquivo sem um caminho de diretório.
    if path:
        # os.makedirs() cria todos os diretórios intermediários necessários.
        # exist_ok=True evita um erro se o diretório já existir.
        os.makedirs(path, exist_ok=True)

def load_json(file_path: str, default_data: any = None) -> any:
    """
    Objetivo: Carregar dados de um arquivo JSON.
    Esta função é robusta: se o arquivo não existir, estiver vazio ou corrompido,
    ela retorna dados padrão, evitando erros no programa principal.

    Args:
        file_path (str): O caminho completo para o arquivo JSON a ser lido.
        default_data (any, optional): Os dados a serem retornados se o arquivo não puder ser lido.
                                      Se None, um padrão sensato ({} para objetos JSON, [] para listas JSON)
                                      é inferido com base no nome do arquivo. Padrão para None.

    Returns:
        any: O conteúdo do arquivo JSON (como um dicionário ou lista Python),
             ou os 'default_data' se houver algum problema.
    """
    # Se 'default_data' não for especificado, a função tenta inferir um valor padrão.
    if default_data is None:
        if file_path.endswith(".json"):
            # Para arquivos que esperamos serem dicionários JSON (como turmas, usuários, progresso),
            # o padrão é um dicionário vazio.
            if "turmas.json" in file_path or "usuarios.json" in file_path or "progresso_alunos.json" in file_path:
                default_data = {}
            # Para outros JSONs (assumidos como listas de exercícios), o padrão é uma lista vazia.
            else:
                default_data = []
        else:
            # Padrão genérico caso o nome do arquivo não termine em .json.
            default_data = {}

    # Extrai o caminho do diretório do 'file_path'.
    dir_path = os.path.dirname(file_path)
    # Garante que o diretório pai do arquivo exista antes de tentar carregar ou criar o arquivo.
    if dir_path:
        _ensure_dir_exists(dir_path)

    # Verifica se o arquivo não existe ou se está vazio.
    # os.stat(file_path).st_size == 0 verifica se o arquivo tem 0 bytes (está vazio).
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return default_data # Se não existe ou está vazio, retorna os dados padrão.

    try:
        # Tenta abrir o arquivo em modo de leitura ('r') com codificação UTF-8 para suportar caracteres especiais.
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f) # Carrega e retorna o conteúdo JSON.
    except json.JSONDecodeError:
        # Captura erros se o arquivo JSON estiver malformado ou corrompido.
        print(f"Erro: Arquivo JSON corrompido ou inválido: {file_path}. Retornando dados padrão.")
        return default_data # Em caso de erro de decodificação, retorna dados padrão.
    except IOError as e:
        # Captura outros erros de I/O (entrada/saída), como permissão negada.
        print(f"Erro ao ler o arquivo {file_path}: {e}")
        return default_data # Em caso de erro de I/O, retorna dados padrão.

def save_json(data: any, file_path: str):
    """
    Objetivo: Salvar dados Python (dicionários, listas) em um arquivo JSON.
    Esta função garante que o diretório de destino exista antes de tentar salvar.

    Args:
        data (any): Os dados Python a serem salvos (geralmente um dicionário ou lista).
        file_path (str): O caminho completo para o arquivo JSON onde os dados serão gravados.

    Returns:
        None: A função não retorna valor; ela executa uma ação (salva o arquivo) e imprime mensagens de erro se falhar.
    """
    # Extrai o caminho do diretório do 'file_path'.
    dir_path = os.path.dirname(file_path)
    # Garante que o diretório de destino exista antes de tentar salvar o arquivo.
    # A função _ensure_dir_exists() já trata o caso de 'dir_path' ser uma string vazia (diretório atual).
    _ensure_dir_exists(dir_path)
    
    try:
        # Tenta abrir o arquivo em modo de escrita ('w') com codificação UTF-8.
        with open(file_path, 'w', encoding='utf-8') as f:
            # json.dump() escreve os dados no arquivo.
            # ensure_ascii=False permite que caracteres não-ASCII (como acentos) sejam gravados diretamente.
            # indent=4 formata o JSON com indentação de 4 espaços, tornando-o legível.
            json.dump(data, f, ensure_ascii=False, indent=4)
        # Uma mensagem de sucesso pode ser adicionada aqui para depuração, mas foi comentada para evitar poluição no console.
        # print(f"Dados salvos com sucesso em: {file_path}")
    except IOError as e:
        # Captura erros de I/O (ex: permissão negada, disco cheio) durante a gravação.
        print(f"Erro ao salvar o arquivo {file_path}: {e}")