import json
import os

# Caminhos dos arquivos JSON que serão usados por professor.py
LISTAS_DE_EXERCICIOS_DIR = "listas_de_exercicios" # Diretório para guardar os arquivos de listas
TURMAS_JSON_PATH = "turmas.json"

def _ensure_dir_exists(path: str):
    """Garante que o diretório especificado existe. Se não existir, ele é criado."""
    os.makedirs(path, exist_ok=True)

def load_json(file_path: str, default_data: any = None) -> any:
    """
    Carrega dados de um arquivo JSON. Se o arquivo não existir ou estiver vazio,
    retorna os dados padrão fornecidos.
    """
    # Define um valor padrão mais adequado para listas (lista vazia) ou dicionários (dicionário vazio)
    if default_data is None:
        if file_path.endswith(".json"):
            if "turmas.json" in file_path:
                default_data = {}
            else: # Assumimos que é uma lista de exercícios
                default_data = []
        else:
            default_data = {} # Padrão genérico

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
    _ensure_dir_exists(os.path.dirname(file_path))
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Dados salvos com sucesso em: {file_path}")
    except IOError as e:
        print(f"Erro ao salvar o arquivo {file_path}: {e}")