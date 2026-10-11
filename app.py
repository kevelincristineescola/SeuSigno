import os
from datetime import date, datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for

import db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
db.init_app(app)


@app.route("/")
def index():
    return render_template(
        "index.html",
        signos=db.listar_signos(),
        hoje=date.today().isoformat(),
        giro=0,
        ativo=None,
    )


@app.post("/descobrir")
def descobrir():
    texto = request.form.get("data_nascimento", "").strip()
    try:
        nascimento = datetime.strptime(texto, "%Y-%m-%d").date()
    except ValueError:
        flash("Informe uma data de nascimento válida.", "erro")
        return redirect(url_for("index"))

    if nascimento > date.today() or nascimento.year < 1900:
        flash("A data deve estar entre 01/01/1900 e hoje.", "erro")
        return redirect(url_for("index"))

    signo = db.buscar_signo_por_data(nascimento.month, nascimento.day)
    db.registrar_consulta(signo["id"])
    flash(nascimento.strftime("%d/%m/%Y"), "nascimento")
    return redirect(url_for("signo", slug=signo["slug"]))


@app.route("/signo/<slug>")
def signo(slug):
    atual = db.buscar_signo(slug)
    if atual is None:
        abort(404)

    signos = db.listar_signos()
    por_slug = {s["slug"]: s for s in signos}
    compativeis = [por_slug[c] for c in atual["compativeis"]]

    # Gira a roda pelo menor caminho para deixar o signo no topo.
    ordem = atual["ordem"]
    giro = -ordem * 30 if ordem <= 6 else (12 - ordem) * 30

    return render_template(
        "signo.html",
        signo=atual,
        signos=signos,
        compativeis=compativeis,
        total=db.total_consultas(atual["id"]),
        giro=giro,
        ativo=atual["slug"],
    )


@app.errorhandler(404)
def nao_encontrado(_erro):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
