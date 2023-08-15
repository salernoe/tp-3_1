from flask import Blueprint, jsonify, current_app

#main_routes = Blueprint("main", __name__)
app = Blueprint("main", __name__)

@app.route("/")
def index():
    return jsonify( "Bienvenidos!"), 200

@app.route('/info')
def info():
    return jsonify( f"Bienvenidx a {current_app.config['APP_NAME']}"),200

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
    
