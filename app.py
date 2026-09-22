from flask import Flask, render_template

from db import db
from model import Usu, Publi, Curt, Coment, Diar, Int, Not, Rec

from routes.usu import Usu_bp
from routes.publi import Publi_bp


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///JJ.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(Usu_bp, url_prefix="/usuarios")
app.register_blueprint(Publi_bp, url_prefix="/publicacoes")


@app.route("/")
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

    app.run(debug=True)