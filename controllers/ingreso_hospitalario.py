@auth.requires_login()
def administrar():
    datos=db(db.ingreso_hospitalario.id>0).select()
    # return dict(ingreso_hospitalario=ingreso_hospitalario)
    return locals()