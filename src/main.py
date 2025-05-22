from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config.settings import load_config
from infrastructure.db.session import db  # este contiene db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.update(load_config())

    jwt = JWTManager(app)

    db.init_app(app)
    Migrate(app, db)  # ❗ Correcto: usa db no Base

    from interfaces.api.auth_blueprint import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from interfaces.api.bikes_blueprint import bikes_bp
    app.register_blueprint(bikes_bp, url_prefix="/api")

    from interfaces.device.gps_service_stub import device_bp
    app.register_blueprint(device_bp, url_prefix="/api/device")

    from interfaces.api.users_blueprint import users_bp
    app.register_blueprint(users_bp, url_prefix="/api/users")
    


    from interfaces.api.register_blueprint import register_bp
    app.register_blueprint(register_bp, url_prefix="/api")



    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
