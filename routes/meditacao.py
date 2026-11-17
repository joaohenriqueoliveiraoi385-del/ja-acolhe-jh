from flask import Blueprint, render_template

meditacao_bp = Blueprint('meditacao', __name__)

@meditacao_bp.route("/meditacao")
def meditacao():
   
    return render_template("meditacao.html")