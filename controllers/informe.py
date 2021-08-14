# -*- coding: utf-8 -*-
import datetime


@auth.requires_login()
def seleccionar_reporte():
    reportes = db(db.reporte.id > 0).select()

    if not auth.has_membership("Administrador"):
        provincia = db((db.usuario_provincia.idusuario ==
                        auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()
        reportes = db(db.reporte.idprovincia == provincia.id).select()

    return locals()


@auth.requires_login()
def redirigir_pdf():
    if not request.args(0):
        redirect(URL('seleccionar_reporte'))

    session.reporte = db.reporte(request.args(0, cast=int)
                                 ) or redirect(URL('seleccionar_reporte'))

    redirect(URL('documento.pdf'))
    return locals()


@auth.requires_login()
def documento():
    if not session.reporte:
        redirect(URL("seleccionar_reporte"))

    from gluon.contrib.pyfpdf import FPDF, HTMLMixin

    response.title = "Situación epidemiológica de la COVID-19"

    if request.extension == "pdf":
        provincia = db(db.provincia.id ==
                       session.reporte.idprovincia).select().first()

        class MyFPDF(FPDF, HTMLMixin):
            def header(self):
                """
                define doc header
                """
                self.set_font('Arial', 'B', 15)
                self.cell(0, 10, response.title, ln=1, align="C")
                self.cell(
                    0, 3, f"Reporte del día {session.reporte.fecha.strftime('%d/%m/%Y')} - {provincia.nombre}", align="C", ln=1)

                self.ln(15)

        pdf = MyFPDF()
        pdf.add_page()

        idreporte = session.reporte.id

        __confirmados(pdf, idreporte)
        pdf.ln(5)
        __sospechosos_ira(pdf, idreporte)
        pdf.ln(5)
        __movimiento_hospitalario(pdf, idreporte)
        pdf.ln(5)
        __fallecidos_criticos_graves(pdf, idreporte)
        pdf.ln(5)
        __eventos(pdf, idreporte)
        pdf.ln(5)
        __controles_foco(pdf, idreporte)
        pdf.ln(5)
        __pesquisa_activa(pdf, idreporte)
        pdf.ln(5)
        __vigilancia(pdf, idreporte)
        pdf.ln(5)
        __inspeccion_sanitaria_estatal(pdf, idreporte)

        response.headers['Content-Type'] = 'application/pdf'
        return pdf.output(dest='S')
    else:
        return dict()


def __margen(pdf, margen=10):
    pdf.cell(margen)


def __fin_de_parrafo(pdf):
    pdf.cell(0, 3,  "", 0, ln=1)


def __confirmados(pdf, idreporte):
    confirmados = db(db.confirmados.idreporte == idreporte).select().first()

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, "- Confirmados y Activos:", 0, ln=1)

    pdf.set_font('Arial', '', 12)

    # 1
    __margen(pdf)
    pdf.cell(
        0, 10,  f"1. Casos confirmados en el día: {confirmados.total}", 0, ln=1)

    # 2
    __margen(pdf)
    sum = db.municipio_confirmados.cantidad.sum()
    sum = db(db.municipio_confirmados.idconfirmados ==
             confirmados.id).select(sum).first()[sum]

    pdf.cell(
        0, 8,  f"2. Casos confirmados en el día por municipios: {sum or 0}", 0, ln=3)

    __margen(pdf)
    for i in db(db.municipio_confirmados.idconfirmados == confirmados.id).select():
        pdf.cell(0, 8,  f"- {i.idmunicipio.nombre}: {i.cantidad}", 0, ln=2)

    __fin_de_parrafo(pdf)

    # 3
    __margen(pdf)
    pdf.cell(0, 8,  "3. Casos según nacionalidad:", 0, ln=3)
    __margen(pdf)
    pdf.cell(0, 8,  f"- Cubanos: {confirmados.cubanos}", 0, ln=2)
    pdf.cell(0, 8,  f"- Extranjeros: {confirmados.extranjeros}", 0, ln=2)
    __fin_de_parrafo(pdf)

    # 4
    __margen(pdf)
    pdf.cell(
        0, 10,  f"4. Casos sin fuente de infección precisada: {confirmados.sin_fid}", 0, ln=1)

    # 5
    __margen(pdf)
    pdf.cell(0, 8,  "5. Casos según sexo:", 0, ln=3)
    __margen(pdf)
    pdf.cell(0, 8,  f"- Masculinos: {confirmados.masculinos}", 0, ln=2)
    pdf.cell(0, 8,  f"- Femeninos: {confirmados.femeninos}", 0, ln=2)
    __fin_de_parrafo(pdf)

    # 6
    __margen(pdf)
    sum = db.edades_confirmados.cantidad.sum()
    sum = db(db.edades_confirmados.idconfirmados ==
             confirmados.id).select(sum).first()[sum]

    pdf.cell(0, 8,  f"6. Casos según grupos de edades: {sum or 0}", 0, ln=3)

    __margen(pdf)
    for i in db(db.edades_confirmados.idconfirmados == confirmados.id).select():
        pdf.cell(0, 8,  f"- {i.idgrupo_edades.grupo}: {i.cantidad}", 0, ln=2)

    __fin_de_parrafo(pdf)

    # 7
    __margen(pdf)
    pdf.cell(
        0, 10,  f"7. Casos confirmados en el día sintomáticos: {confirmados.sintomaticos}", 0, ln=1)

    # 8
    __margen(pdf)
    pdf.cell(
        0, 10,  f"8. Casos confirmados en el día asintomáticos: {confirmados.asintomaticos}", 0, ln=1)

    # 9
    __margen(pdf)
    pdf.cell(
        0, 10,  f"9. Total de contactos a partir de las encuestas: {confirmados.contactos}", 0, ln=1)

    # 10
    __margen(pdf)
    pdf.cell(
        0, 10,  f"10. Promedio de contactos por caso: {confirmados.promedio_contactos_por_caso or 0}", 0, ln=1)

    # 11
    __margen(pdf)
    pdf.cell(
        0, 10,  f"11. Número de casos que se encontraban aislados: {confirmados.casos_aislados}", 0, ln=1)

    # 12
    __margen(pdf)
    pdf.cell(
        0, 10,  f"12. Número de casos que se encontraban en la comunidad: {confirmados.casos_comunidad}", 0, ln=1)

    # 13
    __margen(pdf)
    pdf.cell(
        0, 10,  f"13. Número de casos que se encontraban en vigiliancia APS: {confirmados.casos_vigilancia_aps}", 0, ln=1)

    # 14
    activos = db(db.activos.idreporte == idreporte).select().first()

    __margen(pdf)
    pdf.cell(0, 10,  f"14. Casos activos ingresados: {activos.total}", 0, ln=3)

    if activos.total:
        __margen(pdf)
        pdf.cell(0, 8,  "Ubicación de los casos activos", 0, ln=2)

        for i in db(db.ubicacion_activos.idactivos == activos.id).select():
            pdf.cell(0, 8,  f"- {i.idubicacion.nombre}: {i.cantidad}", 0, ln=2)

    __fin_de_parrafo(pdf)


def __sospechosos_ira(pdf, idreporte):
    sospechosos = db(db.sospechosos.idreporte == idreporte).select().first()
    casos_ira = db(db.casos_ira.idreporte == idreporte).select().first()
    atencion_ira = db(db.atencion_ira.idreporte == idreporte).select().first()

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, "- Casos Sospechosos e IRA:", 0, ln=1)

    pdf.set_font('Arial', '', 12)

    # Sospechosos

    # 1
    __margen(pdf)
    pdf.cell(
        0, 10,  f"1. Casos sospechosos reportados en el día: {sospechosos.total}", 0, ln=1)

    # 2
    __margen(pdf)
    pdf.cell(
        0, 10,  f"2. Casos sospechosos ingresados: {sospechosos.ingresados}", 0, ln=1)

    # 3
    __margen(pdf)
    pdf.cell(
        0, 10,  f"3. Casos sospechosos en la comunidad: {sospechosos.comunidad}", 0, ln=1)

    # 4
    __margen(pdf)
    pdf.cell(
        0, 10,  f"4. Casos sospechosos identificados en hospitales: {sospechosos.iden_hospital}", 0, ln=1)

    # 5
    __margen(pdf)
    pdf.cell(
        0, 10,  f"5. Casos sospechosos identificados en policlínicos: {sospechosos.iden_policlinico}", 0, ln=1)

    # 6
    __margen(pdf)
    pdf.cell(
        0, 10,  f"6. Casos sospechosos identificados en los consultorios: {sospechosos.iden_consultorio}", 0, ln=1)

    # 7
    __margen(pdf)
    pdf.cell(
        0, 10,  f"7. Casos sospechosos identificados por la pesquisa: {sospechosos.iden_pesquisa}", 0, ln=1)

    pdf.ln(5)

    # casos IRA

    # 8
    __margen(pdf)
    pdf.cell(
        0, 10,  f"8. Casos IRA reportados en el día: {casos_ira.total}", 0, ln=1)

    # 9
    __margen(pdf)
    pdf.cell(
        0, 10,  f"9. Casos IRA ingresados: {casos_ira.ingresados}", 0, ln=1)

    # 10
    __margen(pdf)
    pdf.cell(
        0, 10,  f"10. Casos IRA en la comunidad: {casos_ira.comunidad}", 0, ln=1)

    # 11
    __margen(pdf)
    pdf.cell(
        0, 10,  f"11. Casos IRA identificados en hospitales: {casos_ira.iden_hospital}", 0, ln=1)

    # 12
    __margen(pdf)
    pdf.cell(
        0, 10,  f"12. Casos IRA identificados en policlínicos: {casos_ira.iden_policlinico}", 0, ln=1)

    # 13
    __margen(pdf)
    pdf.cell(
        0, 10,  f"13. Casos IRA identificados en los consultorios: {casos_ira.iden_consultorio}", 0, ln=1)

    # 14
    __margen(pdf)
    pdf.cell(
        0, 10,  f"14. Casos IRA identificados por la pesquisa: {casos_ira.iden_pesquisa}", 0, ln=1)

    pdf.ln(5)

    # atención x IRA

    # 15
    __margen(pdf)
    pdf.cell(
        0, 10,  f"15. Atenciones médicas por IRA reportadas en el día: {atencion_ira.total}", 0, ln=1)

    # 16
    __margen(pdf)
    pdf.cell(
        0, 10,  f"16. Atenciones por IRA reportadas por por Hospitales: {atencion_ira.repor_hospital}", 0, ln=1)

    # 17
    __margen(pdf)
    pdf.cell(
        0, 10,  f"17. Atenciones por IRA reportadas por Policlínicos: {atencion_ira.repor_policlinico}", 0, ln=1)

    # 18
    __margen(pdf)
    pdf.cell(
        0, 10,  f"18. Atenciones por IRA reportadas por Consultorios: {atencion_ira.repor_consultorio}", 0, ln=1)


def __movimiento_hospitalario(pdf, idreporte):
    movimiento_hospitalario = db(
        db.movimiento_hospitalario.idreporte == idreporte).select().first()

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, "- Movimiento Hospitalario:", 0, ln=1)

    pdf.set_font('Arial', '', 12)

    # Movimiento Hospitalario

    # 1
    __margen(pdf)
    pdf.cell(
        0, 10,  f"1. Pacientes ingresados en el día: {movimiento_hospitalario.ingresados}", 0, ln=1)

    # 2
    __margen(pdf)
    pdf.cell(
        0, 10,  f"2. Casos confirmados ingresados en el día: {movimiento_hospitalario.confirmados_ingresados}", 0, ln=1)

    # 3
    __margen(pdf)
    pdf.cell(
        0, 10,  f"3. Casos sospechosos ingresados en el día: {movimiento_hospitalario.sospechosos_ingresados}", 0, ln=1)

    # 4
    __margen(pdf)
    pdf.cell(
        0, 10,  f"4. Contactos ingresados en el día: {movimiento_hospitalario.contactos_ingresados}", 0, ln=1)

    # 5
    __margen(pdf)
    pdf.cell(
        0, 10,  f"5. Disponibilidad de camas totales para ingresos: {movimiento_hospitalario.disponibilidad_camas_ingreso}", 0, ln=1)

    # 6
    __margen(pdf)
    pdf.cell(
        0, 10,  f"6. Disponibilidad de camas totales para atención al grave: {movimiento_hospitalario.disponibilidad_camas_graves}", 0, ln=1)

    # 7
    __margen(pdf)
    pdf.cell(
        0, 10,  f"7. Disponibilidad de camas totales para casos sospechosos: {movimiento_hospitalario.disponibilidad_camas_sospechosos}", 0, ln=1)

    # 8
    __margen(pdf)
    pdf.cell(
        0, 10,  f"8. Disponibilidad de camas totales para contactos: {movimiento_hospitalario.disponibilidad_camas_contactos}", 0, ln=1)


def __fallecidos_criticos_graves(pdf, idreporte):
    fallecidos_criticos_graves = db(
        db.fallecidos_criticos_graves.idreporte == idreporte).select().first()

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, "- Fallecidos, casos críticos y casos graves:", 0, ln=1)

    pdf.set_font('Arial', '', 12)

    # Fallecidos, casos críticos y casos graves

    # 1
    __margen(pdf)
    pdf.cell(
        0, 10,  f"1. Pacientes de COVID fallecidos en el día: {fallecidos_criticos_graves.covid_fallecidos}", 0, ln=1)

    # 2
    __margen(pdf)
    pdf.cell(
        0, 10,  f"2. Pacientes de COVID críticos en el día: {fallecidos_criticos_graves.covid_criticos}", 0, ln=1)

    # 3
    __margen(pdf)
    pdf.cell(
        0, 10,  f"3. Pacientes de COVID graves en el día: {fallecidos_criticos_graves.covid_graves}", 0, ln=1)

    # 4
    __margen(pdf)
    pdf.cell(
        0, 10,  f"4. Pacientes de IRA graves reportados en el día: {fallecidos_criticos_graves.ira_graves}", 0, ln=1)

    # 5
    __margen(pdf)
    pdf.cell(
        0, 10,  f"5. Pacientes de IRA graves pendientes de resultados de PCR: {fallecidos_criticos_graves.ira_graves_pendiente_pcr}", 0, ln=1)

    # 6
    __margen(pdf)
    pdf.cell(
        0, 10,  f"6. Altas clínicas a pacientes de Covid en el día: {fallecidos_criticos_graves.altas_clinicas_covid}", 0, ln=1)

    # 7
    __margen(pdf)
    pdf.cell(
        0, 10,  f"7. Altas a sospechosos dadas en el día: {fallecidos_criticos_graves.altas_sospechosos}", 0, ln=1)

    # 8
    __margen(pdf)
    pdf.cell(
        0, 10,  f"8. Altas a contactos dadas en el día: {fallecidos_criticos_graves.altas_contactos}", 0, ln=1)


def __eventos(pdf, idreporte):
    fecha_actual = datetime.datetime.now().date()
    reporte = db(db.reporte.id == idreporte).select().first()
    fecha_reporte = reporte.fecha
    provincia = db(db.provincia.id == reporte.idprovincia).select().first()

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, "- Eventos:", 0, ln=1)

    pdf.set_font('Arial', '', 12)

    consulta_provincia = (db.eventos.idmunicipio == db.municipio.id) & (
        db.municipio.idprovincia == provincia.id)
    # Eventos

    # 1
    eventos_abiertos = db((db.eventos.estado == "Abierto") & consulta_provincia).select(db.eventos.ALL).find(
        lambda row: row.fecha_apertura <= fecha_reporte if row.fecha_apertura else False)

    __margen(pdf)
    pdf.cell(
        0, 8,  f"1. Eventos abiertos: {0 if not eventos_abiertos else ''}", 0, ln=1 if not eventos_abiertos else 3)

    if eventos_abiertos:
        __margen(pdf)
        for i in eventos_abiertos:
            sum = db.evento_diario.cantidad.sum()
            sum = db(db.evento_diario.ideventos ==
                     i.id).select(sum).first()[sum]

            msg = f"- El evento {i.tipo_evento} \"{i.nombre}\" tiene un acumulado de {sum or 0} caso(s)." + \
                f" El último caso registrado fue el {i.fecha_ultimo_caso.strftime('%d/%m/%Y')}." + \
                f" La fecha de cierre es el {i.fecha_cierre}."

            pdf.multi_cell(0, 8,  msg, 0)
            pdf.ln(4)
            pdf.cell(20)

        __fin_de_parrafo(pdf)

    # 2
    eventos_abiertos_hoy = db((db.eventos.fecha_apertura == fecha_reporte)
                              & consulta_provincia).select(db.eventos.ALL)

    __margen(pdf)
    pdf.cell(
        0, 10,  f"2. Eventos abiertos en el día: {0 if not eventos_abiertos_hoy else ''}", 0, ln=1 if not eventos_abiertos_hoy else 3)

    if eventos_abiertos_hoy:
        __margen(pdf)

        # Institucionales

        eventos_institucionales = eventos_abiertos_hoy.find(
            lambda row: row.tipo_evento == "Institucional")

        pdf.set_font('Arial', 'B', 12)
        pdf.cell(
            0, 8,  f"Institucionales: {0 if not eventos_institucionales else ''}", 0, ln=3)
        pdf.set_font('Arial', '', 12)
        for i in eventos_institucionales:
            sum = db.evento_diario.cantidad.sum()
            sum = db(db.evento_diario.ideventos ==
                     i.id).select(sum).first()[sum]

            msg = f"- {i.nombre}: {sum} caso(s)."

            pdf.multi_cell(0, 4,  msg, 0)
            pdf.ln(4)
            pdf.cell(20)

        # Comunitarios
        eventos_comunitario = eventos_abiertos_hoy.find(
            lambda row: row.tipo_evento == "Comunitario")

        pdf.set_font('Arial', 'B', 12)
        pdf.cell(
            0, 8,  f"Comunitarios: {0 if not eventos_comunitario else ''}", 0, ln=3)
        pdf.set_font('Arial', '', 12)
        for i in eventos_comunitario:
            sum = db.evento_diario.cantidad.sum()
            sum = db(db.evento_diario.ideventos ==
                     i.id).select(sum).first()[sum]

            msg = f"- {i.nombre}: {sum} caso(s)."

            pdf.multi_cell(0, 4,  msg, 0)
            pdf.ln(4)
            pdf.cell(20)

        __fin_de_parrafo(pdf)

    # 3
    delta_15 = datetime.timedelta(days=15)

    # Traer los eventos sin casos en lo ultimos 15 dias, pero mayor de 30 dias atras.
    eventos_sin_casos = db(
        (db.eventos.fecha_ultimo_caso < fecha_actual - delta_15) & (db.eventos.estado == "Abierto") & consulta_provincia).select(db.eventos.ALL)

    __margen(pdf)
    pdf.cell(
        0, 10,  f"3. Eventos abiertos sin casos en los últimos 15 días: {0 if not eventos_sin_casos else ''}", 0, ln=1 if not eventos_sin_casos else 3)

    if eventos_sin_casos:
        __margen(pdf)
        for i in eventos_sin_casos:
            sum = db.evento_diario.cantidad.sum()
            sum = db(db.evento_diario.ideventos ==
                     i.id).select(sum).first()[sum]

            msg = f"- El evento {i.tipo_evento} \"{i.nombre}\" tiene un acumulado de {sum or 0} caso(s)." + \
                f" El último caso registrado fue el {i.fecha_ultimo_caso.strftime('%d/%m/%Y')}."

            pdf.multi_cell(0, 8,  msg, 0)
            pdf.ln(4)
            pdf.cell(20)

        __fin_de_parrafo(pdf)


def __controles_foco(pdf, idreporte):
    fecha_actual = datetime.datetime.now().date()

    reporte = db(db.reporte.id == idreporte).select().first()
    fecha_reporte = reporte.fecha

    provincia = db(db.provincia.id == reporte.idprovincia).select().first()

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, "- Controles de foco:", 0, ln=1)

    pdf.set_font('Arial', '', 12)

    consulta_provincia = (db.control_foco.idmunicipio == db.municipio.id) & (
        db.municipio.idprovincia == provincia.id)

    # Controles de foco

    # 1
    control_foco_abiertos = db((db.control_foco.estado == "Abierto") & consulta_provincia).select(db.control_foco.ALL).find(
        lambda row: row.fecha_apertura <= fecha_reporte if row.fecha_apertura else False)

    __margen(pdf)
    pdf.cell(
        0, 8,  f"1. Controles de foco abiertos: {0 if not control_foco_abiertos else ''}", 0, ln=1 if not control_foco_abiertos else 3)

    if control_foco_abiertos:
        __margen(pdf)
        for i in control_foco_abiertos:
            sum = db.control_foco_diario.cantidad.sum()
            sum = db(db.control_foco_diario.idcontrol_foco ==
                     i.id).select(sum).first()[sum]

            msg = f"- El control de foco \"{i.nombre}\" tiene un acumulado de {sum or 0} caso(s)." + \
                f" El último caso registrado fue el {i.fecha_ultimo_caso.strftime('%d/%m/%Y')}." + \
                f" La fecha de cierre es el {i.fecha_cierre}."

            pdf.multi_cell(0, 8,  msg, 0)
            pdf.ln(4)
            pdf.cell(20)

        __fin_de_parrafo(pdf)

    # 2
    control_foco_abiertos_hoy = db(db.control_foco.fecha_apertura == fecha_reporte).select(db.control_foco.ALL)


    __margen(pdf)
    pdf.cell(
        0, 10,  f"2. Controles de foco abiertos en el día: {0 if not control_foco_abiertos_hoy else ''}", 0, ln=1 if not control_foco_abiertos_hoy else 3)

    if control_foco_abiertos_hoy:
        __margen(pdf)

        for i in control_foco_abiertos_hoy:
            sum = db.control_foco_diario.cantidad.sum()
            sum = db(db.control_foco_diario.idcontrol_foco ==
                     i.id).select(sum).first()[sum]

            msg = f"- {i.nombre}: {sum} caso(s)."

            pdf.multi_cell(0, 4,  msg, 0)
            pdf.ln(4)
            pdf.cell(20)

        __fin_de_parrafo(pdf)

    # 3
    delta_15 = datetime.timedelta(days=15)

    # Traer los controles de foco abiertos sin casos en lo ultimos 15 dias.
    cf_sin_casos = db((db.control_foco.fecha_ultimo_caso < fecha_actual - delta_15)
                      & (db.control_foco.estado == "Abierto") & consulta_provincia).select(db.control_foco.ALL)

    __margen(pdf)
    pdf.cell(
        0, 10,  f"3. Controles de foco abiertos sin casos en los últimos 15 días: {0 if not cf_sin_casos else ''}", 0, ln=1 if not cf_sin_casos else 3)

    if cf_sin_casos:
        __margen(pdf)
        for i in cf_sin_casos:
            sum = db.control_foco_diario.cantidad.sum()
            sum = db(db.control_foco_diario.idcontrol_foco ==
                     i.id).select(sum).first()[sum]

            msg = f"- El control de foco \"{i.nombre}\" tiene un acumulado de {sum or 0} caso(s)." + \
                f" El último caso registrado fue el {i.fecha_ultimo_caso.strftime('%d/%m/%Y')}."

            pdf.multi_cell(0, 8,  msg, 0)
            pdf.ln(4)
            pdf.cell(20)

        __fin_de_parrafo(pdf)


def __pesquisa_activa(pdf, idreporte):
    pesquisa_activa = db(
        db.pesquisa_activa.idreporte == idreporte).select().first()

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, "- Pesquisa activa:", 0, ln=1)

    pdf.set_font('Arial', '', 12)

    # Fallecidos, casos críticos y casos graves

    # 1
    __margen(pdf)
    pdf.cell(
        0, 10,  f"1. Porciento de población pesquisada: {pesquisa_activa.porciento_pesquisada}", 0, ln=1)

    # 2
    __margen(pdf)
    pdf.cell(
        0, 10,  f"2. Población a pesquisar: {pesquisa_activa.a_pesquisar}", 0, ln=1)

    # 3
    __margen(pdf)
    pdf.cell(
        0, 10,  f"3. Presuntas IRA identificadas: {pesquisa_activa.presuntas_ira_identificadas}", 0, ln=1)

    # 4
    __margen(pdf)
    pdf.cell(
        0, 10,  f"4. Presuntas IRA atendidas: {pesquisa_activa.presuntas_ira_atendidas}", 0, ln=1)

    # 5
    __margen(pdf)
    pdf.cell(
        0, 10,  f"5. Porciento que representa el 0,01 % de los pesquisados: {round(pesquisa_activa.porciento_001, 8)}", 0, ln=1)


def __vigilancia(pdf, idreporte):
    vigilancia = db(
        db.vigilancia.idreporte == idreporte).select().first()

    muestras_pendientes = db(
        db.muestras_pendientes.idreporte == idreporte).select().first()

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, "- Vigilancia Microbiológica:", 0, ln=1)

    pdf.set_font('Arial', '', 12)

    # Vigilancia Microbiológica

    # 1
    __margen(pdf)
    pdf.cell(
        0, 10,  f"1. Muestras tomadas en el día: {vigilancia.muestras_tomadas}", 0, ln=1)

    # 2
    __margen(pdf)
    pdf.cell(
        0, 10,  f"2. Muestras enviadas en el día: {vigilancia.muestras_enviadas}", 0, ln=1)

    # 3
    __margen(pdf)
    pdf.cell(
        0, 10,  f"3. Muestras según eventos: {vigilancia.muestras_eventos}", 0, ln=1)

    # 4
    __margen(pdf)
    pdf.cell(
        0, 10,  f"4. Muestras según controles de foco: {vigilancia.muestras_control_foco}", 0, ln=1)

    # 5
    __margen(pdf)
    pdf.cell(
        0, 10,  f"5. Muestras acumuladas: {round(vigilancia.acumuladas_enviadas, 8)}", 0, ln=1)

    # 6
    __margen(pdf)
    pdf.cell(
        0, 10,  f"6. Resultados positivos que llegaron en el día: {vigilancia.resultados_positivos}", 0, ln=1)

    # 7
    __margen(pdf)
    pdf.cell(
        0, 10,  f"7. Resultados confirmatorios que llegaron en el día: {vigilancia.resultados_confirmatorios}", 0, ln=1)

    # 8
    __margen(pdf)
    pdf.cell(
        0, 10,  f"8. Resultados negativos que llegaron en el día: {vigilancia.resultados_negativos}", 0, ln=1)

    # 9
    __margen(pdf)
    pdf.cell(
        0, 10,  f"9. Resultados evolutivos que llegaron en el día: {vigilancia.resultados_evolutivos}", 0, ln=1)

    # 10
    __margen(pdf)
    pdf.cell(
        0, 10,  f"10. Resultados inhibidos que llegaron en el día: {vigilancia.resultados_inhibidos}", 0, ln=1)

    # 11
    __margen(pdf)
    pdf.cell(
        0, 10,  f"11. Tiempo promedio entre la toma de muestra y su salida hacia La Habana: {vigilancia.tiempo_promedio_salida}", 0, ln=1)

    # 12
    __margen(pdf)
    pdf.cell(
        0, 10,  f"12. Tiempo promedio entre la toma de muestra y el resultado: {vigilancia.tiempo_promedio_resultado}", 0, ln=1)

    # 13
    __margen(pdf)
    sum = db.origen_muestras.cantidad.sum()
    sum = db(db.origen_muestras.idvigilancia ==
             vigilancia.id).select(sum).first()[sum]

    pdf.cell(
        0, 8,  f"13. Origen de las muestras: {sum or 0}", 0, ln=3)

    __margen(pdf)
    for i in db(db.origen_muestras.idvigilancia == vigilancia.id).select():
        pdf.cell(0, 8,  f"- {i.idorigen.nombre}: {i.cantidad}", 0, ln=2)

    __fin_de_parrafo(pdf)

    # 14
    __margen(pdf)
    pdf.cell(
        0, 10,  f"14. Muestras pendientes con 2 días de retraso: {muestras_pendientes.con_2_dias}", 0, ln=1)

    # 15
    __margen(pdf)
    pdf.cell(
        0, 10,  f"15. Muestras pendientes con más de 3 días de retraso: {muestras_pendientes.con_mas_3_dias}", 0, ln=1)


def __inspeccion_sanitaria_estatal(pdf, idreporte):
    inspeccion_sanitaria_estatal = db(
        db.inspeccion_sanitaria_estatal.idreporte == idreporte).select().first()

    municipio_no_salieron = db(
        db.municipio_no_salieron.idinspeccion == inspeccion_sanitaria_estatal.id).select()

    municipio_no_medidas = db(
        db.municipio_no_medidas.idinspeccion == inspeccion_sanitaria_estatal.id).select()

    municipio_no_inspectores = db(
        db.municipio_no_inspectores.idinspeccion == inspeccion_sanitaria_estatal.id).select()

    municipio_mayor_notificaciones = db(
        db.municipio_mayor_notificaciones.idinspeccion == inspeccion_sanitaria_estatal.id).select()

    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, "- Inspección Sanitaria Estatal:", 0, ln=1)

    pdf.set_font('Arial', '', 12)

    # Inspección Sanitaria Estatal

    # 1
    __margen(pdf)
    pdf.cell(
        0, 10,  f"1. Centros visitados en el día: {inspeccion_sanitaria_estatal.centros_visitados}", 0, ln=1)

    # 2
    __margen(pdf)
    pdf.cell(
        0, 10,  f"2. Centros inspeccionados en el día: {inspeccion_sanitaria_estatal.centros_inspeccionados}", 0, ln=1)

    # 3
    __margen(pdf)
    pdf.cell(
        0, 10,  f"3. Inspectores que salieron: {inspeccion_sanitaria_estatal.inspectores_salieron}", 0, ln=1)

    # 4
    __margen(pdf)
    pdf.cell(
        0, 10,  f"4. Medidas impuestas: {inspeccion_sanitaria_estatal.medidas_impuestas}", 0, ln=1)

    # 5
    __margen(pdf)

    pdf.cell(
        0, 8,  f"5. Municipios que no salieron a inspeccionar: {0 if not municipio_no_salieron else ''}", 0, ln=3)

    __margen(pdf)
    for i in municipio_no_salieron:
        pdf.cell(0, 8,  f"- {i.idmunicipio.nombre}", 0, ln=2)

    __fin_de_parrafo(pdf)

    # 6
    __margen(pdf)

    pdf.cell(
        0, 8,  f"6. Municipios que no tomaron medidas: {0 if not municipio_no_medidas else ''}", 0, ln=3)

    __margen(pdf)
    for i in municipio_no_medidas:
        pdf.cell(0, 8,  f"- {i.idmunicipio.nombre}", 0, ln=2)

    __fin_de_parrafo(pdf)

    # 7
    __margen(pdf)

    pdf.cell(
        0, 8,  f"7. Municipios que no tienen inspectores: {0 if not municipio_no_inspectores else ''}", 0, ln=3)

    __margen(pdf)
    for i in municipio_no_inspectores:
        pdf.cell(0, 8,  f"- {i.idmunicipio.nombre}", 0, ln=2)

    __fin_de_parrafo(pdf)

    # 8
    __margen(pdf)

    pdf.cell(
        0, 8,  f"8. Municipios con mayor número de notificaciones: {0 if not municipio_mayor_notificaciones else ''}", 0, ln=3)

    __margen(pdf)
    for i in municipio_mayor_notificaciones:
        pdf.cell(0, 8,  f"- {i.idmunicipio.nombre}", 0, ln=2)

    __fin_de_parrafo(pdf)
