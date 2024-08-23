
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .blueprints.wizard import bp as wizard_blueprint
    app.register_blueprint(wizard_blueprint, url_prefix='/wizard')
    
    return app