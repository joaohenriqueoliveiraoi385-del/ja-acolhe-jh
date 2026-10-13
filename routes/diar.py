from flask import Blueprint, render_template, request, redirect, url_for, session
from db import db
from model import Diar

diar_bp = Blueprint("diar", __name__, url_prefix="/diario")


@diar_bp.route("/", methods=["GET"])
def index():
    
    if 'usuario_id' not in session:
        return redirect(url_for("home"))

    usu_id = session['usuario_id']
    
    
    diarios = Diar.query.filter_by(usu_id=usu_id).order_by(Diar.data_registro.desc()).all()

    return render_template("diario.html", diarios=diarios)


@diar_bp.route("/criar", methods=["POST"])
def criar():
    if 'usuario_id' not in session:
        return redirect(url_for("home"))

    humor = request.form.get("humor")
    texto_diar = request.form.get("texto_diar")
    usu_id = session['usuario_id']

    if humor and texto_diar:
        novo_diario = Diar(
            humor=humor,
            texto_diar=texto_diar,
            usu_id=usu_id
        )
        db.session.add(novo_diario)
        db.session.commit()

    return redirect(url_for("diar.index"))