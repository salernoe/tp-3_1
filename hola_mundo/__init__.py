from flask import render_template, request,Flask,jsonify, current_app, Blueprint
from config import Config
from datetime import datetime
import re
import json
import os

def init_app():
    
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    
    app.config.from_object(Config)
    # Un endpoint que dice 'Hola Mundo!'
    
    
    
    @app.route('/')
    # ejercicio 1 Crear una aplicación Flask que muestre una página web con un mensaje de bienvenida.
    def hello_world():
        return 'bienvenidos!'
    
    
    
    @app.route('/info')
    # ejercico 2 crea una aplicación Flask que muestre una página web con la información de la aplicación.
    
    def info():
        
        return ({"message": f"Bienvenidx a {current_app.config['APP_NAME']}"}),200
    
       
    
   
    
    @app.route('/about')
    # ejercicio 3 Definir un endpoint para la ruta /about que muestre información sobre la aplicación en formato JSON

    def about():
        app_info = {
            "app_name": current_app.config['APP_NAME'],
            "description": current_app.config['DESCRIPTION'],
            "developers": current_app.config['DEVELOPERS'],
            "version": current_app.config['VERSION']
        }
        return jsonify(app_info)
    

    @app.route("/sum/<int:num1>/<int:num2>")
    
    #ejercion 4 Definir un endpoint para la ruta /sum/<int:num1>/<int:num2> que sume dos números 
    #enteros y muestre el resultado. Por ejemplo, para la petición /sum/20/10 devolveríamos  30.
    
    def sum_numbers(num1, num2):
      result = num1 + num2
      return jsonify({"result": result})

    
    
    @app.route("/age/<dob>")
    
    # ejercio 5 definir un endpoint que calcule la edad de una persona en base a su fecha de 
    #nacimiento. Para ello se establece la ruta /age/<dob>, donde dob se refiere a day of birth
    #y se encuentra en formato ISO 8601 (YYYY-MM-DD).
    # ejemplo /age/2001-10-20
    
    
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
    
    
    
    @app.route("/operate/<string:operation>/<int:num1>/<int:num2>")
    
    #ejercicio 6 definir un endpoint que realice operaciones básicas (suma, resta, multiplicación y división)
    # ejemplos operate/sum/10/20 , /operate/sub/30/15 , /operate/mult/5/8 , /operate/div/100/4 , /operate/div/10/0
        
    def perform_operation(operation, num1, num2):
        if operation == "sum":
            result = num1 + num2
        elif operation == "sub":
            result = num1 - num2
        elif operation == "mult":
            result = num1 * num2
        elif operation == "div":
            if num2 == 0:
                return jsonify({"error": "La división por cero no está definida"}), 400
            result = num1 / num2
        else:
            return jsonify({"error": "Operación no válida. Las operaciones válidas son: sum, sub, mult, div"}), 400
        
        return jsonify({"result": result})
    
    @app.route("/operate2")
    #  ejercico 7 Reformular el ejercicio anterior para el endpoint /operate, con la diferencia que esta ruta 
    #deberá recibir parámetros de consulta (query params) operation, num1 y num2 en lugar 
    #de parámetros de ruta como veíamos en el ejercicio 8.
    def perform_operation2():
        operation = request.args.get("operation")
        num1 = int(request.args.get("num1"))
        num2 = int(request.args.get("num2"))
        
        if operation == "sum":
            result = num1 + num2
        elif operation == "sub":
            result = num1 - num2
        elif operation == "mult":
            result = num1 * num2
        elif operation == "div":
            if num2 == 0:
                return jsonify({"error": "La división por cero no está definida"}), 400
            result = num1 / num2
        else:
            return jsonify({"error": "Operación no válida. Las operaciones válidas son: sum, sub, mult, div"}), 400
        
        return jsonify({"result": result})
   
    @app.route("/title/<string:word>")
    # ejercicio 8 Definir un endpoint que convierta una palabra en formato título.crear una ruta para en el endpoint /title/<string:word>, el cual aplica el 
    #formato título al parámetro de ruta word
    # ejemplo /title/SARmienTo
    
    def format_title(word):
        formatted_word = word.title()
        return jsonify({"formatted_word": formatted_word})
   
   
    
    #  ejecicio 9 convierte dni a numero entero 
    # ejemplo /formatted/23.456.007
    
    
    
    def validate_dni_format(dni):
    # Elimina puntos y guiones del DNI
        dni = dni.replace(".", "").replace("-", "")
    
    # Verifica si el DNI contiene solo dígitos y tiene una longitud válida
        if not dni.isdigit() or len(dni) != 8:
            return False
        return True

    def convert_dni_to_integer(dni):
        dni = dni.replace(".", "").replace("-", "")  # Elimina puntos y guiones del DNI
        
        if not validate_dni_format(dni):
            return None
        
        return int(dni)
   
   
   
    @app.route("/formatted/<string:dni>")
    def formatted_dni(dni):
        integer_dni = convert_dni_to_integer(dni)
        
        if integer_dni is None:
            return jsonify({"error": "Formato de DNI no válido"}), 400
        
        return jsonify({"formatted_dni": integer_dni})   
   
   
    
    
    @app.route("/format")
    #  ejercicio 10 convierte los parámetros de consulta (query params) firstname, lastname y dob etc
    # ejemplo /format?firstname=LUiS&lastname=JUARez&dob=2001-08-27&dni=44.010.777
    
    def format_user_data():
        firstname = request.args.get("firstname").capitalize()
        lastname = request.args.get("lastname").capitalize()
        dob = request.args.get("dob")
        dni = request.args.get("dni")
        
        if not validate_dni_format(dni):
            return jsonify({"error": "Formato de DNI no válido"}), 400
        
        integer_dni = convert_dni_to_integer(dni)
        
        if integer_dni is None:
            return jsonify({"error": "Formato de DNI no válido"}), 400
        
        # Cálculo de la edad en base a la fecha de nacimiento
        dob_date = datetime.strptime(dob, "%Y-%m-%d")
        current_date = datetime.now()
        age = current_date.year - dob_date.year - ((current_date.month, current_date.day) < (dob_date.month, dob_date.day))
        
        response_data = {
            "firstname": firstname,
            "lastname": lastname,
            "age": age,
            "dni": integer_dni
        }
        
        return jsonify(response_data)
    
   
    
    with open('hola_mundo/morse_code.json') as f:
        morse_data = json.load(f)

    morse_letters = morse_data['letters']
    
    def encode_to_morse(keyword):
        encoded = []
        for char in keyword:
            if char == '+':
                encoded.append('^')  
            elif char in morse_letters:
                encoded.append(morse_letters[char])
        return '+'.join(encoded)
    
    @app.route('/encode/<string:keyword>')
    def encode_keyword(keyword):
        encoded = encode_to_morse(keyword)
        return jsonify({'morse_code': encoded})




    
    
    
    
    
    
    
    
    return app