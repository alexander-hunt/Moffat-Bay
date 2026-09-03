"""Routes available to all visitors."""

from flask import render_template

from . import public_bp


@public_bp.get("/")
def index():
    return render_template("public/index.html")


@public_bp.get("/about")
def about():
    """Render lodge background and hospitality information."""
    return render_template("public/about.html")


@public_bp.get("/contact")
def contact():
    """Render lodge contact information."""
    return render_template("public/contact.html")


@public_bp.get("/attractions")
def attractions():
    """Render Joviedsa Island activity information."""
    return render_template("public/attractions.html")
