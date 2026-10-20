from flask import Blueprint, render_template, request, redirect, url_for, session
from db import db
from model import Usu

Usu_bp = Blueprint("usu", __name__)


@Usu_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        nome = (request.form.get("nome") or "").strip()
        gmail = (request.form.get("gmail") or "").strip()
        senha = (request.form.get("senha") or "").strip()

        print("--- TENTATIVA DE CADASTRO ---")
        print(f"Nome: '{nome}' | E-mail: '{gmail}'")

        if not nome or not gmail or not senha:
            print("❌ Campos obrigatórios não preenchidos.")
            return redirect(url_for("usu.create"))

        usuario_existente = Usu.query.filter_by(gmail=gmail).first()
        if usuario_existente:
            print(f"⚠️ E-mail '{gmail}' já cadastrado!")
            return redirect(url_for("home"))

        novo_usuario = Usu(nome=nome, gmail=gmail, senha=senha)
        
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            print(f"✅ Usuário '{nome}' (ID: {novo_usuario.id_usu}) cadastrado com sucesso!")
            
            # Login automático após o cadastro
            session['usuario_id'] = novo_usuario.id_usu
            session['usuario_nome'] = novo_usuario.nome
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao salvar usuário no banco: {e}")
            return redirect(url_for("usu.create"))

    return render_template("cadastro.html")


@Usu_bp.route("/login", methods=["POST"])
def login():
    gmail = (request.form.get("gmail") or "").strip()
    senha = (request.form.get("senha") or "").strip()

    print("--- TENTATIVA DE LOGIN ---")
    print(f"E-mail recebido: '{gmail}'")

    usuario = Usu.query.filter_by(gmail=gmail, senha=senha).first()

    if usuario:
        print(f"✅ Login bem-sucedido: {usuario.nome} (ID: {usuario.id_usu})")
        session['usuario_id'] = usuario.id_usu
        session['usuario_nome'] = usuario.nome
        return redirect(url_for("index"))
    else:
        print("❌ Login falhou: e-mail ou senha não coincidem.")
        return redirect(url_for("home"))


@Usu_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))