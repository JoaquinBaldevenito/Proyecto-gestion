from flask import Blueprint, app, jsonify, render_template, request

from app.models import Cliente, db

bp = Blueprint('main', __name__)

@bp.route('/')
def base():
    return render_template('base.html')

@bp.route('/clientes')
def clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@bp.route('/clientes/add', methods=['POST'])
def add_cliente():
    data = request.get_json()
    nombre_cliente = data.get('nombre_cliente')
    if nombre_cliente:
        nuevo_cliente = Cliente(nombre_cliente=nombre_cliente)
        db.session.add(nuevo_cliente)
        db.session.commit()
        return jsonify({'id_cliente': nuevo_cliente.id_cliente, 'nombre_cliente': nuevo_cliente.nombre_cliente}), 201
    return jsonify({'error': 'Nombre requerido'}), 400
