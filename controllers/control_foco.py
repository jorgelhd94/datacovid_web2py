@auth.requires_login()
def administrar():

    if not auth.has_membership("Administrador"):
        provincia = db((db.usuario_provincia.idusuario ==
                        auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

        control_foco = db((db.municipio.id == db.control_foco.idmunicipio) & (db.municipio.idprovincia == db.provincia.id) & (
            db.provincia.id == provincia.id)).select()
    else:
        control_foco = db((db.control_foco.id > 0) & (db.municipio.id == db.control_foco.idmunicipio) & (
            db.provincia.id == db.municipio.idprovincia)).select()

    return locals()


@auth.requires_login()
def detalles():
    if not request.args(0):
        redirect(URL('administrar'))

    provincia = db((db.usuario_provincia.idusuario ==
                    auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

    control_foco = db.control_foco(
        request.args(0)) or redirect(URL('administrar'))

    if provincia and control_foco.idmunicipio.idprovincia != provincia.id:
        redirect(URL('administrar'))

    return locals()


@auth.requires_membership("Usuario estándar")
def crear():
    provincia = db((db.usuario_provincia.idusuario ==
                    auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

    db.control_foco.idmunicipio.requires = IS_IN_DB(
        db(db.municipio.idprovincia == provincia.id), "municipio.id", '%(nombre)s')

    db.control_foco.estado.writable = False
    form = SQLFORM(db.control_foco)

    if form.validate():
        control_foco_id = db.control_foco.insert(**form.vars)
        session.status = True
        session.msg = T('El control de foco se ha creado correctamente')
        redirect(URL("detalles", args=[control_foco_id]))
    elif form.errors:
        session.error = True
        session.msg = T('Existen errores en el formulario')
    return locals()


@auth.requires_membership("Usuario estándar")
def editar():
    if not request.args(0):
        redirect(URL('administrar'))

    provincia = db((db.usuario_provincia.idusuario ==
                    auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

    db.control_foco.estado.writable = False

    db.control_foco.idmunicipio.requires = IS_IN_DB(
        db(db.municipio.idprovincia == provincia.id), "municipio.id", '%(nombre)s')

    db.control_foco.fecha_ultimo_caso.writable = False

    control_foco = db.control_foco(
        request.args(0)) or redirect(URL('administrar'))

    if provincia and control_foco.idmunicipio.idprovincia != provincia.id:
        redirect(URL('administrar'))

    form = SQLFORM(db.control_foco, control_foco)

    if form.validate():
        db(db.control_foco.id == control_foco.id).update(**form.vars)
        session.status = True
        session.msg = T('El control de foco se ha actualizado correctamente')
        redirect(URL("detalles", args=[control_foco.id]))

    elif form.errors:
        session.error = True
        session.msg = T('Existen errores en el formulario')
    return locals()


@auth.requires_membership("Usuario estándar")
def eliminar():
    if not request.args(0):
        redirect(URL('administrar'))

    provincia = db((db.usuario_provincia.idusuario ==
                    auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

    registro = db.control_foco(request.args(0, cast=int)
                               ) or redirect(URL('administrar'))
    
    if provincia and registro.idmunicipio.idprovincia != provincia.id:
        redirect(URL('administrar'))

    x = registro.id
    db(db.control_foco.id == x).delete()
    session.status = True
    session.msg = 'Control de foco eliminado correctamente'
    redirect(URL("administrar"))

    return dict()


@auth.requires_membership("Usuario estándar")
def cambiar_estado():
    if not request.args(0):
        redirect(URL('administrar'))

    registro = db.control_foco(request.args(0, cast=int)
                               ) or redirect(URL('administrar'))
    x = registro.id

    if registro.estado == "Abierto":
        db(db.control_foco.id == x).update(estado="Cerrado")
        estado = "Cerrado"
    else:
        db(db.control_foco.id == x).update(estado="Abierto")
        estado = "Abierto"

    session.status = True
    session.msg = f'El control de foco ha cambiado su estado a {estado} correctamente'
    redirect(URL("detalles", args=x))

    return dict()

# API que devuelve los controles de foco


@request.restful()
def api():
    response.view = 'generic.json'

    def GET(*args, **vars):
        if not request.env.request_method == 'GET':
            raise HTTP(403)

        provincia = db((db.usuario_provincia.idusuario ==
                    auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

        control_foco = db((db.municipio.id == db.control_foco.idmunicipio) & (db.municipio.idprovincia == db.provincia.id) & (
            db.provincia.id == provincia.id)).select(db.control_foco.ALL).as_list()

        print(control_foco)

        return dict(controles_foco=control_foco)

    return locals()
