from app_ingresos_gastos import app, MOVIMIENTOS_FILE, LAST_ID_FILE
from flask import render_template, request, redirect
import csv
from datetime import date

@app.route("/")
def index():
    datos = []
    #llamada al archivo csv
    fichero = open(MOVIMIENTOS_FILE,'r')
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
            ficheroId = open(LAST_ID_FILE,'r')
            #accediendo a cada registro de archivo y darle formato
            csvReaderId = csv.reader(ficheroId, delimiter=',', quotechar='"')
            for items in csvReaderId:
                lista_id.append(items[0])
            ficheroId.close()
            last_id = lista_id[len(lista_id)-1]#El último valor del Id
            new_id = int(last_id)+1
            #########################################Guardar el Id generado en last_id################
            fichero_new_id = open(LAST_ID_FILE,'w')
            fichero_new_id.write(str(new_id))
            fichero_new_id.close()

            ###################################
            #acceder al archivo y configurar para la carga de nuevo registro
            mifichero = open(MOVIMIENTOS_FILE, 'a', newline='')
            #llamar al metodo writer de escritura y configuramos formato
            lectura = csv.writer(mifichero, delimiter=',', quotechar='"')
            #registramos los datos recibidos en el archivo csv
            lectura.writerow([new_id, request.form['fecha'], request.form['concepto'], request.form['monto']])
            mifichero.close()

            return redirect('/')
    
    else:#Si es GET
        return render_template('new.html', titulo = 'Nuevo', tipoAccion = 'Registro', tipoBoton = 'Guardar', dataForm = {}, urlForm = '/new' )

@app.route('/delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    if request.method == 'GET':
        miFicheroDelete = open(MOVIMIENTOS_FILE, 'r')
        lecturaDelete = csv.reader(miFicheroDelete, delimiter=',', quotechar='"')
        registro_buscado = []
        for item in lecturaDelete:
            if item[0] == str(id):
                registro_buscado = item
        
        return render_template('delete.html', titulo = 'Borrar', data = registro_buscado)
    else:#post
        #####################Lectura de archivo para quitar todos los datos excepto el del id dado#########################
        fichero_lectura = open(MOVIMIENTOS_FILE, 'r')
        csv_reader = csv.reader(fichero_lectura, delimiter=',', quotechar='"')
        registros = []
        for item in csv_reader:
            if item[0] != str(id):#filtrando el id dado
                registros.append(item)
        fichero_lectura.close()
        ###################################guardar el registro obtenido################################
        fichero_guardar = open(MOVIMIENTOS_FILE, 'w', newline='')
        csv_writer = csv.writer(fichero_guardar, delimiter=',', quotechar='"')
        #registramos los datos recibidos en el archivo csv
        for datos in registros:
            csv_writer.writerow(datos)

        fichero_guardar.close()

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