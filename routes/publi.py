from flask import Blueprint, request, redirect, url_for, session
from db import db
from model import Publi, Curt, Coment

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


@publi.route("/curtir/<int:publi_id>", methods=["POST"])
def curtir(publi_id):
    if 'usuario_id' not in session:
        return redirect(url_for("home"))

    usu_id = session['usuario_id']

    
    curtida_existente = Curt.query.filter_by(id_publicacao=publi_id, usu_id=usu_id).first()

    if curtida_existente:
        db.session.delete(curtida_existente)
    else:
        nova_curtida = Curt(id_publicacao=publi_id, usu_id=usu_id)
        db.session.add(nova_curtida)

    db.session.commit()
    return redirect(url_for("index"))


@publi.route("/comentar/<int:publi_id>", methods=["POST"])
def comentar(publi_id):
    if 'usuario_id' not in session:
        return redirect(url_for("home"))

    texto_coment = request.form.get("texto_coment")
    usu_id = session['usuario_id']

    if texto_coment and texto_coment.strip():
       
        novo_comentario = Coment(
            texto_coment=texto_coment,
            id_publicacao=publi_id,
            usu_id=usu_id
        )
        db.session.add(novo_comentario)
        db.session.commit()

    return redirect(url_for("index"))