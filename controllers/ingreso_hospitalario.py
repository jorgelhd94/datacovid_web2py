requirements = auth.has_membership(
    "Administrador") or auth.has_membership("Ingresos Hospitalarios")

only_ingresos = auth.has_membership("Ingresos Hospitalarios")

@auth.requires(requirements)
def administrar():
    datos = db(db.ingreso_hospitalario.id > 0).select()
    return locals()


@auth.requires(requirements)
def detalles():
    if not request.args(0):
        redirect(URL('administrar'))
    ingreso = db.ingreso_hospitalario(
        request.args(0)) or redirect(URL('administrar'))
    return locals()


@auth.requires(requirements)
def cambiar_estado():
    if not request.args(0):
        redirect(URL('administrar'))
    ingreso = db.ingreso_hospitalario(
        request.args(0)) or redirect(URL('administrar'))

    form = SQLFORM.factory(
        Field("fecha_alta", "date", requires=[
              IS_EMPTY_OR([IS_DATE(format=T('%d/%m/%Y'), error_message=T('Entre una fecha válida')),
                          IS_DATE_IN_RANGE(format=T('%d/%m/%Y'),
                                           minimum=ingreso.fecha_ingreso)])
              ]),
        Field("estado", default=ingreso.estado, requires=IS_IN_SET(
            ["Estable", "Grave", "Crítico", "Fallecido", "Alta"])),
    )

    if form.process(keepvalues=True).accepted:
        if form.vars.estado != 'Alta' and form.vars.estado != 'Fallecido':
            fecha_alta = None
        else:
            fecha_alta = form.vars.fecha_alta

            if not fecha_alta:
                form.errors.fecha_alta = 'No puede ser vacío'
                session.error = True
                session.msg = T('Existen errores en el formulario')

        if not form.errors.fecha_alta:
            db(db.ingreso_hospitalario.id == ingreso.id).update(
                fecha_alta=fecha_alta, estado=form.vars.estado)

            session.status = True
            session.msg = T('El Estado se ha cambiado correctamente')

            redirect(URL("detalles", args=[ingreso.id]))

    elif form.errors:
        session.error = True
        session.msg = T('Existen errores en el formulario')

    return locals()


@auth.requires(only_ingresos)
def crear():
    db.ingreso_hospitalario.estado.writable = False
    form = SQLFORM(db.ingreso_hospitalario)

    if form.validate():
        form.vars.idubicacion = db(
            db.usuario_ubicacion.idusuario == auth.user.id).select().first().idubicacion

        # Fecha del Ingreso
        fecha_ingreso = str(form.vars.fecha_ingreso).split("/")
        form.vars.fecha_ingreso = "-".join(
            [i for i in reversed(fecha_ingreso)])

        if not form.vars.vacunado:
            form.vars.tipo_vacunacion = ""
            form.vars.vacuna = ""

        ingreso_id = db.ingreso_hospitalario.insert(**form.vars)
        session.status = True
        session.msg = T('El Ingreso Hospitalario se ha creado correctamente')
        redirect(URL("detalles", args=[ingreso_id]))
    elif form.errors:
        session.error = True
        session.msg = T('Existen errores en el formulario')
    return locals()


@auth.requires(only_ingresos)
def editar():
    if not request.args(0):
        redirect(URL('administrar'))
    db.ingreso_hospitalario.estado.writable = False

    ingreso = db.ingreso_hospitalario(
        request.args(0)) or redirect(URL('administrar'))

    form = SQLFORM(db.ingreso_hospitalario, ingreso)

    if form.validate():
        form.vars.idubicacion = db(
            db.usuario_ubicacion.idusuario == auth.user.id).select().first().idubicacion

        # Fecha del reporte
        fecha_ingreso = str(form.vars.fecha_ingreso).split("/")
        form.vars.fecha_ingreso = "-".join(
            [i for i in reversed(fecha_ingreso)])

        if not form.vars.vacunado:
            form.vars.tipo_vacunacion = ""
            form.vars.vacuna = ""

        db(db.ingreso_hospitalario.id == ingreso.id).update(**form.vars)

        session.status = True
        session.msg = T('El Ingreso Hospitalario se ha editado correctamente')
        redirect(URL("detalles", args=[ingreso.id]))
    elif form.errors:
        session.error = True
        session.msg = T('Existen errores en el formulario')
    return locals()


@auth.requires(requirements)
def eliminar():
    if not request.args(0):
        redirect(URL('administrar'))

    registro = db.ingreso_hospitalario(request.args(0, cast=int)
                                       ) or redirect(URL('administrar'))
    x = registro.id
    db(db.ingreso_hospitalario.id == x).delete()
    session.status = True
    session.msg = 'Ingreso eliminado correctamente'
    redirect(URL("administrar"))

    return dict()
