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

@bp.route('/add_cliente', methods=['POST'])
def add_cliente():
    data = request.get_json()
    nombre_cliente = data.get('nombre_cliente')
    telefono_cliente = data.get('telefono_cliente', '-')  # Valor por defecto es un guion
    direccion_cliente = data.get('direccion_cliente', '-')  # Valor por defecto es un guion
    
    # Validación de nombre_cliente
    if not nombre_cliente:
        return jsonify({'error': 'Nombre del cliente es requerido'}), 400
    
    # Crear el cliente y agregarlo a la base de datos
    cliente = Cliente(nombre_cliente=nombre_cliente, telefono_cliente=telefono_cliente, direccion_cliente=direccion_cliente)
    db.session.add(cliente)
    db.session.commit()
    
    # Obtener el ID del cliente generado por la base de datos
    new_cliente = {
        'id_cliente': cliente.id_cliente,  # Usamos el ID generado por la base de datos
        'nombre_cliente': cliente.nombre_cliente,
        'telefono_cliente': cliente.telefono_cliente,
        'direccion_cliente': cliente.direccion_cliente
    }
    
    return jsonify(new_cliente), 201
