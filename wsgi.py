"""Used to start the application with gunicorn."""
from api import create_app

app = create_app()
