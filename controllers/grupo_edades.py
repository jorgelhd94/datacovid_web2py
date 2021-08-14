# API para los grupo de edades
@request.restful()
def api():
    response.view = 'generic.json'

    def GET(*args, **vars):
        if not request.env.request_method == 'GET': raise HTTP(403)
        
        grupo_edades = db(db.grupo_edades.id > 0).select().as_list()       

        return dict(grupo_edades = grupo_edades)
    
    return locals()

