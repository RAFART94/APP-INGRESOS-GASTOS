# Aplicación de introducción a Flask

Programa hecho con python con el framewor flask, Hello word

## Instalación

-Crear un entorno en python y ejecutar el comando

```
pip install - requirements.txt
```
-La librería ultilizada en Flask https://flask-wtf.readthedocs.io/en/1.2.x/

## Ejecución del programa
-Inicializar parametros para servidor de Flask
-en mac:

``export FLASK_APP = main.py``

-en windows

``set FLASK_APP=main.py``

### Comando para ejecutar el servidor

``flask --app main run``

### Comando para ejecutar el servidor en otro puerto diferente (por default siempre es el 5000)

``flask --app main run -p 5002``

### Comando para ejecutar el servidor en modo debug (realizar cambios en tiempo real)

``flask --app main --debug run``