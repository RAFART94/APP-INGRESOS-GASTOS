from app_ingresos_gastos import app
from flask import render_template

@app.route("/")
def index():
    datos = [
        {'fecha': '01/01/2023',
        'concepto': 'Salario',
        'monto': '1500'},
        {'fecha': '05/01/2023',
        'concepto': 'Ropa',
        'monto': '-150'},
        {'fecha': '17/01/2023',
        'concepto': 'Supermercado',
        'monto': '-250'}  
    ]
    return render_template('index.html', data = datos)

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/update')
def update():
    return render_template('update.html')

@app.route('/delete')
def delete():
    return render_template('delete.html')