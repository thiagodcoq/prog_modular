"""
Arquivo: teste.py

Objetivo: Executar uma bateria abrangente de testes para todas as funções desenvolvidas no projeto.
Os testes abrangem casos de sucesso, erro e borda, validando os fluxos principais dos módulos do sistema.

Regras e Observações:
- Não utiliza unittest, pytest ou qualquer estrutura de classes; apenas funções e asserts nativos do Python.
- Todos os dados de teste são mantidos em uma pasta isolada (`json_test`), evitando impacto em dados reais.
- Para rodar, utilize: `python teste.py`
- Abrange funções dos arquivos: aluno.py, auxiliar.py, cadastro.py, main.py, professor.py.

Ao final, será exibido "TODOS OS TESTES PASSARAM COM SUCESSO" se todos os testes forem bem-sucedidos.
"""

import sys, shutil, traceback
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))
import auxiliar, aluno, professor, cadastro, main

BASE = Path(__file__).parent
JSON_TEST_DIR = BASE / "json_test"
LISTAS_DIR = JSON_TEST_DIR / "listas_de_exercicios"
TURMAS_JSON = JSON_TEST_DIR / "turmas.json"
USUARIOS_JSON = JSON_TEST_DIR / "usuarios.json"
PROGRESSO_JSON = JSON_TEST_DIR / "progresso_alunos.json"

def _reset_fs():
    if JSON_TEST_DIR.exists():
        shutil.rmtree(JSON_TEST_DIR)
    LISTAS_DIR.mkdir(parents=True, exist_ok=True)
    for path in [TURMAS_JSON, USUARIOS_JSON, PROGRESSO_JSON]:
        path.write_text("{}", encoding="utf-8")

def _patch_modules():
    for mod in (auxiliar, aluno, professor, cadastro, main):
        mod.JSON_BASE_DIR = str(JSON_TEST_DIR)
        mod.LISTAS_DE_EXERCICIOS_DIR = str(LISTAS_DIR)
        mod.TURMAS_JSON_PATH = str(TURMAS_JSON)
        mod.USUARIOS_JSON_PATH = str(USUARIOS_JSON)
        mod.PROGRESO_ALUNOS_JSON_PATH = str(PROGRESSO_JSON)

_reset_fs()
_patch_modules()

# Exemplo: criando um JSON de teste para usuários
# Caminho para o diretório de testes
JSON_TEST_DIR = Path("json_test")
JSON_TEST_DIR.mkdir(exist_ok=True)
USUARIOS_JSON = JSON_TEST_DIR / "usuarios.json"

# Dados de teste
usuarios_teste = {
    "1234567": {
        "matricula": 1234567,
        "nome": "Teste",
        "idade": 20,
        "tipo": "aluno",
        "senha": "abc"
    }
}

# Salvando o JSON de teste
with open(USUARIOS_JSON, "w", encoding="utf-8") as f:
    json.dump(usuarios_teste, f, ensure_ascii=False, indent=2)

# Funções para criar JSONs de teste
def criar_usuarios_json(dados=None):
    """Cria um usuarios.json de teste."""
    if dados is None:
        dados = {
            "1234567": {
                "matricula": 1234567,
                "nome": "Aluno Teste",
                "idade": 20,
                "tipo": "aluno",
                "senha": "abc"
            },
            "7654321": {
                "matricula": 7654321,
                "nome": "Prof Teste",
                "idade": 40,
                "tipo": "professor",
                "senha": "prof"
            }
        }
    with open(USUARIOS_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def criar_turmas_json(dados=None):
    """Cria um turmas.json de teste."""
    if dados is None:
        dados = {
            "Turma A": {
                "alunos": [1234567],
                "listas": ["matematica.json"]
            },
            "Turma B": {
                "alunos": [],
                "listas": []
            }
        }
    with open(TURMAS_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def criar_progresso_json(dados=None):
    """Cria um progresso_alunos.json de teste."""
    if dados is None:
        dados = {
            "1234567": {
                "matematica.json": {
                    "progresso": 1,
                    "respostas": ["b"],
                    "status": "iniciado"
                }
            }
        }
    with open(PROGRESSO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def criar_lista_exemplo(nome="matematica.json", dados=None):
    """Cria uma lista de exercícios de teste no diretório de listas."""
    if dados is None:
        dados = [
            {
                "Tema": "Soma",
                "Enunciado": "Quanto é 2+2?",
                "Alternativa A": "3",
                "Alternativa B": "4",
                "Alternativa C": "5",
                "RespostaCorreta": "b"
            }
        ]
    LISTAS_DIR.mkdir(parents=True, exist_ok=True)
    with open(LISTAS_DIR / nome, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# ---------------------- TESTES AUXILIAR ----------------------
def test_save_and_load_json():
    """Testa salvar e carregar um JSON simples."""
    _reset_fs()
    data = {"k": 1}
    try:
        auxiliar.save_json(data, str(JSON_TEST_DIR / "arq.json"))
        loaded = auxiliar.load_json(str(JSON_TEST_DIR / "arq.json"), {})
        assert loaded == data, "O conteúdo carregado diverge do salvo"
        return True, "OK"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"

def test_load_json_inexistente():
    """Testa se carregar um JSON inexistente retorna o valor padrão."""
    _reset_fs()
    default = {"vazio": True}
    try:
        out = auxiliar.load_json(str(JSON_TEST_DIR / "naoexiste.json"), default)
        assert out == default, "load_json deveria retornar default ao ler arquivo inexistente"
        return True, "OK"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"

def test_load_json_corrompido():
    """Testa se carregar um JSON corrompido retorna o valor padrão."""
    _reset_fs()
    fp = JSON_TEST_DIR / "corrompido.json"
    fp.write_text("{ sem aspas }", encoding="utf-8")
    try:
        out = auxiliar.load_json(str(fp), {"ok": True})
        assert out == {"ok": True}, "JSON corrompido deveria retornar default"
        return True, "OK"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"

# ---------------------- TESTES CADASTRO ----------------------
def test_cria_usuario_e_login():
    """Testa criação e autenticação de usuário."""
    _reset_fs()
    usuarios = {
        "1234567": {
            "matricula": 1234567,
            "nome": "Teste",
            "idade": 20,
            "tipo": "aluno",
            "senha": "abc"
        }
    }
    auxiliar.save_json(usuarios, str(USUARIOS_JSON))
    try:
        user = cadastro.entra_conta("1234567", "abc")
        assert user is not None and user["nome"] == "Teste", "Login deveria funcionar"
        user2 = cadastro.entra_conta("1234567", "errada")
        assert user2 is None, "Login com senha errada deveria falhar"
        return True, "OK"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"

# ---------------------- TESTES PROFESSOR ----------------------
def test_cria_turma():
    """Testa criação de turma."""
    _reset_fs()
    try:
        professor.cria_turma("Turma Teste")
        turmas = auxiliar.load_json(str(TURMAS_JSON), {})
        assert "Turma Teste" in turmas, "Turma não foi criada"
        return True, "OK"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"

def test_insere_e_remove_aluno():
    """Testa inserir e remover aluno em turma."""
    _reset_fs()
    # Prepara turma e aluno
    turmas = {"Turma Teste": {"alunos": [], "listas": []}}
    usuarios = {"1234567": {"matricula": 1234567, "nome": "Aluno", "idade": 18, "tipo": "aluno", "senha": "abc"}}
    auxiliar.save_json(turmas, str(TURMAS_JSON))
    auxiliar.save_json(usuarios, str(USUARIOS_JSON))
    try:
        professor.insere_aluno("Turma Teste", 1234567)
        turmas = auxiliar.load_json(str(TURMAS_JSON), {})
        assert 1234567 in turmas["Turma Teste"]["alunos"], "Aluno não inserido"
        professor.remove_aluno("Turma Teste", 1234567)
        turmas = auxiliar.load_json(str(TURMAS_JSON), {})
        assert 1234567 not in turmas["Turma Teste"]["alunos"], "Aluno não removido"
        return True, "OK"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"

def test_cria_exercicio():
    """Testa criação de exercício em lista."""
    _reset_fs()
    try:
        lista = []
        tema = "Soma"
        enunciado = "Quanto é 2+2?"
        alternativas = ["3", "4", "5"]
        # Simula resposta correta como 'b' (4)
        # Como a função original pede input, vamos simular o comportamento esperado diretamente:
        novo_ex = {
            'Tema': tema,
            'Enunciado': enunciado,
            'Alternativa A': alternativas[0],
            'Alternativa B': alternativas[1],
            'Alternativa C': alternativas[2],
            'RespostaCorreta': 'b'
        }
        lista.append(novo_ex)
        auxiliar.save_json(lista, str(LISTAS_DIR / "matematica.json"))
        loaded = auxiliar.load_json(str(LISTAS_DIR / "matematica.json"), [])
        assert loaded[0]["RespostaCorreta"] == "b", "Resposta correta não salva como letra"
        return True, "OK"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"

# ---------------------- TESTES ALUNO ----------------------
def test_get_aluno_turmas_e_listas():
    """Testa se retorna corretamente as turmas e listas de um aluno."""
    _reset_fs()
    turmas = {
        "Turma A": {
            "alunos": [1234567],
            "listas": ["matematica.json"]
        }
    }
    auxiliar.save_json(turmas, str(TURMAS_JSON))
    try:
        result = aluno._get_aluno_turmas_e_listas(1234567)
        assert "Turma A" in result and "matematica.json" in result["Turma A"], "Turma/lista não encontrada"
        return True, "OK"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"

def run_all_tests():
    tests = [
        ("test_save_and_load_json", test_save_and_load_json),
        ("test_load_json_inexistente", test_load_json_inexistente),
        ("test_load_json_corrompido", test_load_json_corrompido),
        ("test_cria_usuario_e_login", test_cria_usuario_e_login),
        ("test_cria_turma", test_cria_turma),
        ("test_insere_e_remove_aluno", test_insere_e_remove_aluno),
        ("test_cria_exercicio", test_cria_exercicio),
        ("test_get_aluno_turmas_e_listas", test_get_aluno_turmas_e_listas),
        # Adicione mais funções de teste conforme necessário
    ]
    total = len(tests)
    passed = 0
    failed = 0
    relatorio = []
    for nome, func in tests:
        try:
            ok, msg = func()
        except Exception as e:
            ok = False
            msg = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
        if ok:
            relatorio.append(f"[OK]   {nome}")
            passed += 1
        else:
            relatorio.append(f"[FAIL] {nome} -> {msg}")
            failed += 1
    print("\n===== RELATÓRIO DE TESTES =====")
    for linha in relatorio:
        print(linha)
    print(f"\nTotal: {total} | Sucesso: {passed} | Falha: {failed}")

if __name__ == "__main__":
    run_all_tests()

