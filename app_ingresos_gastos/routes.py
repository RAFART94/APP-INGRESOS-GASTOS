from app_ingresos_gastos import app
from flask import render_template, request, redirect
import csv

@app.route("/")
def index():
    datos = []
    #llamada al archivo csv
    fichero = open('data/movimiento.csv', 'r')
    #accediendo a cada registro de archivo y darle formato
    csvReader = csv.reader(fichero, delimiter=',', quotechar='"')
    for items in csvReader:
        datos.append(items)

    return render_template('index.html', data = datos, titulo = 'Lista')

@app.route('/new', methods = ['GET', 'POST'])
def new():
    if request.method == 'POST':
        #return 'esto debería registrase' + str(request.form)

        #acceder al archivo y configurar para la carga de nuevo registro
        mifichero = open('data/movimientos.csv', 'a', newline = '')
        #llamar al metodo writer de escritura y configuramos formato
        lectura = csv.writer(mifichero, delimiter=',', quotechar='"')
        #registramos los datos recibidos en el archivo csv
        lectura.writerow([request.form['fecha'], request.form['concepto'], request.form['moto']])
        mifichero.close()

        return redirect('/')
    
    else:
        return render_template('new.html', titulo = 'Nuevo', tipoAccion = 'Registro', tipoBoton = 'Guardar')

@app.route('/update')
def update():
    return render_template('update.html', titulo = 'Actualizar', tipoAccion = 'Actualización', tipoBoton = 'Editar')

@app.route('/delete')
def delete():
    return render_template('delete.html', titulo = 'Borrar')