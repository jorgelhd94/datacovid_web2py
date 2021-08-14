# Provincias

# API que devuelve las provincias y sus muncipios
@request.restful()
def api():
    response.view = 'generic.json'

    def GET(*args, **vars):
        if not request.env.request_method == 'GET': raise HTTP(403)
        
        datos = dict()
        provincias = db(db.provincia.id > 0).select()

        for p in provincias:
            municipios = db(db.municipio.idprovincia == p.id).select()
            datos[p.nombre] = municipios

        
        municipios = db(db.municipio.id > 0).select().as_list()
    

        return dict(provincias = datos, municipios = municipios)
    
    return locals()

