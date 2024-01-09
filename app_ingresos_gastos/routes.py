from app_ingresos_gastos import app
from flask import render_template, request, redirect
import csv
from datetime import date

@app.route("/")
def index():
    datos = []
    #llamada al archivo csv
    fichero = open('data/movimientos.csv','r')
    #accediendo a cada registro de archivo y darle formato
    csvReader = csv.reader(fichero, delimiter=',', quotechar='"')
    for items in csvReader:
        datos.append(items)

    return render_template('index.html', data = datos, titulo= 'Lista')

@app.route('/new', methods= ['GET', 'POST']) 
def new():
    if request.method == 'POST':
        
        comprobar_error = validarFormulario(request.form)

        if comprobar_error:
            return render_template('new.html', titulo = 'Nuevo', tipoAccion = 'Registro', tipoBoton = 'Guardar', error = comprobar_error, dataForm = request.form)
        else:
            #acceder al archivo y configurar para la carga de nuevo registro
            mifichero = open('data/movimientos.csv', 'a', newline='')
            #llamar al metodo writer de escritura y configuramos formato
            lectura = csv.writer(mifichero, delimiter=',', quotechar='"')
            #registramos los datos recibidos en el archivo csv
            lectura.writerow([request.form['fecha'], request.form['concepto'], request.form['monto']])
            mifichero.close()

            return redirect('/')
    
    else:#Si es GET
        return render_template('new.html', titulo = 'Nuevo', tipoAccion = 'Registro', tipoBoton = 'Guardar', dataForm = {})

@app.route('/delete/<int:id>')
def delete(id):
    return f'El registro a eliminar es el de id: {id}'
    #return render_template('delete.html', titulo = 'Borrar')

@app.route('/update/<int:id>')
def update(id):
    return f'El registro a editar es el de id: {id}'
    #return render_template('update.html', titulo = 'Actualizar', tipoAccion = 'Actualización', tipoBoton = 'Editar', dataForm = {})

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