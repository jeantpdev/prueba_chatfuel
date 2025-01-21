from librerias import *
from utils import *

class Formulario():  

    def recibir_datos(self):

        try:
            datos = request.get_json()
            print(datos)
            nombre = datos["nombre"]
            print(nombre)
            return jsonify({"mensaje": "Datos recibidos correctamente", "nombre": nombre}), 200

            # return jsonify({"urls_imagenes_secundarias": urls_imagenes_secundarias, "url_imagen_principal": url_imagen_principal}), 200
        
        except Exception as e:
            return jsonify({"mensaje": str(e)}), 500
       