@auth.requires_login()
def administrar():
    if not auth.has_membership("Administrador"):
        provincia = db((db.usuario_provincia.idusuario ==
                        auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

        eventos = db((db.municipio.id == db.eventos.idmunicipio) & (db.municipio.idprovincia == db.provincia.id) & (
            db.provincia.id == provincia.id)).select()
    else:
        eventos = db((db.eventos.id > 0) & (db.municipio.id == db.eventos.idmunicipio) & (
            db.provincia.id == db.municipio.idprovincia)).select()

    return locals()


@auth.requires_login()
def detalles():
    if not request.args(0):
        redirect(URL('administrar'))

    provincia = db((db.usuario_provincia.idusuario ==
                    auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

    evento = db.eventos(request.args(0)) or redirect(URL('administrar'))

    if provincia and evento.idmunicipio.idprovincia != provincia.id:
        redirect(URL('administrar'))

    return locals()


@auth.requires_membership("Puesto de mando")
def crear():
    provincia = db((db.usuario_provincia.idusuario ==
                    auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()
    db.eventos.idmunicipio.requires = IS_IN_DB(
        db((db.municipio.idprovincia == provincia.id)), "municipio.id", '%(nombre)s')
    db.eventos.estado.writable = False
    form = SQLFORM(db.eventos)

    if form.validate():
        evento_id = db.eventos.insert(**form.vars)
        session.status = True
        session.msg = T('El evento se ha creado correctamente')
        redirect(URL("detalles", args=[evento_id]))
    elif form.errors:
        session.error = True
        session.msg = T('Existen errores en el formulario')
    return locals()


@auth.requires_membership("Puesto de mando")
def editar():
    if not request.args(0):
        redirect(URL('administrar'))

    provincia = db((db.usuario_provincia.idusuario ==
                    auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

    db.eventos.idmunicipio.requires = IS_IN_DB(
        db(db.municipio.idprovincia == provincia.id), "municipio.id", '%(nombre)s')
    db.eventos.fecha_ultimo_caso.writable = False
    db.eventos.estado.writable = False

    evento = db.eventos(request.args(0)) or redirect(URL('administrar'))

    if provincia and evento.idmunicipio.idprovincia != provincia.id:
        redirect(URL('administrar'))

    form = SQLFORM(db.eventos, evento)

    if form.validate():
        db(db.eventos.id == evento.id).update(**form.vars)
        session.status = True
        session.msg = T('El evento se ha actualizado correctamente')
        redirect(URL("detalles", args=[evento.id]))

    elif form.errors:
        session.error = True
        session.msg = T('Existen errores en el formulario')
    return locals()


@auth.requires_membership("Puesto de mando")
def eliminar():
    if not request.args(0):
        redirect(URL('administrar'))

    provincia = db((db.usuario_provincia.idusuario ==
                    auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

    registro = db.eventos(request.args(0, cast=int)
                          ) or redirect(URL('administrar'))

    if provincia and registro.idmunicipio.idprovincia != provincia.id:
        redirect(URL('administrar'))

    x = registro.id
    db(db.eventos.id == x).delete()
    session.status = True
    session.msg = 'Evento eliminado correctamente'
    redirect(URL("administrar"))

    return dict()


@auth.requires_membership("Puesto de mando")
def cambiar_estado():
    if not request.args(0):
        redirect(URL('administrar'))

    registro = db.eventos(request.args(0, cast=int)
                          ) or redirect(URL('administrar'))
    x = registro.id

    if registro.estado == "Abierto":
        db(db.eventos.id == x).update(estado="Cerrado")
        estado = "Cerrado"
    else:
        db(db.eventos.id == x).update(estado="Abierto")
        estado = "Abierto"

    session.status = True
    session.msg = f'El evento ha cambiado su estado a {estado} correctamente'
    redirect(URL("detalles", args=x))

    return dict()


# API que devuelve los eventos
@request.restful()
def api():
    response.view = 'generic.json'

    def GET(*args, **vars):
        if not request.env.request_method == 'GET':
            raise HTTP(403)

        provincia = db((db.usuario_provincia.idusuario ==
                    auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

        eventos = db((db.municipio.id == db.eventos.idmunicipio) & (db.municipio.idprovincia == db.provincia.id) & (
            db.provincia.id == provincia.id)).select(db.eventos.ALL).as_list()

        return dict(eventos=eventos)

    return locals()
