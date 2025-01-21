class utils:

    def extraer_id_imagen(imagen_url):
        parts = imagen_url.split('/')
        imagen_id = parts[-1].split('.')[0]
        return imagen_id