from librerias import *
from productos.controladores.controlador_productos import *

con_formulario = Formulario_Controlador()

#TODO: Validación | Mejorar mensajes de respuestas
#TODO: Validación | Rutas protegidas por Token

productos = Blueprint('productos', __name__)

@productos.route('/recibir-datos/', methods=['POST'])
@cross_origin()
def post_crear_imagen_producto():
   try:
        return con_formulario.get_traer_datos()
   except Exception as e:
        return jsonify({"error": str(e)}), 500     