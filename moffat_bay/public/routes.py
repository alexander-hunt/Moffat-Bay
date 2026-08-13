"""Routes available to all visitors."""

from flask import render_template

from . import public_bp


@public_bp.get("/")
def index():
    return render_template("public/index.html")

