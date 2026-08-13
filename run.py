"""Development entry point for the Moffat Bay Lodge application."""

from moffat_bay import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])

