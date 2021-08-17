@auth.requires_membership("Ingresos Hospitalarios")
def administrar():
    datos = db(db.ingreso_hospitalario.id > 0).select()
    # return dict(ingreso_hospitalario=ingreso_hospitalario)
    return locals()


@auth.requires_membership("Ingresos Hospitalarios")
def crear():
    form = SQLFORM(db.ingreso_hospitalario)

    if form.validate():
        form.vars.idubicacion = db(db.usuario_ubicacion.idusuario == auth.user.id).select().first().idubicacion
        if not form.vars.vacunado:
            form.vars.tipo_vacunacion = ""
            form.vars.vacuna = ""
        ingreso_id = db.ingreso_hospitalario.insert(**form.vars)
        session.status = True
        session.msg = T('El Ingreso Hospitalario se ha creado correctamente')
        # redirect(URL("detalles", args=[ingreso_id]))
    elif form.errors:
        session.error = True
        session.msg = T('Existen errores en el formulario')
    return locals()
