from app import db
# Tabla de clientes
class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_cliente = db.Column(db.String(255), nullable=False)
    telefono_cliente = db.Column(db.String(255), nullable=True)
    direccion_cliente = db.Column(db.String(255), nullable=True)

class Transaccion(db.Model):
    __tablename__ = 'transacciones'
    id_transaccion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    
    # Tipo de transacción (Venta o Compra)
    tipo_transaccion = db.Column(db.Enum('VENTA', 'COMPRA'), nullable=False)
    
    # Subcategoría del producto (Cámaras, Insumos, Comodatos)
    tipo_producto = db.Column(db.Enum('CAMARAS', 'INSUMOS', 'COMODATOS'), nullable=False)
    
    fecha_transaccion = db.Column(db.Date, nullable=False)
    dolares = db.Column(db.Numeric(10, 2), nullable=True)
    
    # Campos de pago solo para VENTA (pueden ser nulos)
    ingreso_cheque = db.Column(db.Numeric(10, 2), nullable=True)
    ing_efectivo_n = db.Column(db.Numeric(10, 2), nullable=True)
    ing_efectivo_f = db.Column(db.Numeric(10, 2), nullable=True)
    ingreso_tarjeta = db.Column(db.Numeric(10, 2), nullable=True)
    gasto_tarjeta = db.Column(db.Numeric(10, 2), nullable=True)
    ingreso_transf = db.Column(db.Numeric(10, 2), nullable=True)
    
    # `egreso` solo se usa en COMPRA
    egreso = db.Column(db.Numeric(10, 2), nullable=True)
    
    cliente = db.relationship('Cliente', backref='transacciones', lazy=True)
    


# Tabla de gastos fijos
class GastoFijo(db.Model):
    __tablename__ = 'gastos_fijos'
    id_gasto_fijo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    egreso_cheque = db.Column(db.Numeric(10, 2), nullable=True)
    egreso_efectivo = db.Column(db.Numeric(10, 2), nullable=True)

# Tabla de gastos de casa
class GastoCasa(db.Model):
    __tablename__ = 'gastos_casa'
    id_gasto_casa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Enum('HOGAR', 'OFICINA'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    importe = db.Column(db.Numeric(10, 2), nullable=False)

# Tabla tacataca
class Tacataca(db.Model):
    __tablename__ = 'tacataca'
    id_tacataca = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    n_factura = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    venta = db.Column(db.Numeric(10, 2), nullable=False)
    porcentaje = db.Column(db.Numeric(5, 2))
    comision = db.Column(db.Numeric(10, 2))
    importe = db.Column(db.Numeric(10, 2))
    comision_devuelta = db.Column(db.Numeric(10, 2))
    total_parcial = db.Column(db.Numeric(10, 2))
    retenciones_sirtac = db.Column(db.Numeric(10, 2))
    retencion_iva = db.Column(db.Numeric(10, 2))
    retencion_ganancias = db.Column(db.Numeric(10, 2))
    promo_comision = db.Column(db.Numeric(10, 2))
    total = db.Column(db.Numeric(10, 2))
    tarjeta = db.Column(db.String(50))
    cuotas = db.Column(db.Integer)
    fecha_pago = db.Column(db.Date)
    rendimiento = db.Column(db.Numeric(10, 2))
    cliente = db.relationship('Cliente', backref='tacatacas', lazy=True)

# Tabla clover
class Clover(db.Model):
    __tablename__ = 'clover'
    id_clover = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    n_factura = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    venta = db.Column(db.Numeric(10, 2), nullable=False)
    porcentaje = db.Column(db.Numeric(5, 2))
    recargo = db.Column(db.Numeric(10, 2))
    importe = db.Column(db.Numeric(10, 2))
    arancel = db.Column(db.Numeric(10, 2))
    iva_21 = db.Column(db.Numeric(10, 2))
    promo_en_cuotas_descuento = db.Column(db.Numeric(10, 2))
    iibb = db.Column(db.Numeric(10, 2))
    iva_promo_cuotas_10_5 = db.Column(db.Numeric(10, 2))
    perc_iva_3 = db.Column(db.Numeric(10, 2))
    promo_comision = db.Column(db.Numeric(10, 2))
    total = db.Column(db.Numeric(10, 2))
    tipo_tarjeta = db.Column(db.String(50))
    cuotas = db.Column(db.Integer)
    fecha_pago = db.Column(db.Date)
    cliente = db.relationship('Cliente', backref='clovers', lazy=True)

# Tabla de cheques
class Cheque(db.Model):
    __tablename__ = 'cheques'
    id_cheque = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha_entrega = db.Column(db.Date, nullable=False)
    fecha_cobro = db.Column(db.Date)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    banco = db.Column(db.String(255), nullable=False)
    n_cheque = db.Column(db.String(50), nullable=False)
    importe = db.Column(db.Numeric(10, 2), nullable=False)
    entregado_a = db.Column(db.String(255))
    fecha_dep = db.Column(db.Date)
    cliente = db.relationship('Cliente', backref='cheques', lazy=True)
