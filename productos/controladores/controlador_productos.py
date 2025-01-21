from productos.modelos.modelo_productos import *

mod_formulario = Formulario()

class Formulario_Controlador():
    
    def get_traer_datos(self):
        query = mod_formulario.recibir_datos()
        return query