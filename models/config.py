# Configuraciones iniciales
import os


def __open_csv(url):
    with open(url, 'r', encoding='utf-8', newline='') as dumpfile:
        db.import_from_csv_file(dumpfile)


# Roles
if not db(db.auth_group.id > 0).select():
    db.auth_group.truncate()
    db.auth_group.insert(role="Administrador")
    db.auth_group.insert(role="Puesto de mando")


# Provincias, Municipios y Grupo de edades

if not db(db.provincia.id > 0).select():
    db.provincia.truncate()

    url = os.path.join(
        request.folder, "static/database_config/db_provincia.csv")

    __open_csv(url)


if not db(db.municipio.id > 0).select():
    db.municipio.truncate()

    url = os.path.join(
        request.folder, "static/database_config/db_municipio.csv")

    __open_csv(url)


if not db(db.grupo_edades.id > 0).select():
    db.grupo_edades.truncate()
    url = os.path.join(
        request.folder, "static/database_config/db_grupo_edades.csv")

    __open_csv(url)


# Crear usuario de administrador
if not db(db.auth_user.id > 0).select():
    db.auth_user.truncate()
    url = os.path.join(
        request.folder, "static/database_config/db_auth_user.csv")

    __open_csv(url)

    db.auth_membership.insert(user_id=1, group_id=1)
