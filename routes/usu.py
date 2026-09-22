from flask import Blueprint, redirect, request, url_for

from db import db
from model import Usu


Usu_bp = Blueprint("usu", __name__)


@Usu_bp.route("/create", methods=["POST"])
def create():
    nome = request.form["nome"]
    gmail = request.form["gmail"]
    senha = request.form["senha"]

    usuario_existente = Usu.query.filter_by(gmail=gmail).first()

    if usuario_existente:
        return redirect(url_for("index"))

    novo_usuario = Usu(
        nome=nome,
        gmail=gmail,
        senha=senha
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for("index"))