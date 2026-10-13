from flask import Blueprint, request, redirect, url_for, session
from db import db
from model import Publi

publi = Blueprint("publi", __name__)


@publi.route("/create", methods=["POST"])
def create():
    if 'usuario_id' not in session:
        return redirect(url_for("home"))

    titulo = request.form.get("titulo")
    texto = request.form.get("conteudo")
    
    usu_id = session['usuario_id']

    nova_publi = Publi(
        titulo_publi=titulo,
        texto_publi=texto,
        usu_id=usu_id
    )

    db.session.add(nova_publi)
    db.session.commit()

    return redirect(url_for("index"))