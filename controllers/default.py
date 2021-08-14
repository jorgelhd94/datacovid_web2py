# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
@auth.requires_login()
def index():
    import datetime

    confirmados = 0
    activos = 0
    eventos = 0
    cf = 0

    provincia = db((db.usuario_provincia.idusuario ==
                    auth.user.id) & (db.usuario_provincia.idprovincia == db.provincia.id)).select(db.provincia.ALL).first()

    if auth.has_membership("Administrador"):
        reportes = db(db.reporte.fecha ==
                      datetime.datetime.now().date()).select(db.reporte.ALL)

        for i in reportes:
            confirmados += db(db.confirmados.idreporte ==
                              i.id).select().first().total
            activos += db(db.activos.idreporte ==
                          i.id).select().first().total

        eventos = db(db.eventos.estado == "Abierto").count()
        cf = db(db.control_foco.estado == "Abierto").count()

        reportes_list = db(db.reporte.id > 0).select(orderby=db.reporte.fecha)

    else:
        reporte = db((db.reporte.fecha == datetime.datetime.now().date()) & (db.reporte.idprovincia == provincia.id)).select(
            db.reporte.ALL).first()

        if reporte:
            confirmados = db(db.confirmados.idreporte ==
                             reporte.id).select().first().total

            activos = db(db.activos.idreporte ==
                         reporte.id).select().first().total

            eventos = db((db.eventos.estado == "Abierto") & (db.eventos.idmunicipio ==
                                                             db.municipio.id) & (db.municipio.idprovincia == provincia.id)).count()
            cf = db((db.control_foco.estado == "Abierto") & (db.control_foco.idmunicipio ==
                                                             db.municipio.id) & (db.municipio.idprovincia == provincia.id)).count()

        reportes_list = db(db.reporte.idprovincia == provincia.id).select(
            orderby=db.reporte.fecha)

    return locals()

# ---- Embedded wiki (example) ----


def wiki():
    auth.wikimenu()  # add the wiki to the menu
    return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
