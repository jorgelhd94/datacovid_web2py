# --------------------------------------------------------------------------
# Ingresos Hospitalarios
# --------------------------------------------------------------------------
db.define_table("usuario_ubicacion",
                Field("idubicacion", "reference ubicacion"),
                Field("idusuario", "reference auth_user"),
                format='%(nombre)s'
                )

db.define_table("ingreso_hospitalario",
                Field("nombre"),
                Field("apellidos"),
                Field("edad","integer"),
                Field("ci", label='Carnet de identidad'),
                Field("sexo", label='Sexo', default='Masculino'),
                Field("morbilidades","text"),
                Field("vacunado","boolean"),
                Field("tipo_vacunacion", label=T('Tipo de Vacunación')),   # SET
                Field("vacuna"),   # SET           
                Field("estado", default='Estable'), # SET
                Field("fecha_ingreso","date"),
                Field("fecha_alta","date"),
                # Field("fecha_vacunacion","date"),
                Field("idubicacion", "reference ubicacion"),
                )

db.ingreso_hospitalario.nombre.requires=[IS_NOT_EMPTY(),IS_LENGTH(50)]
db.ingreso_hospitalario.apellidos.requires=[IS_NOT_EMPTY(),IS_LENGTH(50)]
db.ingreso_hospitalario.edad.requires=IS_INT_IN_RANGE(1,130)
db.ingreso_hospitalario.ci.requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'ingreso_hospitalario.ci'),IS_LENGTH(11)]
db.ingreso_hospitalario.sexo.requires=IS_IN_SET(["Masculino", "Femenino"])
db.ingreso_hospitalario.fecha_ingreso.requires=[IS_DATE(format=T('%d-%m-%Y'), error_message=T('Entre una fecha válida'))]
db.ingreso_hospitalario.morbilidades.requires=[IS_NOT_EMPTY()]
db.ingreso_hospitalario.vacuna.requires=IS_EMPTY_OR(IS_IN_SET(["Tipo 1", "Tipo 2", "Tipo 3", "Tipo 4", "Tipo 5"]))
db.ingreso_hospitalario.tipo_vacunacion.requires=IS_EMPTY_OR(IS_IN_SET(["Tipo 1", "Tipo 2", "Tipo 3", "Tipo 4", "Tipo 5"]))
db.ingreso_hospitalario.estado.requires=IS_IN_SET(["Estable", "Grave", "Crítico", "Fallecido", "Alta"])
