import logging

from flask import Flask
from flask.templating import render_template
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder import BaseView,IndexView, expose
from flask import Flask, g, redirect, url_for
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
            if 'Estudiante' in roles:
                return render_template("cursos.html", rol='Estudiante', base_template=appbuilder.base_template, appbuilder=appbuilder)
            elif 'Docente' in roles:
                return render_template("cursos.html", rol='Docente', base_template=appbuilder.base_template, appbuilder=appbuilder)
            elif 'Admin' in roles:
                return render_template("cursos.html", rol='Admin', base_template=appbuilder.base_template, appbuilder=appbuilder)

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

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
