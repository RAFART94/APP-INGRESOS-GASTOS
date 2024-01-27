from app_ingresos_gastos import app, MOVIMIENTOS_FILE, LAST_ID_FILE
from flask import render_template, request, redirect
import csv
from datetime import date
from app_ingresos_gastos.models import *

@app.route("/")
def index():
    datos = select_all()
    return render_template('index.html', data = datos, titulo= 'Lista')

@app.route('/new', methods= ['GET', 'POST']) 
def new():
    if request.method == 'POST':
        
        comprobar_error = validarFormulario(request.form)

        if comprobar_error:
            return render_template('new.html', titulo = 'Nuevo', tipoAccion = 'Registro', tipoBoton = 'Guardar', error = comprobar_error, dataForm = request.form)
        else:

          insert(request.form)

          return redirect('/')  
    else:#Si es GET
        return render_template('new.html', titulo = 'Nuevo', tipoAccion = 'Registro', tipoBoton = 'Guardar', dataForm = {}, urlForm = '/new' )

@app.route('/delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    if request.method == 'GET':

        registro_buscado = select_by(id, '==')
        
        return render_template('delete.html', titulo = 'Borrar', data = registro_buscado)
    else:#post
        
        registros = select_by(id, '!=')
        delete_by(id, registros = registros)

        
        return redirect('/')


    
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        return f'se debe actualizar estos datos {request.form}'
    else:

        miFicheroUpdate = open(MOVIMIENTOS_FILE, 'r')
        lecturaUpdate = csv.reader(miFicheroUpdate, delimiter=',', quotechar='"')
        registro_buscado = dict()
        for item in lecturaUpdate:
            if item[0] == str(id):
                registro_buscado['id'] = item[0]#id
                registro_buscado['fecha'] = item[1]#fecha
                registro_buscado['concepto'] = item[2]#concepto
                registro_buscado['monto'] = item[3]#monto


        return render_template('update.html', titulo = 'Actualizar', tipoAccion = 'Actualización', tipoBoton = 'Editar', dataForm = registro_buscado, urlForm = f'/update/{id}')

def validarFormulario(datosFormularios):
    errores = []#Crear lista para guardar errores
    hoy = str(date.today())#Esto quita la fecha de hoy
    if datosFormularios['fecha'] > hoy:
        errores.append('La fecha no puede ser mayor a la actual')
    if datosFormularios['concepto'] == '':
        errores.append('El concepto no puede ir vacío')
    if datosFormularios['monto'] == '' or float(datosFormularios['monto']) == 0.0:
        errores.append('El monto debe ser distinto de 0 y de vacío')

    return errores