from flask import Blueprint, render_template, request, redirect, url_for, session
from db import db
from model import Usu

Usu_bp = Blueprint("usu", __name__)


@Usu_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        nome = request.form.get("nome")
        gmail = request.form.get("gmail")
        senha = request.form.get("senha")

        usuario_existente = Usu.query.filter_by(gmail=gmail).first()
        if usuario_existente:
            return redirect(url_for("usu.create"))

        novo_usuario = Usu(nome=nome, gmail=gmail, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("cadastro.html")


@Usu_bp.route("/login", methods=["POST"])
def login():
    gmail = request.form.get("gmail")
    senha = request.form.get("senha")

    usuario = Usu.query.filter_by(gmail=gmail, senha=senha).first()

    if usuario:
        session['usuario_id'] = usuario.id_usu
        session['usuario_nome'] = usuario.nome
        return redirect(url_for("index"))
    else:
        return redirect(url_for("home"))