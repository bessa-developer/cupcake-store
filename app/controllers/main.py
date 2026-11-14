from flask import Blueprint, redirect, url_for

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    # A home leva direto ao catálogo de cupcakes.
    return redirect(url_for("produtos.catalogo"))
