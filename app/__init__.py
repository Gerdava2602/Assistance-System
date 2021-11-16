import logging

from flask import Flask
from flask.templating import render_template
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder import BaseView,IndexView, expose
from flask import Flask, g, request
import fdb
import os
import threading
import time
import datetime
"""
 Logging configuration
"""


class newIndexView(IndexView):
    route_base = "/"

    @expose('/')
    def index(self):
        user = g.user
        if user.is_anonymous:
             return render_template("welcome.html", base_template=appbuilder.base_template, appbuilder=appbuilder)
        else:
            roles = [str(i) for i in user.roles]
            con = fdb.connect(database='C:/Users/germa/Desktop/Universidad/2021-3/Bases de datos/final/project/DB.FDB', user='sysdba', password='masterkey')
            cur = con.cursor()
            cur.execute(f'SELECT "ID_Periodo" FROM "Periodo"')
            periodos=[i[0] for i in cur.fetchall()]

            if 'Estudiante' in roles:
                cur.execute(f'SELECT "Curso"."ID_Curso","Curso".NOMBRE FROM "Estudiante" JOIN "Alumno" ON "Estudiante"."ID_Estudiante" = "Alumno"."ID_Estudiante" JOIN "Curso" ON "Curso"."ID_Curso" = "Alumno"."ID_Curso" WHERE "Estudiante".EMAIL = \'{str(user.email)}\'')
                if request.args.get("periodo","") != "":
                    cur.execute(f'SELECT "Curso"."ID_Curso","Curso".NOMBRE FROM "Estudiante" JOIN "Alumno" ON "Estudiante"."ID_Estudiante" = "Alumno"."ID_Estudiante" JOIN "Curso" ON "Curso"."ID_Curso" = "Alumno"."ID_Curso" WHERE "Estudiante".EMAIL = \'{str(user.email)}\' AND "Curso"."ID_Periodo" = \'{str(request.args.get("periodo",""))}\'')
                return render_template("cursos.html", rol='Estudiante',cursos=cur.fetchall(), periodos= periodos,base_template=appbuilder.base_template, appbuilder=appbuilder)
            elif 'Docente' in roles:
                cur.execute(f'SELECT "Curso"."ID_Curso", "Curso".NOMBRE FROM "Docente" JOIN "Curso" ON "Curso"."ID_Docente" = "Docente"."ID_Docente" WHERE "Docente".EMAIL = \'{str(user.email)}\';')
                if request.args.get("periodo","") != "":
                    cur.execute(f'SELECT "Curso"."ID_Curso", "Curso".NOMBRE FROM "Docente" JOIN "Curso" ON "Curso"."ID_Docente" = "Docente"."ID_Docente" WHERE "Docente".EMAIL = \'{str(user.email)}\' AND "Curso"."ID_Periodo" = \'{str(request.args.get("periodo",""))}\';')
                return render_template("cursos.html", rol='Docente',cursos=cur.fetchall(),periodos=periodos ,base_template=appbuilder.base_template, appbuilder=appbuilder)
            elif 'Admin' in roles:
                return render_template("cursos.html", rol='Admin', periodos = periodos,base_template=appbuilder.base_template, appbuilder=appbuilder)

#Thread to check sessions
def checker_thread():
    while True:
        #Connects to the database
        con = fdb.connect(database='C:/Users/germa/Desktop/Universidad/2021-3/Bases de datos/final/project/DB.FDB', user='sysdba', password='masterkey')
        cur = con.cursor()

        #Gets the sessions of the date for each course
        cur.execute('SELECT "Curso"."ID_Curso","Sesion"."ID_Sesion","Horario"."Hora_Inicio","Horario"."Hora_Fin","Horario".FECHA,"ID_Sesion",ACTIVADA,"Sesion"."CODIGO_BASE","Sesion"."HORA_ACTIVACION" FROM "Curso" JOIN "Sesion" ON "Curso"."ID_Curso" = "Sesion"."ID_Curso" JOIN "Horario" ON "Horario"."ID_Horario" = "Sesion"."ID_Horario" WHERE CURRENT_DATE<="Horario"."Hora_Fin"')
        sessions = cur.fetchall()
        for session in sessions:
            #Check if the session has an 'Asistencia'
            if session[-3] == 1:
                if (datetime.datetime.now() - session[-1]) > datetime.timedelta(minutes=20): 
                    cur.execute(f'SELECT "Estudiante"."ID_Estudiante" FROM "Estudiante" JOIN "Alumno" ON "Estudiante"."ID_Estudiante" = "Alumno"."ID_Estudiante" JOIN "Curso" ON "Curso"."ID_Curso" = "Alumno"."ID_Curso" WHERE "Curso"."ID_Curso" = {session[0]}')
                    estudiantes = cur.fetchall()
                    cur.execute(f'SELECT "ID_Estudiante" FROM "Asistencia" WHERE "ID_Sesion" = {session[1]}')
                    already = cur.fetchall()
                    for estudiante in estudiantes:
                        if not estudiante[0] in [i[0] for i in already]:
                            cur.execute(f'INSERT INTO "Asistencia" VALUES ({session[1]},{estudiante[0]},\'Ausencia\')')
                            con.commit()
        time.sleep(5)

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

checker = threading.Thread(target=checker_thread)
checker.daemon = True
checker.start()
app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session,indexview=newIndexView)


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

from . import views
