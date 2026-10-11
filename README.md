# Meu Signo

Página web para descobrir o signo a partir da data de nascimento.
Feita com **Flask**, **SQLite**, **Bootstrap 5** e CSS próprio.

## Como funciona

1. Na página inicial (`/`) a pessoa informa a data de nascimento.
2. O formulário envia um `POST` para `/descobrir`, que valida a data, busca o signo no banco e **redireciona** para `/signo/<slug>`.
3. A página do signo mostra período, elemento, modalidade, planeta regente, cor, pedra, qualidades, pontos de atenção e signos compatíveis.

A roda do zodíaco também é navegável: cada símbolo abre o perfil do signo.

## Rodando

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abra http://127.0.0.1:5000. O arquivo `signos.db` é criado e populado na primeira execução.

## Estrutura

```
app.py            rotas (início, descobrir, signo, 404)
db.py             conexão SQLite, carga inicial e consultas
schema.sql        tabelas signos e consultas
seed.py           dados dos 12 signos
templates/        base, início, signo, 404 e a roda (_roda.html)
static/css/       style.css (estilos próprios sobre o Bootstrap)
```

## Banco de dados

- `signos`: dados de cada signo. O período é guardado como `MMDD` (21/03 vira `321`). Capricórnio atravessa o ano (`1222` até `119`), e a consulta SQL trata esse caso.
- `consultas`: um registro por signo descoberto, sem guardar a data de nascimento. Alimenta o contador no fim da página do signo.

