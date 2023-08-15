from flask import render_template, request,Flask,jsonify, current_app, Blueprint
from config import Config
from datetime import datetime

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
    
       
    
   
    
    @app.route('/about')
    def about():
        app_info = {
            "app_name": current_app.config['APP_NAME'],
            "description": current_app.config['DESCRIPTION'],
            "developers": current_app.config['DEVELOPERS'],
            "version": current_app.config['VERSION']
        }
        return jsonify(app_info)
    

    @app.route("/sum/<int:num1>/<int:num2>")
    def sum_numbers(num1, num2):
      result = num1 + num2
      return jsonify({"result": result})

    @app.route("/age/<dob>")
    def calculate_age(dob):
        try:
            birth_date = datetime.strptime(dob, "%Y-%m-%d")
            current_date = datetime.now()
            
            if birth_date > current_date:
                return jsonify({"error": "La fecha de nacimiento no puede ser posterior a la fecha actual"}), 400
            
            age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
            return jsonify({"age": age}), 200
        
        except ValueError:
            return jsonify({"error": "Formato de fecha incorrecto. Utilice el formato ISO 8601 (YYYY-MM-DD)"}), 400
    
    return app