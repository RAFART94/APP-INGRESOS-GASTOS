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
    fichero.close()

    return render_template('index.html', data = datos, titulo= 'Lista')

@app.route('/new', methods= ['GET', 'POST']) 
def new():
    if request.method == 'POST':
        
        comprobar_error = validarFormulario(request.form)

        if comprobar_error:
            return render_template('new.html', titulo = 'Nuevo', tipoAccion = 'Registro', tipoBoton = 'Guardar', error = comprobar_error, dataForm = request.form)
        else:
            #####################Generar el nuevo ID#################
            lista_id = []
            last_id = ''
            new_id = 0
            ficheroId = open('data/last_id.csv','r')
            #accediendo a cada registro de archivo y darle formato
            csvReaderId = csv.reader(ficheroId, delimiter=',', quotechar='"')
            for items in csvReaderId:
                lista_id.append(items[0])
            ficheroId.close()
            last_id = lista_id[len(lista_id)-1]#El último valor del Id
            new_id = int(last_id)+1
            #########################################Guardar el Id generado en last_id################
            fichero_new_id = open('data/last_id.csv','w')
            fichero_new_id.write(str(new_id))
            fichero_new_id.close()

            ###################################
            #acceder al archivo y configurar para la carga de nuevo registro
            mifichero = open('data/movimientos.csv', 'a', newline='')
            #llamar al metodo writer de escritura y configuramos formato
            lectura = csv.writer(mifichero, delimiter=',', quotechar='"')
            #registramos los datos recibidos en el archivo csv
            lectura.writerow([new_id, request.form['fecha'], request.form['concepto'], request.form['monto']])
            mifichero.close()

            return redirect('/')
    
    else:#Si es GET
        return render_template('new.html', titulo = 'Nuevo', tipoAccion = 'Registro', tipoBoton = 'Guardar', dataForm = {})

@app.route('/delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    if request.method == 'GET':
        miFicheroDelete = open('data/movimientos.csv', 'r')
        lecturaDelete = csv.reader(miFicheroDelete, delimiter=',', quotechar='"')
        registro_buscado = []
        for item in lecturaDelete:
            if item[0] == str(id):
                registro_buscado = item
        
        return render_template('delete.html', titulo = 'Borrar', data = registro_buscado)
    else:#post
        return f'Esto debería eliminar el registro con el Id {id}'
    
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