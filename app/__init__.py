from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    # Importar rutas (si tienes rutas en un archivo separado)
    from app.routes import bp
    app.register_blueprint(bp)

    Migrate(app, db)
    
    with app.app_context():
        db.create_all()
    return app
