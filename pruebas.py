# lectura de archivos
'''
with open('data/movimientos.csv','r') as resultado:
    leer = resultado.read()
    print(type(leer))
'''
#otro ejemplo de lectura de archivos csv
"""
resultado = open('data/movimientos.csv','r')
lectura = resultado.readlines()
print(lectura)   
"""
"""
import csv

midato= []
mifichero = open('data/movimientos.csv','r')
lectura = csv.reader(mifichero,delimiter=",",quotechar='"')
for items in lectura:
    #print(type(items))
    midato.append(items)

print("mi lista:",midato[0][1])    
"""
#ejemplo para registrar datos en csv
'''
import csv

mifichero = open('data/movimientos.csv','a',newline='')
lectura = csv.writer(mifichero,delimiter=',', quotechar='"')
lectura.writerow(['24/04/2024','roscon de reyes','-40'])

mifichero.close()
'''

from datetime import date

print(type(str(date.today())))
print(date.today())