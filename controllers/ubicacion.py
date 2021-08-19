requirements = auth.has_membership(
    "Administrador") or auth.has_membership("Puesto de mando")

@auth.requires(requirements)
def administrar():
    ubicacion = db(db.ubicacion.id > 0).select()
    return locals()


@auth.requires(requirements)
def detalles():
    if not request.args(0):
        redirect(URL('administrar'))
    ubicacion = db.ubicacion(request.args(0)) or redirect(URL('administrar'))
    return locals()


@auth.requires(requirements)
def crear():
    db.ubicacion.idmunicipio.requires = IS_IN_DB(
        db(db.municipio.id > 0), "municipio.id", '%(nombre)s')

    form = SQLFORM(db.ubicacion)

    if form.validate():
        ubicacion_id = db.ubicacion.insert(**form.vars)
        session.status = True
        session.msg = T('La ubicación de casos activos se ha creado correctamente')
        redirect(URL("detalles", args=[ubicacion_id]))
    elif form.errors:
        session.error = True
        session.msg = T('Existen errores en el formulario')
    return locals()


@auth.requires(requirements)
def editar():
    if not request.args(0):
        redirect(URL('administrar'))
    

    db.ubicacion.idmunicipio.requires = IS_IN_DB(
        db(db.municipio.id > 0), "municipio.id", '%(nombre)s')

    ubicacion = db.ubicacion(request.args(0)) or redirect(URL('administrar'))

    form = SQLFORM(db.ubicacion, ubicacion)

    if form.validate():
        db(db.ubicacion.id == ubicacion.id).update(**form.vars)
        session.status = True
        session.msg = T('La ubicación de casos activos se ha actualizado correctamente')
        redirect(URL("detalles", args=[ubicacion.id]))

    elif form.errors:
        session.error = True
        session.msg = T('Existen errores en el formulario')
    return locals()


@auth.requires(requirements)
def eliminar():
    if not request.args(0):
        redirect(URL('administrar'))

    registro = db.ubicacion(request.args(0, cast=int)
                          ) or redirect(URL('administrar'))
    x = registro.id
    db(db.ubicacion.id == x).delete()
    session.status = True
    session.msg = 'Ubicación de casos activos eliminada correctamente'
    redirect(URL("administrar"))

    return dict()


# API que devuelve las municipios y sus ubicaciones
@request.restful()
def api():
    response.view = 'generic.json'

    def GET(*args, **vars):
        if not request.env.request_method == 'GET': raise HTTP(403)
        
        datos = dict()
        municipios = db(db.municipio.id > 0).select()

        for m in municipios:
            ubicaciones = db(db.ubicacion.idmunicipio == m.id).select().as_list()
            if ubicaciones:
                datos[m.nombre] = ubicaciones
        
        ubicaciones = db(db.ubicacion.id > 0).select().as_list()        

        return dict(municipios = datos, ubicaciones = ubicaciones)
    
    return locals()