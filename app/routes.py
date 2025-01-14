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


@bp.route('/update_cliente', methods=['POST'])
def update_cliente():
    try:
        # Obtener datos de la solicitud
        data = request.json
        id_cliente = data.get('id_cliente')
        field = data.get('field')
        value = data.get('value')

        if not id_cliente or not field or value is None:
            return jsonify({"error": "Faltan datos requeridos"}), 400

        # Verificar si el cliente existe
        cliente = Cliente.query.get(id_cliente)
        if not cliente:
            return jsonify({"error": "Cliente no encontrado"}), 404

        # Actualizar el campo dinámicamente
        if hasattr(cliente, field):
            setattr(cliente, field, value)
            db.session.commit()
            return jsonify({"success": True, "message": "Cliente actualizado correctamente"})
        else:
            return jsonify({"error": f"Campo '{field}' no válido"}), 400

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500