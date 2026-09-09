"""Routes available to all visitors."""

from flask import render_template

from . import public_bp


@public_bp.get("/")
def index():
    return render_template("public/index.html")


@public_bp.get("/about")
def about():
    """Render lodge information and contact details."""
    return render_template("public/about.html")
