from flask import Flask
from api.routes import register_routes
from infrastructure.logging import setup_logging
from infrastructure.databases.base import Base
from infrastructure.databases.session import engine

def create_app():
    app = Flask(__name__)

    setup_logging(app)
    Base.metadata.create_all(bind=engine)
    register_routes(app)

    return app
