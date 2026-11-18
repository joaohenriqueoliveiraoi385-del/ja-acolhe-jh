import os
import random
from flask import Flask, render_template, session

from db import db
from model import Usu, Publi, Curt, Coment, Diar, Int, Not, Rec, Grupo, GrupoMembro, MensagemGrupo

from routes.usu import Usu_bp
from routes.publi import publi
from routes.diar import diar_bp
from routes.meditacao import meditacao_bp
from routes.grupo import grupo_bp
from routes.notificacoes import not_bp


app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_super_segura'


basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "JJ.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


app.register_blueprint(Usu_bp, url_prefix="/usuarios")
app.register_blueprint(publi, url_prefix="/publicacoes")
app.register_blueprint(diar_bp)
app.register_blueprint(meditacao_bp)
app.register_blueprint(grupo_bp)
app.register_blueprint(not_bp)


@app.context_processor
def injetar_notificacoes():
    usuario_id = session.get('usuario_id')
    if usuario_id:
        nao_lidas = Not.query.filter_by(usu_id=usuario_id, lida=False).count()
        return dict(notificacoes_nao_lidas=nao_lidas)
    return dict(notificacoes_nao_lidas=0)


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/feed")
def index():
    usuarios = Usu.query.all()
    publicacoes = Publi.query.order_by(Publi.data_publi.desc()).all()

    frases_motivacionais = [
        "Que o seu dia seja repleto de paz e pequenas alegrias! 💜",
        "Respire fundo. Você está fazendo o seu melhor e isso já é o bastante. ✨",
        "Cada novo dia é uma nova chance de cuidar de você mesma(o). 🌱",
        "Acredite na sua força e na beleza dos seus recomeços. 🌻",
        "Permita-se ir no seu próprio ritmo. O importante é não parar. ☕",
        "Você é mais forte do que imagina e mais querida(o) do que sabe. 💫",
        "Que tal tirar alguns minutos hoje para fazer algo que te faz sorrir? 😊"
    ]

    frase_do_dia = random.choice(frases_motivacionais)

    return render_template(
        "index.html",
        usuarios=usuarios,
        publicacoes=publicacoes,
        frase_do_dia=frase_do_dia
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)