-- inicio e fim guardam a data no formato MMDD (ex.: 21/03 -> 321).
-- Capricórnio atravessa o ano: inicio (1222) > fim (119).
CREATE TABLE IF NOT EXISTS signos (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    ordem          INTEGER NOT NULL UNIQUE,
    slug           TEXT    NOT NULL UNIQUE,
    nome           TEXT    NOT NULL,
    simbolo        TEXT    NOT NULL,
    inicio         INTEGER NOT NULL,
    fim            INTEGER NOT NULL,
    elemento       TEXT    NOT NULL,
    modalidade     TEXT    NOT NULL,
    regente        TEXT    NOT NULL,
    cor            TEXT    NOT NULL,
    pedra          TEXT    NOT NULL,
    palavras_chave TEXT    NOT NULL,
    descricao      TEXT    NOT NULL,
    qualidades     TEXT    NOT NULL,
    desafios       TEXT    NOT NULL,
    compativeis    TEXT    NOT NULL
);

-- Guarda só qual signo foi descoberto (nunca a data de nascimento).
CREATE TABLE IF NOT EXISTS consultas (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    signo_id      INTEGER NOT NULL REFERENCES signos(id),
    consultado_em TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
