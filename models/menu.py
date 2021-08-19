# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------
# Idioma
T.force('es-es')

iconos = {"Inicio": "dw-house", "Reportes": "dw-notepad-2",
          'Generar informe': 'dw-presentation-2', "Eventos": "dw-map", "Controles de foco": "dw-map",
          'Ingresos': 'dw-file-4',
          'Orígen de muestras': 'dw-ambulance', 'Ubicación casos activos': 'dw-hospital', 'Usuarios': 'dw-user'}


response.menu = [
    (T('Home'), request.controller == "default" and request.function ==
     "index", URL('default', 'index'), [])
]

menu_generico = [
    ("Divisor",),
    (T('Orígen de muestras'), request.controller == "origen" and (request.function == "crear" or
                                                                  request.function == "administrar"), None, [
        (T('Crear orígen de muestra'), request.controller ==
         "origen" and request.function == "crear", URL('origen', 'crear')),
        (T('Administrar'), request.controller == "origen" and request.function ==
         "administrar", URL('origen', 'administrar')),
    ]),
    (T('Ubicación casos activos'), request.controller == "ubicacion" and (request.function == "crear" or
                                                                          request.function == "administrar"), None, [
        (T('Crear ubicación'), request.controller ==
         "ubicacion" and request.function == "crear", URL('ubicacion', 'crear')),
        (T('Administrar'), request.controller == "ubicacion" and request.function ==
         "administrar", URL('ubicacion', 'administrar')),
    ]),
]

menu_ingresos = [
    ("Divisor",),
    (T('Ingresos'), request.controller == "ingreso_hospitalario" and (request.function == "crear" or
                                                                      request.function == "administrar"), None, [
        (T('Nuevo ingreso'), request.controller ==
         "ingreso_hospitalario" and request.function == "crear", URL('ingreso_hospitalario', 'crear')),
        (T('Administrar'), request.controller == "ingreso_hospitalario" and request.function ==
         "administrar", URL('ingreso_hospitalario', 'administrar')),
    ]),
]


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if auth.has_membership("Administrador"):
    # Usuarios
    response.menu += [
        ("Divisor",),
        (T('Reportes'), request.controller == "reporte" and (request.function == "crear" or
                                                             request.function == "administrar"), None, [
            (T('Listado'), request.controller == "reporte" and request.function ==
             "administrar", URL('reporte', 'administrar')),
        ]),
        (T('Generar informe'), request.controller == "informe" and request.function ==
         "seleccionar_reporte", URL('informe', 'seleccionar_reporte'), []),
        ("Divisor",),
        (T('Ingresos'), request.controller == "ingreso_hospitalario" and (request.function == "crear" or
                                                                          request.function == "administrar"), None, [
         (T('Administrar'), request.controller == "ingreso_hospitalario" and request.function ==
             "administrar", URL('ingreso_hospitalario', 'administrar')),
         ]),
        ("Divisor",),
        (T('Eventos'), request.controller == "evento" and (request.function == "crear" or
                                                           request.function == "administrar"), None, [
            (T('Listado'), request.controller == "evento" and request.function ==
             "administrar", URL('evento', 'administrar')),
        ]),
        (T('Controles de foco'), request.controller == "control_foco" and (request.function == "crear" or
                                                                           request.function == "administrar"), None, [
            (T('Listado'), request.controller == "control_foco" and request.function ==
             "administrar", URL('control_foco', 'administrar')),
        ]),
    ]

    response.menu += menu_generico

    response.menu += [
        ("Divisor",),
        (T('Usuarios'), request.controller == "usuario" and (request.function == "crear" or
                                                             request.function == "administrar"), None, [
            (T('Crear usuario'), request.controller ==
                "usuario" and request.function == "crear", URL('usuario', 'crear')),
            (T('Administrar'), request.controller == "usuario" and request.function ==
                "administrar", URL('usuario', 'administrar')),
        ]),
    ]
elif auth.has_membership("Ingresos Hospitalarios"):
    response.menu += menu_ingresos
else:
    response.menu += [
        ("Divisor",),
        (T('Reportes'), request.controller == "reporte" and (request.function == "crear" or
                                                             request.function == "administrar"), None, [
            (T('Crear reporte'), request.controller ==
             "reporte" and request.function == "crear", URL('reporte', 'crear')),
            (T('Administrar'), request.controller == "reporte" and request.function ==
             "administrar", URL('reporte', 'administrar')),
        ]),
        (T('Generar informe'), request.controller == "informe" and request.function ==
         "seleccionar_reporte", URL('informe', 'seleccionar_reporte'), []),
        ("Divisor",),
        (T('Eventos'), request.controller == "evento" and (request.function == "crear" or
                                                           request.function == "administrar"), None, [
            (T('Crear evento'), request.controller ==
             "evento" and request.function == "crear", URL('evento', 'crear')),
            (T('Administrar'), request.controller == "evento" and request.function ==
             "administrar", URL('evento', 'administrar')),
        ]),
        (T('Controles de foco'), request.controller == "control_foco" and (request.function == "crear" or
                                                                           request.function == "administrar"), None, [
            (T('Crear control de foco'), request.controller ==
             "control_foco" and request.function == "crear", URL('control_foco', 'crear')),
            (T('Administrar'), request.controller == "control_foco" and request.function ==
             "administrar", URL('control_foco', 'administrar')),
        ]),
    ]
    response.menu.extend(menu_generico)
