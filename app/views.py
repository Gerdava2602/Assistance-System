from .models import *
from flask import render_template,request
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi
from flask_babel import lazy_gettext 
from . import appbuilder, db
from flask_appbuilder.security.registerviews import RegisterUserDBView
from flask_appbuilder.security.sqla.manager import SecurityManager
from flask_babel import lazy_gettext 
from app import app
from flask import g
from flask_appbuilder import BaseView,IndexView, expose
import fdb
import datetime
import qrcode
from PIL import Image

class DepartamentoView(ModelView):
    datamodel = SQLAInterface(Departamento)
    add_columns=['ID_Departamento','nombre']

class DocenteView(ModelView):
    datamodel = SQLAInterface(Docente)
    add_columns=['ID_Docente','nombre','apellido','email', 'Departamento']

class AsignaturaView(ModelView):
    datamodel = SQLAInterface(Asignatura)
    add_columns=['ID_Asignatura','nombre','Departamento']

class ProgramaView(ModelView):
    datamodel = SQLAInterface(Programa)
    add_columns=['ID_Programa','nombre']

class PlanView(ModelView):
    datamodel = SQLAInterface(Plan)
    add_columns=['ID_Plan','nombre','semestre','Programa']

class ContieneView(ModelView):
    datamodel = SQLAInterface(Contiene)
    add_columns=['Asignatura','Plan']

class EstudianteView(ModelView):
    datamodel = SQLAInterface(Estudiante)
    add_columns=['ID_Estudiante','nombre','apellido','email']

class PeriodoView(ModelView):
    datamodel = SQLAInterface(Periodo)
    add_columns=['ID_Periodo','descripcion']

class MatriculaView(ModelView):
    datamodel = SQLAInterface(Matricula)
    add_columns=['Estudiante','Periodo','Plan']

class CursoView(ModelView):
    datamodel = SQLAInterface(Curso)
    add_columns=['ID_Curso','nombre','Docente','Asignatura']

class AlumnoView(ModelView):
    datamodel = SQLAInterface(Alumno)
    add_columns=['Estudiante','Periodo','Curso']

class SalonView(ModelView):
    datamodel = SQLAInterface(Salon)
    add_columns=['ID_Salon','modalidad']

class SesionView(ModelView):
    datamodel = SQLAInterface(Sesion)
    add_columns=['ID_Sesion','Curso','Salon','Horario','activada']

class HorarioView(ModelView):
    datamodel = SQLAInterface(Horario)
    add_columns=['ID_Horario','Hora_Inicio','Hora_Fin','fecha']
    

appbuilder.add_view(
    DepartamentoView, "Departamentos", icon="fa-folder-open-o", category="Universidad"
)

appbuilder.add_view(
    ProgramaView, "Programas académicos", icon="fa-folder-open-o", category="Universidad"
)

appbuilder.add_view(
    DocenteView, "Docentes", icon="fa-folder-open-o", category="Universidad"
)
appbuilder.add_view(
    EstudianteView, "Estudiantes", icon="fa-folder-open-o", category="Universidad"
)

appbuilder.add_view(
    AsignaturaView, "Asignaturas", icon="fa-folder-open-o", category="Universidad"
)
appbuilder.add_view(
    PlanView, "Planes", icon="fa-folder-open-o", category="Universidad"
)
appbuilder.add_view(
    ContieneView, "Contiene", icon="fa-folder-open-o", category="Universidad"
)
appbuilder.add_view(
    PeriodoView, "Periodos", icon="fa-folder-open-o", category="Universidad"
)
appbuilder.add_view(
    MatriculaView, "Matriculas", icon="fa-folder-open-o", category="Universidad"
)
appbuilder.add_view(
    CursoView, "Cursos", icon="fa-folder-open-o", category="Universidad"
)
appbuilder.add_view(
    AlumnoView, "Alumnos", icon="fa-folder-open-o", category="Universidad"
)
appbuilder.add_view(
    SalonView, "Salones", icon="fa-folder-open-o", category="Universidad"
)
appbuilder.add_view(
    SesionView, "Sesiones", icon="fa-folder-open-o", category="Universidad"
)
appbuilder.add_view(
    HorarioView, "Horarios", icon="fa-folder-open-o", category="Universidad"
)

@app.route("/curso")
def curso():
    #SQL STATEMENT
    con = fdb.connect(database='C:/Users/germa/Desktop/Universidad/2021-3/Bases de datos/final/project/DB.FDB', user='sysdba', password='masterkey')
    cur = con.cursor()
    cur.execute(f'SELECT "Horario"."Hora_Inicio","Horario"."Hora_Fin","Horario".FECHA,"ID_Sesion",ACTIVADA FROM "Curso" JOIN "Sesion" ON "Curso"."ID_Curso" = "Sesion"."ID_Curso" JOIN "Horario" ON "Horario"."ID_Horario" = "Sesion"."ID_Horario" WHERE "Curso"."ID_Curso" = \'{request.args.get("id")}\' AND CURRENT_DATE<="Horario"."Hora_Fin"')
    #User Role
    user = g.user
    roles = [str(i) for i in user.roles]

    return render_template("curso.html", id = request.args.get("id"), roles = roles,sesiones=cur.fetchall(),base_template=appbuilder.base_template, appbuilder=appbuilder)

@app.route("/activate")
def activate():
    con = fdb.connect(database='C:/Users/germa/Desktop/Universidad/2021-3/Bases de datos/final/project/DB.FDB', user='sysdba', password='masterkey')
    cur = con.cursor()
    #Update info
    cur.execute(f'UPDATE "Sesion" SET ACTIVADA = 1 WHERE "ID_Sesion" = {request.args.get("id")};')

    #Ask for all the sessions
    cur.execute(f'SELECT "Horario"."Hora_Inicio","Horario"."Hora_Fin","Horario".FECHA,"ID_Sesion",ACTIVADA FROM "Curso" JOIN "Sesion" ON "Curso"."ID_Curso" = "Sesion"."ID_Curso" JOIN "Horario" ON "Horario"."ID_Horario" = "Sesion"."ID_Horario" WHERE "Curso"."ID_Curso" = \'{request.args.get("id")}\' AND CURRENT_DATE<="Horario"."Hora_Fin"')
    user = g.user
    roles = [str(i) for i in user.roles]
    return render_template("curso.html", id = request.args.get("id_curso"), roles = roles,sesiones=cur.fetchall(),base_template=appbuilder.base_template, appbuilder=appbuilder)
    