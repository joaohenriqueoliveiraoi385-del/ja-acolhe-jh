from flask import Blueprint, render_template, redirect, url_for, session
from db import db
from model import Not

not_bp = Blueprint("notificacoes", __name__, url_prefix="/notificacoes")


@not_bp.route("/")
def listar():
    if 'usuario_id' not in session:
        return redirect(url_for("home"))

    usuario_id = session['usuario_id']
    notificacoes = (
        Not.query.filter_by(usu_id=usuario_id)
        .order_by(Not.data_not.desc())
        .all()
    )

    for n in notificacoes:
        if not n.lida:
            n.lida = True
    db.session.commit()

    return render_template("notificacoes.html", notificacoes=notificacoes)


@not_bp.route("/limpar", methods=["POST"])
def limpar():
    if 'usuario_id' not in session:
        return redirect(url_for("home"))

    usuario_id = session['usuario_id']
    Not.query.filter_by(usu_id=usuario_id).delete()
    db.session.commit()

    return redirect(url_for("notificacoes.listar"))