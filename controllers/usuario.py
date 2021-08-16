# Controlador para gestionar los usuarios y permisos
def iniciar_sesion():
    form = auth.login()

    if form.errors:
        form.errors.username = False
        form.errors.password = False

        session.error = True
        session.msg = "Existen errores en el formulario"

    return dict(form=form)


@auth.requires_login()
def logout():
    auth.logout()
    return dict()


@auth.requires_login()
def editar_perfil():
    registro = db.auth_user(auth.user.id) or redirect(URL('default', 'index'))

    if registro.username == "admin":
        session.status = True
        session.msg = "El usuario admin no puede editar su perfil"
        redirect(URL("default", "index"))

    form = SQLFORM.factory(Field("first_name", label=T("Nombre(s)"), default=registro.first_name, requires=IS_NOT_EMPTY()),
                           Field("last_name", label=T(
                               "Apellidos"), default=registro.last_name, requires=IS_NOT_EMPTY()),
                           Field("username", label=T("Nombre de usuario"),
                                 default=registro.username, requires=require_username),
                           Field("email", label=T("Correo electrónico"),
                                 default=registro.email, requires=require_email),
                           )

    # my_extra_element = DIV(LABEL(T('Repetir contraseña'), _class="form-control-label col-sm-3"), DIV(INPUT(_name='repeat', _class="form-control", _type='password'),_class="col-sm-9"), _class="form-group row")
    # form[0].insert(-1, my_extra_element)

    if form.validate():
        db(db.auth_user.id == registro.id).update(**form.vars)
        session.status = True
        session.msg = 'Usuario actualizado correctamente'
        redirect(URL("perfil"))
    elif form.errors:
        session.error = True
        session.msg = 'El formulario tiene errores'
    return dict(form=form)

# Administrador


@auth.requires_membership("Administrador")
def administrar():
    grid = db((db.auth_user.id != auth.user.id) & (db.auth_user.username != "admin")
              & (db.auth_membership.user_id == db.auth_user.id)).select(db.auth_user.ALL, db.auth_membership.ALL, db.usuario_provincia.ALL,
                                                                        left=db.usuario_provincia.on(db.auth_user.id == db.usuario_provincia.idusuario))
    return locals()


@auth.requires_login()
def perfil():
    # usuario = db.auth_user(request.args(0))or redirect(URL('administrar'))
    usuario = db.auth_user(auth.user.id) or redirect(URL('default', 'index'))

    rol = db(db.auth_membership.user_id ==
             usuario.id).select().first().group_id.role

    if db(db.usuario_provincia.idusuario == usuario.id).select().first():
        provincia = db(db.usuario_provincia.idusuario ==
                       usuario.id).select().first().idprovincia.nombre
    else:
        provincia = "No tiene"

    return locals()


@auth.requires_membership("Administrador")
def detalles():
    if not request.args(0):
        redirect(URL('default', 'index'))

    usuario = db.auth_user(request.args(0, cast=int)
                           ) or redirect(URL('administrar'))

    rol = db(db.auth_membership.user_id ==
             usuario.id).select().first().group_id.role

    if db(db.usuario_provincia.idusuario == usuario.id).select().first():
        provincia = db(db.usuario_provincia.idusuario ==
                       usuario.id).select().first().idprovincia.nombre
    else:
        provincia = "No tiene"

    return locals()


@auth.requires_membership("Administrador")
def crear():
    usuarios = db(db.auth_user.id > 0)
    require_username = [IS_NOT_EMPTY(), IS_NOT_IN_DB(
        usuarios, "auth_user.username"), IS_LENGTH(20)]
    require_email = [IS_NOT_EMPTY(), IS_EMAIL(
    ), IS_NOT_IN_DB(usuarios, "auth_user.email")]

    try:
        form = SQLFORM.factory(Field("first_name", label=T("Nombre(s)"), requires=IS_NOT_EMPTY()),
                               Field("last_name", label=T("Apellidos"),
                                     requires=IS_NOT_EMPTY()),
                               Field("username", label=T(
                                   "Nombre de usuario"), requires=require_username),
                               Field("email", label=T("Correo electrónico"),
                                     requires=require_email),
                               Field("password", "password", label=T(
                                   "Contraseña"), requires=[IS_NOT_EMPTY(), CRYPT()]),
                               Field("repeat", "password", label=T("Repetir contraseña"), requires=[
                                     IS_EQUAL_TO(request.vars.password)]),
                               Field("rol", "reference auth_group", label=T("Rol de usuario"), requires=IS_IN_DB(db, 'auth_group.id', '%(role)s',
                                                                                                                 zero=T('Seleccionar rol'))),
                               Field("provincia", "reference provincia", label=T("Asignar provincia"),
                                     requires=IS_EMPTY_OR(
                                         IS_IN_SET({i.id: i.nombre for i in db(db.provincia.id > 0).select()}))
                                     ),
                               Field("zona_ingreso", "reference ubicacion", label=T("Asignar Zona de Ingreso"),
                                     requires=IS_EMPTY_OR(
                                   IS_IN_SET({i.id: i.nombre for i in db(db.ubicacion.id > 0).select()}))
        ),
        )

        if form.validate():
            if form.vars.rol == 2:
                if not form.vars.provincia:
                    session.error = True
                    session.msg = 'El formulario tiene errores'
                    form.errors.provincia = "No puede ser vacío"
                else:
                    user_id = db.auth_user.insert(**form.vars)
                    db.auth_membership.insert(
                        user_id=user_id, group_id=form.vars.rol)
                    db.usuario_provincia.insert(
                        idusuario=user_id, idprovincia=form.vars.provincia)

                    raise TypeError
            elif form.vars.rol == 3:
                if not form.vars.zona_ingreso:
                    session.error = True
                    session.msg = 'El formulario tiene errores'
                    form.errors.zona_ingreso = "No puede ser vacío"
                else:
                    user_id = db.auth_user.insert(**form.vars)
                    db.auth_membership.insert(
                        user_id=user_id, group_id=form.vars.rol)
                    db.usuario_ubicacion.insert(
                        idusuario=user_id, idubicacion=form.vars.zona_ingreso)

                    raise TypeError
            else:
                user_id = db.auth_user.insert(**form.vars)
                db.auth_membership.insert(
                    user_id=user_id, group_id=form.vars.rol)

                raise TypeError

        elif form.errors:
            session.error = True
            session.msg = 'El formulario tiene errores'
    except TypeError:
        session.status = True
        session.msg = 'Usuario creado correctamente'
        redirect(URL("usuario", "detalles", args=user_id))
    except:
        redirect(URL("crear"))

    return dict(form=form)


@auth.requires_membership("Administrador")
def editar():
    if not request.args(0):
        redirect(URL('index'))

    registro = db.auth_user(request.args(0, cast=int)
                            ) or redirect(URL('index'))

    usuarios = db(db.auth_user.id != registro.id)
    require_username = [IS_NOT_EMPTY(), IS_NOT_IN_DB(
        usuarios, "auth_user.username"), IS_LENGTH(20)]
    require_email = [IS_NOT_EMPTY(), IS_EMAIL(
    ), IS_NOT_IN_DB(usuarios, "auth_user.email")]

    try:
        rol_id = db(db.auth_membership.user_id ==
                    registro.id).select().first().group_id.id

        if db(db.usuario_provincia.idusuario == registro.id).select().first():
            idprovincia = db(db.usuario_provincia.idusuario ==
                             registro.id).select().first().idprovincia.id
        else:
            idprovincia = 0

        form = SQLFORM.factory(Field("first_name", label=T("Nombre(s)"), default=registro.first_name, requires=IS_NOT_EMPTY()),
                               Field("last_name", label=T(
                                   "Apellidos"), default=registro.last_name, requires=IS_NOT_EMPTY()),
                               Field("username", label=T(
                                   "Nombre de usuario"), default=registro.username, requires=require_username),
                               Field("email", label=T("Correo electrónico"),
                                     default=registro.email, requires=require_email),
                               Field("rol", "reference auth_group", label=T("Rol de usuario"), default=rol_id, requires=IS_IN_DB(db, 'auth_group.id', '%(role)s',
                                                                                                                                 zero=T('Seleccionar rol'))),
                               Field("provincia", "reference provincia", label=T("Asignar provincia"), default=idprovincia,
                                     requires=IS_EMPTY_OR(
                                   IS_IN_SET({i.id: i.nombre for i in db(db.provincia.id > 0).select()}))
        )
        )

        if form.validate():
            if (form.vars.rol == 2):
                if not form.vars.provincia:
                    session.error = True
                    session.msg = 'El formulario tiene errores'
                    form.errors.provincia = "No puede ser vacío"
                else:
                    db(db.auth_user.id == registro.id).update(**form.vars)
                    db(db.auth_membership.user_id == registro.id).update(
                        group_id=form.vars.rol)

                    db(db.usuario_provincia.idusuario == registro.id).delete()
                    db.usuario_provincia.insert(
                        idusuario=registro.id, idprovincia=form.vars.provincia)

                    raise TypeError
            else:
                db(db.auth_user.id == registro.id).update(**form.vars)
                db(db.auth_membership.user_id == registro.id).update(
                    group_id=form.vars.rol)
                db(db.usuario_provincia.idusuario == registro.id).delete()

                raise TypeError

        elif form.errors:
            session.error = True
            session.msg = 'El formulario tiene errores'

    except TypeError:
        session.status = True
        session.msg = 'Usuario actualizado correctamente'
        redirect(URL("detalles", args=registro.id))
    except:
        redirect(URL("editar", args=registro.id))

    return dict(form=form, registro=registro)


@auth.requires_login()
def cambiar_clave():
    registro = db.auth_user(auth.user.id) or redirect(URL('default', 'index'))

    form = SQLFORM.factory(Field("password", "password", label=T("Nueva Contraseña"), requires=[IS_NOT_EMPTY(), CRYPT()]),
                           Field("repeat", "password", label=T("Repetir contraseña"), requires=[
                                 IS_EQUAL_TO(request.vars.password)]),
                           )

    if form.validate():
        db(db.auth_user.id == registro.id).update(**form.vars)
        session.status = True
        session.msg = 'Contraseña actualizada correctamente'
        redirect(URL("perfil", args=registro.id))
    elif form.errors:
        session.error = True
        session.msg = 'El formulario tiene errores'

    return dict(form=form, registro=registro)


@auth.requires_membership("Administrador")
def cambiar_clave_usuario():
    if not request.args(0):
        redirect(URL('default', 'index'))

    registro = db.auth_user(request.args(0, cast=int)
                            ) or redirect(URL('administrar'))

    form = SQLFORM.factory(Field("password", "password", label=T("Nueva Contraseña"), requires=[IS_NOT_EMPTY(), CRYPT()]),
                           Field("repeat", "password", label=T("Repetir contraseña"), requires=[
                                 IS_EQUAL_TO(request.vars.password)]),
                           )

    if form.validate():
        db(db.auth_user.id == registro.id).update(**form.vars)
        session.status = True
        session.msg = 'Contraseña actualizada correctamente'
        redirect(URL("detalles", args=registro.id))
    elif form.errors:
        session.error = True
        session.msg = 'El formulario tiene errores'

    return dict(form=form, registro=registro)


@auth.requires_membership("Administrador")
def eliminar():
    if not request.args(0):
        redirect(URL('administrar'))

    registro = db.auth_user(request.args(0, cast=int)
                            ) or redirect(URL('administrar'))
    x = registro.id

    if not registro.username == "admin":
        db(db.auth_user.id == x).delete()
        session.status = True
        session.msg = 'Usuario eliminado correctamente'

    redirect(URL("administrar"))

    return dict()


@auth.requires_login()
def no_autorizado():
    return locals()
