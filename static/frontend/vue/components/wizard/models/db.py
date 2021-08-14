# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
# Reporte Diario
# -------------------------------------------------------------------------

db.define_table("reporte",                
                Field("fecha", "date"),
                Field("id_usuario", "integer"),
                )

# -------------------------------------------------------------------------
# Reporte del dia
# -------------------------------------------------------------------------

db.define_table("confirmados",                
                Field("total", "integer"),
                Field("sin_fid", "integer"),
                Field("sintomaticos", "integer"),
                Field("asintomaticos", "integer"),
                Field("cubanos", "integer"),
                Field("extranjeros", "integer"),
                Field("masculinos", "integer"),
                Field("femeninos", "integer"),
                Field("contactos", "integer"),
                Field("promedio_contactos_por_caso", "integer"),
                Field("casos_aislados", "integer"),
                Field("casos_comunidad", "integer"),
                Field("casos_vigilancia_aps", "integer"),
                Field("idreporte", "reference reporte"),
                )
                

db.define_table("provincia",                
                Field("nombre", "text"),
                )

db.define_table("municipio",                
                Field("nombre", "text"),
                Field("idprovincia", "reference provincia"),
                )

db.define_table("municipio_confirmados",              
                Field("cantidad", "integer"),
                Field("idmunicipio", "reference municipio"),
                Field("idconfirmados", "reference confirmados"),
                )

db.define_table("grupo_edades",                
                Field("grupo", "text"),
                )

db.define_table("edades_confirmados",                
                Field("cantidad", "integer"),
                Field("idgrupo_edades", "reference grupo_edades"),
                Field("idconfirmados", "reference confirmados"),
                )

# Activos
db.define_table("activos",                
                Field("total", "integer"),
                Field("idreporte", "reference reporte"),
                )

db.define_table("ubicacion",                
                Field("nombre", "text"),
                Field("idmunicipio", "reference municipio"),
                )

db.define_table("ubicacion_activos",                
                Field("cantidad", "integer"),
                Field("idactivos", "reference activos"),
                Field("idubicacion", "reference ubicacion"),
                )



# -------------------------------------------------------------------------
# Fallecidos, casos críticos y casos graves
# -------------------------------------------------------------------------

db.define_table("fallecidos_criticos_graves",
                Field("covid_fallecidos", "integer"),
                Field("covid_criticos", "integer"),
                Field("covid_graves", "integer"),
                Field("ira_graves", "integer"),
                Field("ira_graves_pendiente_pcr", "integer"),
                Field("altas_clinicas_covid", "integer"),
                Field("altas_sospechosos", "integer"),
                Field("altas_contactos", "integer"),
                Field("idreporte", "reference reporte"),
                )


db.define_table("sospechosos",                
                Field("ingresados", "integer"),
                Field("comunidad", "integer"),
                Field("iden_hospital", "integer"),
                Field("iden_policlinico", "integer"),
                Field("iden_consultorio", "integer"),
                Field("iden_pesquisa", "integer"),
                Field("idreporte", "reference reporte"),
                )


db.define_table("casos_ira",                
                Field("ingresados", "integer"),
                Field("comunidad", "integer"),
                Field("iden_hospital", "integer"),
                Field("iden_policlinico", "integer"),
                Field("iden_consultorio", "integer"),
                Field("iden_pesquisa", "integer"),
                Field("idreporte", "reference reporte"),
                )

db.define_table("atencion_ira",                
                Field("repor_hospital", "integer"),
                Field("repor_policlinico", "integer"),
                Field("repor_consultorio", "integer"),
                Field("idreporte", "reference reporte"),
                )


# -------------------------------------------------------------------------
# Pesquisa Activa
# -------------------------------------------------------------------------

db.define_table("pesquisa_activa",                
                Field("porciento_pesquisada", "integer"),
                Field("a_pesquisar", "integer"),
                Field("presuntar_ira_identificadas", "integer"),
                Field("presuntar_ira_atendidas", "integer"),
                Field("porciento_001", "integer"),
                Field("idreporte", "reference reporte"),
                )


# -------------------------------------------------------------------------
# Eventos y Control de Foco en el territorio
# -------------------------------------------------------------------------

db.define_table("eventos",                
                Field("fecha_ultimo_caso", "date"),
                Field("fecha_cierre", "date"),
                Field("tipo_evento", "text"),
                )

db.define_table("evento_diario",                
                Field("casos_confirmados", "integer"),
                Field("ideventos", "reference eventos"),
                Field("idreporte", "reference reporte"),
                )

db.define_table("evento_ubicacion",                
                Field("idubicacion", "reference ubicacion"),
                Field("ideventos", "reference eventos"),
                )

db.define_table("control_foco",                
                Field("fecha_ultimo_caso", "date"),
                Field("fecha_cierre", "date"),
                )

db.define_table("control_foco_diario",                
                Field("casos_confirmados", "integer"),
                Field("idcontrol_foco", "reference control_foco"),
                Field("idreporte", "reference reporte"),
                )

db.define_table("control_foco_ubicacion",                
                Field("idubicacion", "reference ubicacion"),
                Field("idcontrol_foco", "reference control_foco"),
                )


# -------------------------------------------------------------------------
# Movimiento Hospitalario
# -------------------------------------------------------------------------

db.define_table("movimiento_hospitalario",                
                Field("ingresados", "integer"),
                Field("confirmados_ingresados", "integer"),
                Field("sospechosos_ingresados", "integer"),
                Field("contactos_ingresados", "integer"),
                Field("disponibilidad_camas_ingreso", "integer"),
                Field("disponibilidad_camas_graves", "integer"),
                Field("disponibilidad_camas_sospechosos", "integer"),
                Field("disponibilidad_camas_contactos", "integer"),
                Field("idreporte", "reference reporte"),
                )
                
# -------------------------------------------------------------------------
# Vigilancia Microbiologica
# -------------------------------------------------------------------------

db.define_table("vigilancia",                
                Field("muestras_tomadas", "integer"),
                Field("muestras_enviadas", "integer"),
                Field("muestras_eventos", "integer"),
                Field("muestras_control_foco", "integer"),
                Field("acumuladas_enviadas", "integer"),
                Field("resultados_positivos", "integer"),
                Field("resultados_confirmatorios", "integer"),
                Field("resultados_negativos", "integer"),
                Field("resultados_evolutivos", "integer"),
                Field("resultados_inhibidos", "integer"),
                Field("idreporte", "reference reporte"),
                )

db.define_table("origen",                
                Field("nombre", "text"),
                )

db.define_table("origen_muestras",                
                Field("cantidad", "integer"),
                Field("idvigilancia", "reference vigilancia"),
                Field("idorigen", "reference origen"),
                )

db.define_table("muestras_pendientes",                
                Field("con_2_dias", "integer"),
                Field("con_mas_3_dias", "integer"),
                Field("tiempo_promedio_salida", "integer"),
                Field("tiempo_promedio_resultado", "integer"),
                Field("idreporte", "reference reporte"),
                )

# -------------------------------------------------------------------------
# Inspección Sanitaria Estatal
# -------------------------------------------------------------------------

db.define_table("inspeccion_sanitaria_estatal",                
                Field("centros_visitados", "integer"),
                Field("centros_inspeccionados", "integer"),
                Field("inspectores_salieron", "integer"),
                Field("medidas_impuestas", "integer"),
                Field("idreporte", "reference reporte"),
                )

db.define_table("municipio_no_salieron",                
                Field("cantidad", "integer"),
                Field("idinspeccion", "reference inspeccion_sanitaria_estatal"),
                Field("idmunicipio", "reference municipio"),
                )

db.define_table("municipio_no_medidas",                
                Field("cantidad", "integer"),
                Field("idinspeccion", "reference inspeccion_sanitaria_estatal"),
                Field("idmunicipio", "reference municipio"),
                )

db.define_table("municipio_no_inspectores",                
                Field("cantidad", "integer"),
                Field("idinspeccion", "reference inspeccion_sanitaria_estatal"),
                Field("idmunicipio", "reference municipio"),
                )

db.define_table("municipio_mayor_notificaciones",                
                Field("cantidad", "integer"),
                Field("idinspeccion", "reference inspeccion_sanitaria_estatal"),
                Field("idmunicipio", "reference municipio"),
                )


# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
