@auth.requires_login()
def administrar():
    origen = db(db.origen.id > 0).select()
    return locals()


@auth.requires_login()
def detalles():
    if not request.args(0):
        redirect(URL('administrar'))
    origen = db.origen(request.args(0)) or redirect(URL('administrar'))
    return locals()


@auth.requires_login()
def crear():
    db.origen.idmunicipio.requires = IS_IN_DB(
        db(db.municipio.id > 0), "municipio.id", '%(nombre)s')

    form = SQLFORM(db.origen)

    if form.validate():
        origen_id = db.origen.insert(**form.vars)
        session.status = True
        session.msg = T('El orígen de muestra se ha creado correctamente')
        redirect(URL("detalles", args=[origen_id]))
    elif form.errors:
        session.error = True
        session.msg = T('Existen errores en el formulario')
    return locals()


@auth.requires_login()
def editar():
    if not request.args(0):
        redirect(URL('administrar'))

    db.origen.idmunicipio.requires = IS_IN_DB(
        db(db.municipio.id > 0), "municipio.id", '%(nombre)s')

    origen = db.origen(request.args(0)) or redirect(URL('administrar'))

    form = SQLFORM(db.origen, origen)

    if form.validate():
        db(db.origen.id == origen.id).update(**form.vars)
        session.status = True
        session.msg = T('El orígen de muestra se ha actualizado correctamente')
        redirect(URL("detalles", args=[origen.id]))

    elif form.errors:
        session.error = True
        session.msg = T('Existen errores en el formulario')
    return locals()


@auth.requires_login()
def eliminar():
    if not request.args(0):
        redirect(URL('administrar'))

    registro = db.origen(request.args(0, cast=int)
                         ) or redirect(URL('administrar'))
    x = registro.id
    db(db.origen.id == x).delete()
    session.status = True
    session.msg = 'Orígen de muestra eliminado correctamente'
    redirect(URL("administrar"))

    return dict()


# API para los origenes de las muestras
@request.restful()
def api():
    response.view = 'generic.json'

    def GET(*args, **vars):
        if not request.env.request_method == 'GET':
            raise HTTP(403)

        origenes = db(db.origen.id > 0).select().as_list()

        return dict(origenes=origenes)

    return locals()
