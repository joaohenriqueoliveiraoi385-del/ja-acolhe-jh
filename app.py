from flask import Flask, render_template

from db import db
from model import Usu, Publi, Curt, Coment, Diar, Int, Not, Rec

from routes.usu import Usu_bp
from routes.publi import publi


app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_super_segura'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///JJ.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(Usu_bp, url_prefix="/usuarios")
app.register_blueprint(publi, url_prefix="/publicacoes")


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/feed")
def index():
    usuarios = Usu.query.all()
    publicacoes = Publi.query.order_by(Publi.data_publi.desc()).all()

    return render_template(
        "index.html",
        usuarios=usuarios,
        publicacoes=publicacoes
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5001)