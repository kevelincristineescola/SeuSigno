"""Acesso ao SQLite: criação do banco, carga inicial e consultas."""
import sqlite3
from pathlib import Path

from flask import g

from seed import SIGNOS

BASE = Path(__file__).parent
CAMINHO_BD = BASE / "signos.db"

CLASSES_ELEMENTO = {"Fogo": "fogo", "Terra": "terra", "Ar": "ar", "Água": "agua"}


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(CAMINHO_BD)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_erro=None):
    conexao = g.pop("db", None)
    if conexao is not None:
        conexao.close()


def init_db():
    """Cria as tabelas e popula os signos se o banco ainda estiver vazio."""
    conexao = get_db()
    conexao.executescript((BASE / "schema.sql").read_text(encoding="utf-8"))
    total = conexao.execute("SELECT COUNT(*) FROM signos").fetchone()[0]
    if total == 0:
        linhas = [
            {**signo, "ordem": i, "simbolo": chr(0x2648 + i)}  # ♈ ... ♓
            for i, signo in enumerate(SIGNOS)
        ]
        conexao.executemany(
            """INSERT INTO signos
               (ordem, slug, nome, simbolo, inicio, fim, elemento, modalidade,
                regente, cor, pedra, palavras_chave, descricao, qualidades,
                desafios, compativeis)
               VALUES
               (:ordem, :slug, :nome, :simbolo, :inicio, :fim, :elemento,
                :modalidade, :regente, :cor, :pedra, :palavras_chave,
                :descricao, :qualidades, :desafios, :compativeis)""",
            linhas,
        )
        conexao.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()


def _mmdd_para_texto(mmdd):
    return f"{mmdd % 100:02d}/{mmdd // 100:02d}"


def _preparar(linha):
    signo = dict(linha)
    signo["periodo"] = f"{_mmdd_para_texto(signo['inicio'])} a {_mmdd_para_texto(signo['fim'])}"
    signo["classe"] = CLASSES_ELEMENTO[signo["elemento"]]
    for campo in ("palavras_chave", "qualidades", "desafios", "compativeis"):
        signo[campo] = [item.strip() for item in signo[campo].split(",")]
    return signo


def listar_signos():
    linhas = get_db().execute("SELECT * FROM signos ORDER BY ordem").fetchall()
    return [_preparar(linha) for linha in linhas]


def buscar_signo(slug):
    linha = get_db().execute("SELECT * FROM signos WHERE slug = ?", (slug,)).fetchone()
    return _preparar(linha) if linha else None


def buscar_signo_por_data(mes, dia):
    """Retorna o signo de quem nasceu em mes/dia.

    Se inicio <= fim, o período cabe no mesmo ano. Se inicio > fim
    (Capricórnio), ele cobre o fim de dezembro e o começo de janeiro.
    """
    mmdd = mes * 100 + dia
    linha = get_db().execute(
        """SELECT * FROM signos
           WHERE (inicio <= fim AND :md BETWEEN inicio AND fim)
              OR (inicio >  fim AND (:md >= inicio OR :md <= fim))""",
        {"md": mmdd},
    ).fetchone()
    return _preparar(linha) if linha else None


def registrar_consulta(signo_id):
    conexao = get_db()
    conexao.execute("INSERT INTO consultas (signo_id) VALUES (?)", (signo_id,))
    conexao.commit()


def total_consultas(signo_id):
    return get_db().execute(
        "SELECT COUNT(*) FROM consultas WHERE signo_id = ?", (signo_id,)
    ).fetchone()[0]
