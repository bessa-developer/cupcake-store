from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    # Pagina inicial. Por enquanto so renderiza o esqueleto; o catalogo
    # sera ligado aqui na etapa das funcionalidades.
    return render_template("index.html")
