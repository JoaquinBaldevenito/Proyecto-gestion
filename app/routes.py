from datetime import datetime
from flask import Blueprint, app, jsonify, render_template, request

from app.models import Cliente, Transaccion, db

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
    
@bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    # Ejecutar la consulta para obtener los clientes
    clientes = Cliente.query.all()  # Asegúrate de que esto devuelva una lista
    # Filtrar los clientes
    filtered_clients = [c for c in clientes if query in c.nombre_cliente.lower()]
    # Convertir a JSON para enviar al front-end
    return jsonify([{
        'id_cliente': c.id_cliente,
        'nombre_cliente': c.nombre_cliente,
        'telefono_cliente': c.telefono_cliente,
        'direccion_cliente': c.direccion_cliente
    } for c in filtered_clients])

    
@bp.route('/ventas')
def ventas():
    transacciones = Transaccion.query.all()
    return render_template('ventas.html', transacciones=transacciones)


@bp.route('/add_transaccion', methods=['POST'])
def add_transaccion():

    data = request.get_json()
    id_cliente=data.get('id_cliente')
    tipo_transaccion=data.get('tipo_transaccion')
    tipo_producto=data.get('tipo_producto')
    fecha_transaccion=datetime.strptime(data.get('fecha_transaccion'), '%Y-%m-%d')
    dolares=data.get('dolares')
    ingreso_cheque=data.get('ingreso_cheque')
    ing_efectivo_n=data.get('ing_efectivo_n')
    ing_efectivo_f=data.get('ing_efectivo_f')
    ingreso_tarjeta=data.get('ingreso_tarjeta')
    gasto_tarjeta=data.get('gasto_tarjeta')
    ingreso_transf=data.get('ingreso_transf')
    egreso=data.get('egreso')
    
    nueva_transaccion = Transaccion(
        id_cliente=id_cliente, 
        tipo_transaccion=tipo_transaccion,
        tipo_producto=tipo_producto,
        fecha_transaccion=fecha_transaccion,
        dolares=dolares,
        ingreso_cheque=ingreso_cheque,
        ing_efectivo_n=ing_efectivo_n,
        ing_efectivo_f=ing_efectivo_f,
        ingreso_tarjeta=ingreso_tarjeta,
        gasto_tarjeta=gasto_tarjeta,
        ingreso_transf=ingreso_transf,
        egreso=egreso
        )
    
    db.session.add(nueva_transaccion)
    db.session.commit()
    
    return jsonify({
        'id_transaccion': nueva_transaccion.id_transaccion,
        'id_cliente': nueva_transaccion.id_cliente,
        'tipo_transaccion': nueva_transaccion.tipo_transaccion,
        'tipo_producto': nueva_transaccion.tipo_producto,
        'fecha_transaccion': nueva_transaccion.fecha_transaccion.strftime('%Y-%m-%d'),
        'dolares': nueva_transaccion.dolares,
        'ingreso_cheque': nueva_transaccion.ingreso_cheque,
        'ing_efectivo_n': nueva_transaccion.ing_efectivo_n,
        'ing_efectivo_f': nueva_transaccion.ing_efectivo_f,
        'ingreso_tarjeta': nueva_transaccion.ingreso_tarjeta,
        'gasto_tarjeta': nueva_transaccion.gasto_tarjeta,
        'ingreso_transf': nueva_transaccion.ingreso_transf,
        'egreso': nueva_transaccion.egreso,
    }), 201
    
@bp.route('/update_transaccion', methods=['POST'])
def update_transaccion():
    try:
        data = request.json
        id_transaccion = data['id_transaccion']
        field = data['field']
        value = data['value']

        # Encontrar la transacción por ID
        transaccion = Transaccion.query.get(id_transaccion)
        if not transaccion:
            return jsonify({'error': 'Transacción no encontrada'}), 404

        # Actualizar el campo específico
        if field in ['dolares', 'ingreso_cheque', 'ing_efectivo_n', 'ing_efectivo_f', 
                     'ingreso_tarjeta', 'gasto_tarjeta', 'ingreso_transf', 'egreso']:
            setattr(transaccion, field, float(value) if value else None)
        elif field == 'fecha_transaccion':
            transaccion.fecha_transaccion = datetime.strptime(value, '%Y-%m-%d')
        else:
            setattr(transaccion, field, value)

        db.session.commit()
        return jsonify({'message': 'Transacción actualizada con éxito'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
