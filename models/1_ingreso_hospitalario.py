# --------------------------------------------------------------------------
# Ingresos Hospitalarios
# --------------------------------------------------------------------------

db.define_table("ingreso_hospitalario",
                Field("nombre"),
                Field("apellidos"),
                Field("edad","integer"),
                Field("ci"),
                Field("nombre_hospital"),
                Field("morvilidades","text"),
                Field("vacunado","boolean"),
                Field("tipo_vacunacion"),   # SET
                Field("vacuna"),   # SET           
                Field("fecha_ingreso","date"),
                Field("fecha_alta","date"),
                Field("fecha_vacunacion","date"),
                Field("idubicacion", "reference ubicacion"),
                )

db.ingreso_hospitalario.nombre.requires=[IS_NOT_EMPTY(),IS_LENGTH(3)]
db.ingreso_hospitalario.apellidos.requires=[IS_NOT_EMPTY(),IS_LENGTH(50)]
db.ingreso_hospitalario.edad.requires=IS_INT_IN_RANGE(1,110)
db.ingreso_hospitalario.ci.requires=[IS_NOT_EMPTY(),IS_LENGTH(11)]
db.ingreso_hospitalario.nombre_hospital.requires=[IS_NOT_EMPTY(),IS_LENGTH(50)]
db.ingreso_hospitalario.vacuna.requires=IS_IN_SET(["Tipo 1", "Tipo 2", "Tipo 3", "Tipo 4", "Tipo 5"])
db.ingreso_hospitalario.tipo_vacunacion.requires=IS_IN_SET(["Tipo 1", "Tipo 2", "Tipo 3", "Tipo 4", "Tipo 5"])
