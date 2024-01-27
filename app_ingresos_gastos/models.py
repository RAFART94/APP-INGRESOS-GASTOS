from app_ingresos_gastos import MOVIMIENTOS_FILE, LAST_ID_FILE
import csv

def select_all():
    datos = []
    #llamada al archivo csv
    fichero = open(MOVIMIENTOS_FILE,'r')
    #accediendo a cada registro de archivo y darle formato
    csvReader = csv.reader(fichero, delimiter=',', quotechar='"')
    for items in csvReader:
        datos.append(items)
    fichero.close()
    
    return datos

def select_by(id, condicion):
    miFicheroDelete = open(MOVIMIENTOS_FILE, 'r')
    lecturaDelete = csv.reader(miFicheroDelete, delimiter=',', quotechar='"')
    registro_buscado = []
    for item in lecturaDelete:
        if condicion == '==':
            if item[0] == str(id):
                registro_buscado = item
        else:
            if item[0] != str(id):#filtrando el id dado
                registro_buscado.append(item)
    
    miFicheroDelete.close()
    
    return registro_buscado

def delete_by(id, registros):
    fichero_guardar = open(MOVIMIENTOS_FILE, 'w', newline='')
    csv_writer = csv.writer(fichero_guardar, delimiter=',', quotechar='"')
    #registramos los datos recibidos en el archivo csv
    for datos in registros:
        csv_writer.writerow(datos)

    fichero_guardar.close()

def insert(requestForm):
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
    lectura.writerow([new_id, requestForm['fecha'], requestForm['concepto'], requestForm['monto']])
    mifichero.close()