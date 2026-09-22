from flask import Blueprint, redirect, request, url_for

from db import db
from model import Publi, Usu


Publi_bp = Blueprint("publi", __name__)


@Publi_bp.route("/create", methods=["POST"])
def create():
    titulo = request.form["titulo"]
    conteudo = request.form["conteudo"]

    usuario = Usu.query.first()

    if usuario is None:
        return redirect(url_for("index"))

    nova_publicacao = Publi(
        titulo_publi=titulo,
        texto_publi=conteudo,
        usu_id=usuario.id_usu
    )

    db.session.add(nova_publicacao)
    db.session.commit()

    return redirect(url_for("index"))