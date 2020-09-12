from flask import Flask
from .config import app_config
from .views.IntegrationView import extractor_api as extractor_blueprint


def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    app.register_blueprint(extractor_blueprint, url_prefix='/api/v1/nlp')

    @app.route("/", methods=["GET"])
    def index():
        return "Congratulations! Your first endpoint is working"

    return app

