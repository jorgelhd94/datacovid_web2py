# Reportes
import datetime


@auth.requires_login()
def administrar():
    reportes = db(db.reporte.id > 0).select()

    if not auth.has_membership("Administrador"):
        provincia = db((db.usuario_provincia.idusuario ==
                        auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()
        reportes = db(db.reporte.idprovincia == provincia.id).select()

    return locals()


@auth.requires_login()
def detalles():
    if not request.args(0):
        redirect(URL('administrar'))    

    reporte = db.reporte(request.args(0, cast=int)
                         ) or redirect(URL('administrar'))
    
    provincia = db((db.usuario_provincia.idusuario ==
                        auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()
    
    if provincia and reporte.idprovincia != provincia.id:
        redirect(URL('administrar'))

    confirmados = db(db.confirmados.idreporte == reporte.id).select().first()
    confirmados_municipios = db(
        db.municipio_confirmados.idconfirmados == confirmados.id).select()
    confirmados_edades = db(
        db.edades_confirmados.idconfirmados == confirmados.id).select()

    activos = db(db.activos.idreporte == reporte.id).select().first()
    activos_ubicacion = db(
        db.ubicacion_activos.idactivos == activos.id).select()

    fallecidos_criticos_graves = db(
        db.fallecidos_criticos_graves.idreporte == reporte.id).select().first()

    sospechosos = db(db.sospechosos.idreporte == reporte.id).select().first()

    casos_ira = db(db.casos_ira.idreporte == reporte.id).select().first()

    atencion_ira = db(db.atencion_ira.idreporte == reporte.id).select().first()

    pesquisa_activa = db(db.pesquisa_activa.idreporte ==
                         reporte.id).select().first()

    eventos = db(db.evento_diario.idreporte == reporte.id).select()

    controles_foco = db(db.control_foco_diario.idreporte ==
                        reporte.id).select()

    movimiento_hospitalario = db(
        db.movimiento_hospitalario.idreporte == reporte.id).select().first()

    vigilancia = db(db.vigilancia.idreporte == reporte.id).select().first()

    origen_muestras = db(db.origen_muestras.idvigilancia ==
                         vigilancia.id).select()

    muestras_pendientes = db(
        db.muestras_pendientes.idreporte == reporte.id).select().first()

    inspeccion_sanitaria_estatal = db(
        db.inspeccion_sanitaria_estatal.idreporte == reporte.id).select().first()

    municipio_no_salieron = db(
        db.municipio_no_salieron.idinspeccion == inspeccion_sanitaria_estatal.id).select()

    municipio_no_medidas = db(
        db.municipio_no_medidas.idinspeccion == inspeccion_sanitaria_estatal.id).select()

    municipio_no_inspectores = db(
        db.municipio_no_inspectores.idinspeccion == inspeccion_sanitaria_estatal.id).select()

    municipio_mayor_notificaciones = db(
        db.municipio_mayor_notificaciones.idinspeccion == inspeccion_sanitaria_estatal.id).select()

    return locals()


@auth.requires_membership("Puesto de mando")
def eliminar():
    if not request.args(0):
        redirect(URL('administrar'))

    provincia = db((db.usuario_provincia.idusuario ==
                        auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()
    
    registro = db.reporte(request.args(0, cast=int)
                          ) or redirect(URL('administrar'))

    if provincia and registro.idprovincia != provincia.id:
        redirect(URL('administrar'))

    x = registro.id
    db(db.reporte.id == x).delete()
    session.status = True
    session.msg = 'Reporte eliminado correctamente'
    redirect(URL("administrar"))

    return dict()


@auth.requires_membership("Puesto de mando")
def crear():
    fecha_reporte = datetime.datetime.now().strftime("%d/%m/%Y")
    return locals()


@auth.requires_membership("Puesto de mando")
def editar():
    if not request.args(0):
        redirect(URL('administrar'))

    provincia = db((db.usuario_provincia.idusuario ==
                        auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()
    
    reporte = db.reporte(request.args(0, cast=int)
                         ) or redirect(URL('administrar'))

    if provincia and reporte.idprovincia != provincia.id:
        redirect(URL('administrar'))

    fecha_reporte = reporte.fecha.strftime("%d/%m/%Y")

    return locals()


@request.restful()
def verificar_fecha():
    response.view = 'generic.json'

    def POST(*args, **vars):
        reporte_existe = False

        provincia = db((db.usuario_provincia.idusuario ==
                        auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

        fecha_reporte = vars["fecha_reporte"].split("/")
        fecha_reporte = "-".join([i for i in reversed(fecha_reporte)])

        if db((db.reporte.fecha == fecha_reporte) & (db.reporte.idprovincia == provincia.id)).select():
            reporte_existe = True

        return dict(reporte_existe=reporte_existe)

    return locals()


# API Crear
@request.restful()
def api():
    response.view = 'generic.json'

    def POST(*args, **vars):
        if not request.env.request_method == 'POST':
            raise HTTP(403)

        # Fecha del reporte
        fecha_reporte = vars["fecha_reporte"].split("/")
        fecha_reporte = "-".join([i for i in reversed(fecha_reporte)])

        provincia = db((db.usuario_provincia.idusuario ==
                        auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

        existe_registro = db((db.reporte.fecha == fecha_reporte) & (db.reporte.idprovincia == provincia.id)).select()

        if not existe_registro:
            idreporte = db.reporte.insert(
                fecha=fecha_reporte, idprovincia=provincia.id)
        else:
            idreporte = db((db.reporte.fecha ==
                            fecha_reporte) & (db.reporte.idprovincia == provincia.id)).select().first().id

        __confirmados(existe_registro, idreporte, **vars)
        __activos(existe_registro, idreporte, **vars)
        __fallecidos_criticos_graves(existe_registro, idreporte, **vars)
        __sospechosos(existe_registro, idreporte, **vars)
        __casos_ira(existe_registro, idreporte, **vars)
        __atencion_ira(existe_registro, idreporte, **vars)
        __pesquisa_activa(existe_registro, idreporte, **vars)
        __eventos(existe_registro, idreporte, **vars)
        __controles_foco(existe_registro, idreporte, **vars)
        __movimiento_hospitalario(existe_registro, idreporte, **vars)
        __vigilancia_origen(existe_registro, idreporte, **vars)
        __muestras_pendientes(existe_registro, idreporte, **vars)
        __inspeccion_sanitaria_estatal(existe_registro, idreporte, **vars)

        return dict(idreporte=idreporte)

    return locals()


# API Crear
@request.restful()
def api_editar():
    response.view = 'generic.json'

    def GET(*args, **vars):
        idreporte = vars["idreporte"]

        datos = {}

        # Confirmados

        datos["confirmados"] = db(
            db.confirmados.idreporte == idreporte).select().first()

        municipios = db((db.municipio_confirmados.idconfirmados == datos["confirmados"]["id"]) &
                        (db.municipio.id == db.municipio_confirmados.idmunicipio)
                        ).select()

        grupo_edades = db((db.edades_confirmados.idconfirmados == datos["confirmados"]["id"]) &
                          (db.grupo_edades.id == db.edades_confirmados.idgrupo_edades)
                          ).select()

        datos["confirmados"]["municipios"] = [{
            "id": i.municipio.id,
            "nombre": i.municipio.nombre,
            "cantidad": i.municipio_confirmados.cantidad
        } for i in municipios]

        datos["confirmados"]["grupo_edades"] = [{
            "id": i.grupo_edades.id,
            "grupo": i.grupo_edades.grupo,
            "cantidad": i.edades_confirmados.cantidad
        } for i in grupo_edades]

        # Activos
        datos["activos"] = db(
            db.activos.idreporte == idreporte).select().first()

        ubicacion = db((db.ubicacion_activos.idactivos == datos["activos"]["id"]) &
                       (db.ubicacion.id == db.ubicacion_activos.idubicacion)
                       ).select()

        datos["activos"]["ubicaciones"] = [{
            "id": i.ubicacion.id,
            "nombre": i.ubicacion.nombre,
            "cantidad": i.ubicacion_activos.cantidad
        } for i in ubicacion]

        # Fallecidos, criticos y graves
        datos["fallecidos"] = db(
            db.fallecidos_criticos_graves.idreporte == idreporte).select().first()

        # Sospechosos
        datos["sospechosos"] = db(
            db.sospechosos.idreporte == idreporte).select().first()

        # casos IRA
        datos["casosIRA"] = db(
            db.casos_ira.idreporte == idreporte).select().first()

        # atencion IRA
        datos["atencionIRA"] = db(
            db.atencion_ira.idreporte == idreporte).select().first()

        # pesquisa activa
        datos["pesquisa_activa"] = db(
            db.pesquisa_activa.idreporte == idreporte).select().first()

        # eventos
        eventos = db((db.evento_diario.idreporte == idreporte) &
                     (db.eventos.id == db.evento_diario.ideventos)
                     ).select()

        datos["eventos"] = [{
            "id": i.eventos.id,
            "nombre": i.eventos.nombre,
            "cantidad": i.evento_diario.cantidad
        } for i in eventos]

        # controles de foco
        controles_foco = db((db.control_foco_diario.idreporte == idreporte) &
                            (db.control_foco.id ==
                             db.control_foco_diario.idcontrol_foco)
                            ).select()

        datos["controles_foco"] = [{
            "id": i.control_foco.id,
            "nombre": i.control_foco.nombre,
            "cantidad": i.control_foco_diario.cantidad
        } for i in controles_foco]

        # movimiento hospitalario
        datos["movimiento_hospitalario"] = db(
            db.movimiento_hospitalario.idreporte == idreporte).select().first()

        # vigilancia
        datos["vigilancia"] = db(
            db.vigilancia.idreporte == idreporte).select().first()

        # Origen
        origen = db((db.origen_muestras.idvigilancia == datos["vigilancia"]["id"]) &
                    (db.origen.id == db.origen_muestras.idorigen)
                    ).select()

        datos["vigilancia"]["origen"] = [{
            "id": i.origen.id,
            "nombre": i.origen.nombre,
            "cantidad": i.origen_muestras.cantidad
        } for i in origen]

        # muestras pendientes
        datos["muestras_pendientes"] = db(
            db.muestras_pendientes.idreporte == idreporte).select().first()

        # muestras pendientes
        datos["inspeccion_sanitaria_estatal"] = db(
            db.inspeccion_sanitaria_estatal.idreporte == idreporte).select().first()

        # municipio no salieron
        municipio_no_salieron = db((db.municipio_no_salieron.idinspeccion == datos["inspeccion_sanitaria_estatal"]["id"]) &
                                   (db.municipio.id ==
                                    db.municipio_no_salieron.idmunicipio)
                                   ).select()

        datos["inspeccion_sanitaria_estatal"]["municipio_no_salieron"] = [{
            "id": i.municipio.id,
            "nombre": i.municipio.nombre,
        } for i in municipio_no_salieron]

        # municipio no medidas
        municipio_no_medidas = db((db.municipio_no_medidas.idinspeccion == datos["inspeccion_sanitaria_estatal"]["id"]) &
                                  (db.municipio.id ==
                                   db.municipio_no_medidas.idmunicipio)
                                  ).select()

        datos["inspeccion_sanitaria_estatal"]["municipio_no_medidas"] = [{
            "id": i.municipio.id,
            "nombre": i.municipio.nombre,
        } for i in municipio_no_medidas]

        # municipio no inspectores
        municipio_no_inspectores = db((db.municipio_no_inspectores.idinspeccion == datos["inspeccion_sanitaria_estatal"]["id"]) &
                                      (db.municipio.id ==
                                       db.municipio_no_inspectores.idmunicipio)
                                      ).select()

        datos["inspeccion_sanitaria_estatal"]["municipio_no_inspectores"] = [{
            "id": i.municipio.id,
            "nombre": i.municipio.nombre,
        } for i in municipio_no_inspectores]

        # municipio mayor notificaciones
        municipio_mayor_notificaciones = db((db.municipio_mayor_notificaciones.idinspeccion == datos["inspeccion_sanitaria_estatal"]["id"]) &
                                            (db.municipio.id ==
                                             db.municipio_mayor_notificaciones.idmunicipio)
                                            ).select()

        datos["inspeccion_sanitaria_estatal"]["municipio_mayor_notificaciones"] = [{
            "id": i.municipio.id,
            "nombre": i.municipio.nombre,
        } for i in municipio_mayor_notificaciones]

        return dict(datos=datos)

    def POST(*args, **vars):
        if not request.env.request_method == 'POST':
            raise HTTP(403)
        
        # Fecha del reporte
        fecha_reporte = vars["fecha_reporte"].split("/")
        fecha_reporte = "-".join([i for i in reversed(fecha_reporte)])

        provincia = db((db.usuario_provincia.idusuario ==
                        auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

        idreporte = vars["idreporte"]
        del vars["idreporte"]        

        acumular = vars["acumular"]

        # Elimino los atributos idreporte que vienen en el diccionario
        for key in vars["datos"]:
            if "idreporte" in vars["datos"][key]:
                del vars["datos"][key]["idreporte"]

        if not acumular:
            db(db.reporte.id == idreporte).update(fecha=fecha_reporte)
            db(db.confirmados.idreporte == idreporte).delete()
            db(db.activos.idreporte == idreporte).delete()
            db(db.fallecidos_criticos_graves.idreporte == idreporte).delete()
            db(db.sospechosos.idreporte == idreporte).delete()
            db(db.casos_ira.idreporte == idreporte).delete()
            db(db.atencion_ira.idreporte == idreporte).delete()
            db(db.pesquisa_activa.idreporte == idreporte).delete()
            db(db.evento_diario.idreporte == idreporte).delete()
            db(db.control_foco_diario.idreporte == idreporte).delete()
            db(db.movimiento_hospitalario.idreporte == idreporte).delete()
            db(db.vigilancia.idreporte == idreporte).delete()
            db(db.muestras_pendientes.idreporte == idreporte).delete()
            db(db.inspeccion_sanitaria_estatal.idreporte == idreporte).delete()
        else:
            # En caso de que exista otro reporte con la nueva fecha los datos seran acumulados
            reporte_nuevo = db((db.reporte.fecha == fecha_reporte) & (db.reporte.idprovincia == provincia.id)).select().first()

            # Se elimina el viejo reporte y se apunta al otro existente
            db(db.reporte.id == idreporte).delete()
            idreporte = reporte_nuevo.id


        # existe_registro = db(db.reporte.fecha == fecha_reporte).select()

        # if not existe_registro:
        #     idreporte = db.reporte.insert(fecha=fecha_reporte)
        # else:
        #     idreporte = db(db.reporte.fecha ==
        #                    fecha_reporte).select().first().id

        __confirmados(acumular, idreporte, **vars)
        __activos(acumular, idreporte, **vars)
        __fallecidos_criticos_graves(acumular, idreporte, **vars)
        __sospechosos(acumular, idreporte, **vars)
        __casos_ira(acumular, idreporte, **vars)
        __atencion_ira(acumular, idreporte, **vars)
        __pesquisa_activa(acumular, idreporte, **vars)
        __eventos(acumular, idreporte, **vars)
        __controles_foco(acumular, idreporte, **vars)
        __movimiento_hospitalario(acumular, idreporte, **vars)
        __vigilancia_origen(acumular, idreporte, **vars)
        __muestras_pendientes(acumular, idreporte, **vars)
        __inspeccion_sanitaria_estatal(acumular, idreporte, **vars)

        return dict(idreporte=idreporte)

    return locals()


# Confirmados. Crear y Acumular


def __confirmados(existe_registro, idreporte, **vars):
    if not existe_registro:
        confirmados = {**vars["datos"]["confirmados"]}
        municipios_confirmados = confirmados.pop("municipios")
        grupo_edades = confirmados.pop("grupo_edades")

        idconfirmados = db.confirmados.insert(
            idreporte=idreporte, **confirmados)

        # Municipios de confirmados
        for m in municipios_confirmados:
            db.municipio_confirmados.insert(
                cantidad=m["cantidad"], idmunicipio=m["id"], idconfirmados=idconfirmados)

        # Grupo de edades de confirmados
        for g in grupo_edades:
            db.edades_confirmados.insert(
                cantidad=g["cantidad"], idgrupo_edades=g["id"], idconfirmados=idconfirmados)
    else:
        confirmados = {**vars["datos"]["confirmados"]}
        municipios_confirmados = confirmados.pop("municipios")
        grupo_edades = confirmados.pop("grupo_edades")

        confirmados_db = db(db.confirmados.idreporte ==
                            idreporte).select().first()

        confirmados_db.update_record(
            total=db.confirmados.total + confirmados["total"],
            sin_fid=db.confirmados.sin_fid + confirmados["sin_fid"],
            sintomaticos=db.confirmados.sintomaticos +
            confirmados["sintomaticos"],
            asintomaticos=db.confirmados.asintomaticos +
            confirmados["asintomaticos"],
            cubanos=db.confirmados.cubanos + confirmados["cubanos"],
            extranjeros=db.confirmados.extranjeros +
            confirmados["extranjeros"],
            masculinos=db.confirmados.masculinos + confirmados["masculinos"],
            femeninos=db.confirmados.femeninos + confirmados["femeninos"],
            contactos=db.confirmados.contactos + confirmados["contactos"],
            casos_aislados=db.confirmados.casos_aislados +
            confirmados["casos_aislados"],
            casos_comunidad=db.confirmados.casos_comunidad +
            confirmados["casos_comunidad"],
            casos_vigilancia_aps=db.confirmados.casos_vigilancia_aps +
            confirmados["casos_vigilancia_aps"],
        )

        # Municipios de confirmados
        for i in municipios_confirmados:
            if db((db.municipio_confirmados.idconfirmados == confirmados_db.id) &
                    (db.municipio_confirmados.idmunicipio == i["id"])
                  ).select():

                db((db.municipio_confirmados.idconfirmados == confirmados_db.id) &
                    (db.municipio_confirmados.idmunicipio == i["id"])).update(
                    cantidad=db.municipio_confirmados.cantidad + i["cantidad"]
                )
            else:
                db.municipio_confirmados.insert(
                    cantidad=i["cantidad"], idmunicipio=i["id"], idconfirmados=confirmados_db.id)

        # Grupo de edades de confirmados
        for i in grupo_edades:
            if db((db.edades_confirmados.idconfirmados == confirmados_db.id) &
                    (db.edades_confirmados.idgrupo_edades == i["id"])
                  ).select():

                db((db.edades_confirmados.idconfirmados == confirmados_db.id) &
                    (db.edades_confirmados.idgrupo_edades == i["id"])).update(
                    cantidad=db.edades_confirmados.cantidad + i["cantidad"]
                )
            else:
                db.edades_confirmados.insert(
                    cantidad=i["cantidad"], idgrupo_edades=i["id"], idconfirmados=confirmados_db.id)


# Activos y su ubucacion. Crear y Acumular

def __activos(existe_registro, idreporte, **vars):
    if not existe_registro:
        activos = {**vars["datos"]["activos"]}
        ubicacion_activos = activos.pop("ubicaciones")

        idactivos = db.activos.insert(idreporte=idreporte, **activos)

        # Ubicacion de los activos
        for i in ubicacion_activos:
            db.ubicacion_activos.insert(
                cantidad=i["cantidad"], idubicacion=i["id"], idactivos=idactivos)

    else:
        activos = {**vars["datos"]["activos"]}
        ubicacion_activos = activos.pop("ubicaciones")

        activos_db = db(db.activos.idreporte ==
                        idreporte).select().first()

        activos_db.update_record(
            total=db.activos.total + activos["total"],
        )

        # Ubicacion de los activos
        for i in ubicacion_activos:
            if db((db.ubicacion_activos.idactivos == activos_db.id) &
                    (db.ubicacion_activos.idubicacion == i["id"])
                  ).select():

                db((db.ubicacion_activos.idactivos == activos_db.id) &
                    (db.ubicacion_activos.idubicacion == i["id"])).update(
                    cantidad=db.ubicacion_activos.cantidad + i["cantidad"]
                )
            else:
                db.ubicacion_activos.insert(
                    cantidad=i["cantidad"], idubicacion=i["id"], idactivos=activos_db.id)


# Fallecidos, casos críticos y casos graves

def __fallecidos_criticos_graves(existe_registro, idreporte, **vars):
    if not existe_registro:
        fallecidos = {**vars["datos"]["fallecidos"]}
        db.fallecidos_criticos_graves.insert(idreporte=idreporte, **fallecidos)
    else:
        fallecidos = {**vars["datos"]["fallecidos"]}

        fallecidos_db = db(db.fallecidos_criticos_graves.idreporte ==
                           idreporte).select().first()

        fallecidos_db.update_record(
            covid_fallecidos=db.fallecidos_criticos_graves.covid_fallecidos +
            fallecidos["covid_fallecidos"],
            covid_criticos=db.fallecidos_criticos_graves.covid_criticos +
            fallecidos["covid_criticos"],
            covid_graves=db.fallecidos_criticos_graves.covid_graves +
            fallecidos["covid_graves"],
            ira_graves=db.fallecidos_criticos_graves.ira_graves +
            fallecidos["ira_graves"],
            ira_graves_pendiente_pcr=db.fallecidos_criticos_graves.ira_graves_pendiente_pcr +
            fallecidos["ira_graves_pendiente_pcr"],
            altas_clinicas_covid=db.fallecidos_criticos_graves.altas_clinicas_covid +
            fallecidos["altas_clinicas_covid"],
            altas_sospechosos=db.fallecidos_criticos_graves.altas_sospechosos +
            fallecidos["altas_sospechosos"],
            altas_contactos=db.fallecidos_criticos_graves.altas_contactos +
            fallecidos["altas_contactos"],
        )


# Sospechosos

def __sospechosos(existe_registro, idreporte, **vars):
    if not existe_registro:
        sospechosos = {**vars["datos"]["sospechosos"]}
        db.sospechosos.insert(idreporte=idreporte, **sospechosos)
    else:
        sospechosos = {**vars["datos"]["sospechosos"]}

        sospechosos_db = db(db.sospechosos.idreporte ==
                            idreporte).select().first()

        sospechosos_db.update_record(
            ingresados=db.sospechosos.ingresados + sospechosos["ingresados"],
            comunidad=db.sospechosos.comunidad + sospechosos["comunidad"],
            iden_hospital=db.sospechosos.iden_hospital +
            sospechosos["iden_hospital"],
            iden_policlinico=db.sospechosos.iden_policlinico +
            sospechosos["iden_policlinico"],
            iden_consultorio=db.sospechosos.iden_consultorio +
            sospechosos["iden_consultorio"],
            iden_pesquisa=db.sospechosos.iden_pesquisa +
            sospechosos["iden_pesquisa"],
        )


# Casos IRA

def __casos_ira(existe_registro, idreporte, **vars):
    if not existe_registro:
        casosIRA = {**vars["datos"]["casosIRA"]}
        db.casos_ira.insert(idreporte=idreporte, **casosIRA)
    else:
        casos_ira = {**vars["datos"]["casosIRA"]}

        casos_ira_db = db(db.casos_ira.idreporte ==
                          idreporte).select().first()

        casos_ira_db.update_record(
            ingresados=db.casos_ira.ingresados + casos_ira["ingresados"],
            comunidad=db.casos_ira.comunidad + casos_ira["comunidad"],
            iden_hospital=db.casos_ira.iden_hospital +
            casos_ira["iden_hospital"],
            iden_policlinico=db.casos_ira.iden_policlinico +
            casos_ira["iden_policlinico"],
            iden_consultorio=db.casos_ira.iden_consultorio +
            casos_ira["iden_consultorio"],
            iden_pesquisa=db.casos_ira.iden_pesquisa +
            casos_ira["iden_pesquisa"],
        )


# Atencion IRA

def __atencion_ira(existe_registro, idreporte, **vars):
    if not existe_registro:
        atencionIRA = {**vars["datos"]["atencionIRA"]}
        db.atencion_ira.insert(idreporte=idreporte, **atencionIRA)
    else:
        atencion_ira = {**vars["datos"]["atencionIRA"]}

        atencion_ira_db = db(db.atencion_ira.idreporte ==
                             idreporte).select().first()

        atencion_ira_db.update_record(
            repor_hospital=db.atencion_ira.repor_hospital +
            atencion_ira["repor_hospital"],
            repor_policlinico=db.atencion_ira.repor_policlinico +
            atencion_ira["repor_policlinico"],
            repor_consultorio=db.atencion_ira.repor_consultorio +
            atencion_ira["repor_consultorio"],
        )


# Pesquisa activa

def __pesquisa_activa(existe_registro, idreporte, **vars):
    if not existe_registro:
        pesquisa_activa = {**vars["datos"]["pesquisa_activa"]}
        db.pesquisa_activa.insert(idreporte=idreporte, **pesquisa_activa)
    else:
        pesquisa_activa = {**vars["datos"]["pesquisa_activa"]}

        pesquisa_activa_db = db(db.pesquisa_activa.idreporte ==
                                idreporte).select().first()

        pesquisa_activa_db.update_record(
            porciento_pesquisada=db.pesquisa_activa.porciento_pesquisada +
            pesquisa_activa["porciento_pesquisada"],
            a_pesquisar=db.pesquisa_activa.a_pesquisar +
            pesquisa_activa["a_pesquisar"],
            presuntas_ira_identificadas=db.pesquisa_activa.presuntas_ira_identificadas +
            pesquisa_activa["presuntas_ira_identificadas"],
            presuntas_ira_atendidas=db.pesquisa_activa.presuntas_ira_atendidas +
            pesquisa_activa["presuntas_ira_atendidas"],
        )


# Eventos

def __eventos(existe_registro, idreporte, **vars):
    eventos = vars["datos"]["eventos"]

    # Fecha del reporte
    fecha_reporte = vars["fecha_reporte"].split("/")
    fecha_reporte = datetime.date(*[int(i) for i in reversed(fecha_reporte)])

    
    for i in eventos:
        if not existe_registro or not db(db.evento_diario.ideventos == i["id"]).select():
            db.evento_diario.insert(
                cantidad=i["cantidad"], ideventos=i["id"], idreporte=idreporte)

            db(db.eventos.id == i["id"]).update(
                fecha_ultimo_caso=fecha_reporte)

            if not db(db.eventos.id == i["id"]).select().first().fecha_apertura:
                db(db.eventos.id == i["id"]).update(fecha_apertura=fecha_reporte)

        else:
            db(db.evento_diario.ideventos == i["id"]).update(
                    cantidad=db.evento_diario.cantidad + i["cantidad"]
                )


# Controles de foco

def __controles_foco(existe_registro, idreporte, **vars):
    controles_foco = vars["datos"]["controles_foco"]

    # Fecha del reporte
    fecha_reporte = vars["fecha_reporte"].split("/")
    fecha_reporte = datetime.date(*[int(i) for i in reversed(fecha_reporte)])

    for i in controles_foco:
        if not existe_registro or not db(db.control_foco_diario.idcontrol_foco == i["id"]).select():
            db.control_foco_diario.insert(
                cantidad=i["cantidad"], idcontrol_foco=i["id"], idreporte=idreporte)

            db(db.control_foco.id == i["id"]).update(
                fecha_ultimo_caso=fecha_reporte)

            if not db(db.control_foco.id == i["id"]).select().first().fecha_apertura:
                db(db.control_foco.id == i["id"]).update(fecha_apertura=fecha_reporte)

        else:
            db(db.control_foco_diario.idcontrol_foco == i["id"]).update(
                    cantidad=db.control_foco_diario.cantidad + i["cantidad"]
                )

# Movimiento hospitalario

def __movimiento_hospitalario(existe_registro, idreporte, **vars):
    movimiento_hospitalario = {**vars["datos"]["movimiento_hospitalario"]}

    if not existe_registro:
        db.movimiento_hospitalario.insert(
            idreporte=idreporte, **movimiento_hospitalario)

    else:
        movimiento_hospitalario_db = db(db.movimiento_hospitalario.idreporte ==
                                        idreporte).select().first()

        movimiento_hospitalario_db.update_record(
            ingresados=db.movimiento_hospitalario.ingresados +
            movimiento_hospitalario["ingresados"],

            confirmados_ingresados=db.movimiento_hospitalario.confirmados_ingresados +
            movimiento_hospitalario["confirmados_ingresados"],

            sospechosos_ingresados=db.movimiento_hospitalario.sospechosos_ingresados +
            movimiento_hospitalario["sospechosos_ingresados"],

            contactos_ingresados=db.movimiento_hospitalario.contactos_ingresados +
            movimiento_hospitalario["contactos_ingresados"],

            disponibilidad_camas_ingreso=db.movimiento_hospitalario.disponibilidad_camas_ingreso +
            movimiento_hospitalario["disponibilidad_camas_ingreso"],

            disponibilidad_camas_graves=db.movimiento_hospitalario.disponibilidad_camas_graves +
            movimiento_hospitalario["disponibilidad_camas_graves"],

            disponibilidad_camas_sospechosos=db.movimiento_hospitalario.disponibilidad_camas_sospechosos +
            movimiento_hospitalario["disponibilidad_camas_sospechosos"],

            disponibilidad_camas_contactos=db.movimiento_hospitalario.disponibilidad_camas_contactos +
            movimiento_hospitalario["disponibilidad_camas_contactos"],
        )


# Vigilancia y origen de muestras


def __vigilancia_origen(existe_registro, idreporte, **vars):
    vigilancia = {**vars["datos"]["vigilancia"]}
    origen = vigilancia.pop("origen")

    if not existe_registro:
        idvigilancia = db.vigilancia.insert(idreporte=idreporte, **vigilancia)

        # Origen de las muestras
        for o in origen:
            db.origen_muestras.insert(
                cantidad=o["cantidad"], idorigen=o["id"], idvigilancia=idvigilancia)
    else:
        vigilancia_db = db(db.vigilancia.idreporte ==
                           idreporte).select().first()

        vigilancia_db.update_record(
            muestras_tomadas=db.vigilancia.muestras_tomadas +
            vigilancia["muestras_tomadas"],
            muestras_enviadas=db.vigilancia.muestras_enviadas +
            vigilancia["muestras_enviadas"],
            muestras_eventos=db.vigilancia.muestras_eventos +
            vigilancia["muestras_eventos"],
            muestras_control_foco=db.vigilancia.muestras_control_foco +
            vigilancia["muestras_control_foco"],
            acumuladas_enviadas=db.vigilancia.acumuladas_enviadas +
            vigilancia["acumuladas_enviadas"],
            resultados_positivos=db.vigilancia.resultados_positivos +
            vigilancia["resultados_positivos"],
            resultados_confirmatorios=db.vigilancia.resultados_confirmatorios +
            vigilancia["resultados_confirmatorios"],
            resultados_negativos=db.vigilancia.resultados_negativos +
            vigilancia["resultados_negativos"],
            resultados_evolutivos=db.vigilancia.resultados_evolutivos +
            vigilancia["resultados_evolutivos"],
            resultados_inhibidos=db.vigilancia.resultados_inhibidos +
            vigilancia["resultados_inhibidos"],
            tiempo_promedio_salida=db.vigilancia.tiempo_promedio_salida +
            vigilancia["tiempo_promedio_salida"],
            tiempo_promedio_resultado=db.vigilancia.tiempo_promedio_resultado +
            vigilancia["tiempo_promedio_resultado"],
        )

        # Origen de las muestras
        for i in origen:
            if db((db.origen_muestras.idvigilancia == vigilancia_db.id) &
                    (db.origen_muestras.idorigen == i["id"])
                  ).select():

                db((db.origen_muestras.idvigilancia == vigilancia_db.id) &
                    (db.origen_muestras.idorigen == i["id"])).update(
                    cantidad=db.origen_muestras.cantidad + i["cantidad"]
                )
            else:
                db.origen_muestras.insert(
                    cantidad=i["cantidad"], idorigen=i["id"], idvigilancia=vigilancia_db.id)


# Muestras pendientes

def __muestras_pendientes(existe_registro, idreporte, **vars):
    muestras_pendientes = {**vars["datos"]["muestras_pendientes"]}

    if not existe_registro:
        db.muestras_pendientes.insert(
            idreporte=idreporte, **muestras_pendientes)

    else:
        muestras_pendientes_db = db(db.muestras_pendientes.idreporte ==
                                    idreporte).select().first()

        muestras_pendientes_db.update_record(
            con_2_dias=db.muestras_pendientes.con_2_dias +
            muestras_pendientes["con_2_dias"],
            con_mas_3_dias=db.muestras_pendientes.con_mas_3_dias +
            muestras_pendientes["con_mas_3_dias"],
        )

# Inspección Sanitaria Estatal


def __inspeccion_sanitaria_estatal(existe_registro, idreporte, **vars):
    inspeccion_sanitaria_estatal = {
        **vars["datos"]["inspeccion_sanitaria_estatal"]}

    municipio_no_salieron = inspeccion_sanitaria_estatal.pop(
        "municipio_no_salieron")
    municipio_no_medidas = inspeccion_sanitaria_estatal.pop(
        "municipio_no_medidas")
    municipio_no_inspectores = inspeccion_sanitaria_estatal.pop(
        "municipio_no_inspectores")
    municipio_mayor_notificaciones = inspeccion_sanitaria_estatal.pop(
        "municipio_mayor_notificaciones")

    if not existe_registro:
        idinspeccion = db.inspeccion_sanitaria_estatal.insert(
            idreporte=idreporte, **inspeccion_sanitaria_estatal)

        # Municipios que no salieron
        for i in municipio_no_salieron:
            db.municipio_no_salieron.insert(
                idmunicipio=i["id"], idinspeccion=idinspeccion)

        # Municipios que no tomaron medidas
        for i in municipio_no_medidas:
            db.municipio_no_medidas.insert(
                idmunicipio=i["id"], idinspeccion=idinspeccion)

        # Municipios sin inspectores
        for i in municipio_no_inspectores:
            db.municipio_no_inspectores.insert(
                idmunicipio=i["id"], idinspeccion=idinspeccion)

        # Municipios con mayor notificaciones
        for i in municipio_mayor_notificaciones:
            db.municipio_mayor_notificaciones.insert(
                idmunicipio=i["id"], idinspeccion=idinspeccion)

    else:
        inspeccion_sanitaria_db = db(db.inspeccion_sanitaria_estatal.idreporte ==
                                     idreporte).select().first()

        inspeccion_sanitaria_db.update_record(
            centros_visitados=db.inspeccion_sanitaria_estatal.centros_visitados +
            inspeccion_sanitaria_estatal["centros_visitados"],
            centros_inspeccionados=db.inspeccion_sanitaria_estatal.centros_inspeccionados +
            inspeccion_sanitaria_estatal["centros_inspeccionados"],
            inspectores_salieron=db.inspeccion_sanitaria_estatal.inspectores_salieron +
            inspeccion_sanitaria_estatal["inspectores_salieron"],
            medidas_impuestas=db.inspeccion_sanitaria_estatal.medidas_impuestas +
            inspeccion_sanitaria_estatal["medidas_impuestas"],
        )

        # Municipios que no salieron
        for i in municipio_no_salieron:
            if not db((db.municipio_no_salieron.idinspeccion == inspeccion_sanitaria_db.id) &
                      (db.municipio_no_salieron.idmunicipio == i["id"])).select():

                db.municipio_no_salieron.insert(
                    idmunicipio=i["id"], idinspeccion=inspeccion_sanitaria_db.id)

        # Municipios que no tomaron medidas
        for i in municipio_no_medidas:
            if not db((db.municipio_no_medidas.idinspeccion == inspeccion_sanitaria_db.id) &
                      (db.municipio_no_medidas.idmunicipio == i["id"])).select():

                db.municipio_no_medidas.insert(
                    idmunicipio=i["id"], idinspeccion=inspeccion_sanitaria_db.id)

        # Municipios sin inspectores
        for i in municipio_no_inspectores:
            if not db((db.municipio_no_inspectores.idinspeccion == inspeccion_sanitaria_db.id) &
                      (db.municipio_no_inspectores.idmunicipio == i["id"])).select():

                db.municipio_no_inspectores.insert(
                    idmunicipio=i["id"], idinspeccion=inspeccion_sanitaria_db.id)

        # Municipios con mayor notificaciones
        for i in municipio_mayor_notificaciones:
            if not db((db.municipio_mayor_notificaciones.idinspeccion == inspeccion_sanitaria_db.id) &
                      (db.municipio_mayor_notificaciones.idmunicipio == i["id"])).select():

                db.municipio_mayor_notificaciones.insert(
                    idmunicipio=i["id"], idinspeccion=inspeccion_sanitaria_db.id)
