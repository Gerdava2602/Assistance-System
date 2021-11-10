from flask_appbuilder import Model
from sqlalchemy import Column, Integer,Date ,String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import Sequence
from sqlalchemy.sql.sqltypes import Date

class Departamento(Model):
    __tablename__ = 'Departamento'
    nombre = Column(String(60), nullable=False)
    ID_Departamento = Column(Integer, primary_key=True, nullable=False)

    def __str__(self):
        return self.nombre

class Docente(Model):
    __tablename__ = 'Docente'
    nombre = Column(String(60), nullable=False)
    apellido = Column(String(60), nullable=False)
    email = Column(String(60),nullable=False)
    ID_Docente = Column(Integer, primary_key=True, nullable=False)
    ID_Departamento = Column(Integer, ForeignKey("Departamento.ID_Departamento"), nullable=False)
    Departamento = relationship("Departamento")

    def __str__(self):
        return self.nombre

class Asignatura(Model):
    __tablename__ = 'Asignatura'
    nombre = Column(String(60), nullable=False)
    ID_Departamento = Column(Integer, ForeignKey("Departamento.ID_Departamento"), nullable=False)
    Departamento = relationship("Departamento")
    ID_Asignatura = Column(Integer, primary_key=True, nullable=False)

    def __str__(self):
        return self.nombre

class Programa(Model):
    __tablename__ = 'Programa'
    nombre = Column(String(60), nullable=False)
    ID_Programa = Column(Integer, primary_key=True, nullable=False)

    def __str__(self):
        return self.nombre

class Plan(Model):
    __tablename__ = 'Plan'
    nombre = Column(String(60), nullable=False)
    ID_Plan = Column(Integer, primary_key=True, nullable=False)
    semestre = Column(Integer,nullable=False)
    ID_Programa = Column(Integer, ForeignKey("Programa.ID_Programa"), nullable=False)
    Programa = relationship("Programa")
    
    def __str__(self):
        return self.nombre

class Contiene(Model):
    __tablename__ = 'Contiene'
    ID_Asignatura = Column(Integer, ForeignKey("Asignatura.ID_Asignatura"), nullable=False, primary_key=True)
    Asignatura = relationship("Asignatura")
    ID_Plan = Column(Integer, ForeignKey("Plan.ID_Plan"), nullable=False, primary_key=True)
    Plan = relationship("Plan")

class Estudiante(Model):
    __tablename__ = 'Estudiante'
    nombre = Column(String(60), nullable=False)
    apellido = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    ID_Estudiante = Column(Integer,primary_key=True,nullable=False)

    def __str__(self):
        return self.nombre

class Periodo(Model):
    __tablename__ = 'Periodo'
    descripcion = Column(String(500), nullable=False)
    ID_Periodo = Column(String(8), nullable=False, primary_key=True)

    def __str__(self):
        return self.ID_Periodo

#
class Matricula(Model):
    __tablename__ = 'Matricula'
    ID_Estudiante = Column(Integer, ForeignKey("Estudiante.ID_Estudiante"), nullable=False, primary_key=True)
    Estudiante = relationship("Estudiante")
    ID_Periodo = Column(String(8), ForeignKey("Periodo.ID_Periodo"), nullable=False, primary_key=True)
    Periodo = relationship("Periodo")
    ID_Plan = Column(Integer, ForeignKey("Plan.ID_Plan"), nullable=False, primary_key=True)
    Plan = relationship("Plan")

#
class Curso(Model):
    __tablename__ = 'Curso'
    nombre = Column(String(60), nullable=False)
    ID_Docente = Column(Integer, ForeignKey("Docente.ID_Docente"), nullable=False)
    Docente = relationship("Docente")
    ID_Asignatura = Column(Integer, ForeignKey("Asignatura.ID_Asignatura"), nullable=False)
    Asignatura = relationship("Asignatura")
    ID_Curso = Column(Integer, nullable=False, primary_key=True)

    def __str__(self):
        return self.nombre

#
class Alumno(Model):
    __tablename__ = 'Alumno'
    ID_Estudiante = Column(Integer, ForeignKey("Estudiante.ID_Estudiante"), nullable=False, primary_key=True)
    Estudiante = relationship("Estudiante")
    ID_Periodo = Column(String(8), ForeignKey("Periodo.ID_Periodo"), nullable=False, primary_key=True)
    Periodo = relationship("Periodo")
    ID_Curso = Column(Integer, ForeignKey("Curso.ID_Curso"), nullable=False, primary_key=True)
    Curso = relationship("Curso")

class Salon(Model):
    __tablename__ = 'Salon'
    modalidad = Column(String(60), nullable=False)
    ID_Salon = Column(Integer, primary_key=True, nullable=False)

#
class Sesion(Model):
    __tablename__ = 'Sesion'
    ID_Sesion = Column(Integer,primary_key=True,nullable=True)
    ID_Curso = Column(Integer, ForeignKey("Curso.ID_Curso"), nullable=False)
    Curso = relationship("Curso")
    ID_Salon = Column(Integer, ForeignKey("Salon.ID_Salon"), nullable=False)
    Salon = relationship("Salon")

#
class Horario(Model):
    __tablename__ = 'Horario'
    ID_Sesion = Column(Integer, ForeignKey("Sesion.ID_Sesion"), nullable=False, primary_key=True)
    Sesion = relationship("Sesion")
    Hora_Inicio = Column(DateTime, nullable=False)
    Hora_Fin = Column(DateTime, nullable=False)
    fecha = Column(Date, nullable=False)

class Asistencia(Model):
    __tablename__ = 'Asistencia'
    ID_Sesion = Column(Integer, ForeignKey("Sesion.ID_Sesion"), nullable=False, primary_key=True)
    Sesion = relationship("Sesion")
    ID_Estudiante = Column(Integer, ForeignKey("Estudiante.ID_Estudiante"), nullable=False)
    Estudiante = relationship("Estudiante")
    estado = Column(String(60), nullable=False)
