from flask import render_template, request,Flask,jsonify, current_app
from config import Config

def init_app():
    
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    
    app.config.from_object(Config)
    # Un endpoint que dice 'Hola Mundo!'
    
    @app.route('/')
    def hello_world():
        return 'bienvenidos!'
    
    
    
    @app.route('/info')
    def info():
        
        return ({"message": f"Bienvenidx a {current_app.config['APP_NAME']}"}),200
    
       
    
   
    
    @app.route("/about")
    def about():
        app_info = {
            "app_name": current_app.config['APP_NAME'],
            "description": current_app.config['DESCRIPTION'],
            "developers": current_app.config['DEVELOPERS'],
            "version": current_app.config['VERSION']
        }
        return jsonify(app_info)
    
    return app