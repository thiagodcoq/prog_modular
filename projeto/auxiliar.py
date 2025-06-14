import json
import os

# Define a pasta base onde todos os JSONs serão salvos
JSON_BASE_DIR = "json"

# Caminhos dos arquivos JSON que serão usados por professor.py, cadastro.py e aluno.py
LISTAS_DE_EXERCICIOS_DIR = os.path.join(JSON_BASE_DIR, "listas_de_exercicios") # Diretório para guardar os arquivos de listas
TURMAS_JSON_PATH = os.path.join(JSON_BASE_DIR, "turmas.json")
USUARIOS_JSON_PATH = os.path.join(JSON_BASE_DIR, "usuarios.json")
PROGRESO_ALUNOS_JSON_PATH = os.path.join(JSON_BASE_DIR, "progresso_alunos.json")

def _ensure_dir_exists(path: str):
    """Garante que o diretório especificado existe. Se não existir, ele é criado."""
    if path: # Apenas tenta criar o diretório se o path não for vazio
        os.makedirs(path, exist_ok=True)

def load_json(file_path: str, default_data: any = None) -> any:
    """
    Carrega dados de um arquivo JSON. Se o arquivo não existir ou estiver vazio,
    retorna os dados padrão fornecidos.
    """
    if default_data is None:
        if file_path.endswith(".json"):
            # Ajustado para incluir progresso_alunos.json e turmas/usuarios como dicionários vazios por padrão
            if "turmas.json" in file_path or "usuarios.json" in file_path or "progresso_alunos.json" in file_path:
                default_data = {}
            else: # Assumimos que é uma lista de exercícios
                default_data = []
        else:
            default_data = {}

    dir_path = os.path.dirname(file_path)
    if dir_path: # Garante que o diretório exista antes de tentar carregar/criar o arquivo
        _ensure_dir_exists(dir_path)

    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return default_data
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Erro: Arquivo JSON corrompido ou inválido: {file_path}. Retornando dados padrão.")
        return default_data
    except IOError as e:
        print(f"Erro ao ler o arquivo {file_path}: {e}")
        return default_data

def save_json(data: any, file_path: str):
    """
    Salva dados em um arquivo JSON.
    Garante que o diretório pai do arquivo exista antes de tentar salvar.
    """
    dir_path = os.path.dirname(file_path)
    _ensure_dir_exists(dir_path) # _ensure_dir_exists já trata o caso de string vazia
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        # print(f"Dados salvos com sucesso em: {file_path}") # Comentado para evitar poluição no console
    except IOError as e:
        print(f"Erro ao salvar o arquivo {file_path}: {e}")