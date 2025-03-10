from datetime import datetime
from app.extensions import db

class Drone(db.Model):
    """Drone model for storing cargo drone information."""
    
    __tablename__ = 'drones'

    id = db.Column(db.Integer, primary_key=True)
    drone_id = db.Column(db.String(20), unique=True, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Basic Info
    manufacturer = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)
    manufacture_date = db.Column(db.Date, nullable=False)
    drone_type = db.Column(db.String(50), nullable=False)
    lift_system = db.Column(db.String(50), nullable=False)

    # Relationships
    vendor = db.relationship('Vendor', back_populates='drones')
    technical_specs = db.relationship('TechnicalSpecs', uselist=False, back_populates='drone', cascade='all, delete-orphan')
    regulatory_info = db.relationship('RegulatoryInfo', uselist=False, back_populates='drone', cascade='all, delete-orphan')
    cargo_capabilities = db.relationship('CargoCapabilities', uselist=False, back_populates='drone', cascade='all, delete-orphan')
    equipment = db.relationship('Equipment', uselist=False, back_populates='drone', cascade='all, delete-orphan')
    maintenance = db.relationship('Maintenance', uselist=False, back_populates='drone', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Drone {self.drone_id}>'

class TechnicalSpecs(db.Model):
    """Technical specifications for a drone."""
    
    __tablename__ = 'technical_specs'

    id = db.Column(db.Integer, primary_key=True)
    drone_id = db.Column(db.Integer, db.ForeignKey('drones.id'), nullable=False, unique=True)
    empty_weight_kg = db.Column(db.Float, nullable=False)
    length_cm = db.Column(db.Float, nullable=False)
    width_cm = db.Column(db.Float, nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    max_takeoff_weight_kg = db.Column(db.Float, nullable=False)
    max_speed_loaded_kph = db.Column(db.Float, nullable=False)
    max_flight_time_loaded_minutes = db.Column(db.Integer, nullable=False)
    operational_range_loaded_km = db.Column(db.Float, nullable=False)

    # Relationship
    drone = db.relationship('Drone', back_populates='technical_specs')

class RegulatoryInfo(db.Model):
    """Regulatory information for a drone."""
    
    __tablename__ = 'regulatory_info'

    id = db.Column(db.Integer, primary_key=True)
    drone_id = db.Column(db.Integer, db.ForeignKey('drones.id'), nullable=False, unique=True)
    registration_number = db.Column(db.String(100), unique=True, nullable=False)
    certification_type = db.Column(db.String(50), nullable=False)
    special_airworthiness_cert = db.Column(db.Boolean, default=False)
    registration_expiry = db.Column(db.Date, nullable=False)
    operation_type = db.Column(db.String(50), nullable=False)

    # Relationship
    drone = db.relationship('Drone', back_populates='regulatory_info')
    jurisdictions = db.relationship('ApprovedJurisdiction', back_populates='regulatory_info', cascade='all, delete-orphan')

class ApprovedJurisdiction(db.Model):
    """Approved jurisdictions for a drone."""
    
    __tablename__ = 'approved_jurisdictions'

    id = db.Column(db.Integer, primary_key=True)
    regulatory_info_id = db.Column(db.Integer, db.ForeignKey('regulatory_info.id'), nullable=False)
    jurisdiction = db.Column(db.String(50), nullable=False)

    # Relationship
    regulatory_info = db.relationship('RegulatoryInfo', back_populates='jurisdictions')

class CargoCapabilities(db.Model):
    """Cargo capabilities for a drone."""
    
    __tablename__ = 'cargo_capabilities'

    id = db.Column(db.Integer, primary_key=True)
    drone_id = db.Column(db.Integer, db.ForeignKey('drones.id'), nullable=False, unique=True)
    max_payload_kg = db.Column(db.Float, nullable=False)
    cargo_volume_m3 = db.Column(db.Float, nullable=False)
    lift_mechanism = db.Column(db.String(100), nullable=False)
    cargo_securing_method = db.Column(db.String(100), nullable=False)
    load_distribution = db.Column(db.String(100), nullable=False)
    ground_clearance_cm = db.Column(db.Float, nullable=False)

    # Relationship
    drone = db.relationship('Drone', back_populates='cargo_capabilities')
    approved_cargo_types = db.relationship('ApprovedCargoType', back_populates='cargo_capabilities', cascade='all, delete-orphan')

class ApprovedCargoType(db.Model):
    """Approved cargo types for a drone."""
    
    __tablename__ = 'approved_cargo_types'

    id = db.Column(db.Integer, primary_key=True)
    cargo_capabilities_id = db.Column(db.Integer, db.ForeignKey('cargo_capabilities.id'), nullable=False)
    cargo_type = db.Column(db.String(100), nullable=False)

    # Relationship
    cargo_capabilities = db.relationship('CargoCapabilities', back_populates='approved_cargo_types')

class Equipment(db.Model):
    """Equipment information for a drone."""
    
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    drone_id = db.Column(db.Integer, db.ForeignKey('drones.id'), nullable=False, unique=True)
    
    # Lift System
    motor_type = db.Column(db.String(50), nullable=False)
    number_of_motors = db.Column(db.Integer, nullable=False)
    motor_power_kw = db.Column(db.Float, nullable=False)

    # Relationships
    drone = db.relationship('Drone', back_populates='equipment')
    redundancy_features = db.relationship('RedundancyFeature', back_populates='equipment', cascade='all, delete-orphan')
    safety_features = db.relationship('SafetyFeature', back_populates='equipment', cascade='all, delete-orphan')
    sensors = db.relationship('Sensor', back_populates='equipment', cascade='all, delete-orphan')

class RedundancyFeature(db.Model):
    """Redundancy features for drone equipment."""
    
    __tablename__ = 'redundancy_features'

    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    feature = db.Column(db.String(100), nullable=False)

    # Relationship
    equipment = db.relationship('Equipment', back_populates='redundancy_features')

class SafetyFeature(db.Model):
    """Safety features for drone equipment."""
    
    __tablename__ = 'safety_features'

    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    feature = db.Column(db.String(100), nullable=False)

    # Relationship
    equipment = db.relationship('Equipment', back_populates='safety_features')

class Sensor(db.Model):
    """Sensors for drone equipment."""
    
    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    sensor_type = db.Column(db.String(100), nullable=False)

    # Relationship
    equipment = db.relationship('Equipment', back_populates='sensors')

class Maintenance(db.Model):
    """Maintenance information for a drone."""
    
    __tablename__ = 'maintenance'

    id = db.Column(db.Integer, primary_key=True)
    drone_id = db.Column(db.Integer, db.ForeignKey('drones.id'), nullable=False, unique=True)
    last_maintenance_date = db.Column(db.Date, nullable=False)
    flight_hours = db.Column(db.Float, nullable=False)
    load_cycles = db.Column(db.Integer, nullable=False)
    frame_inspection_date = db.Column(db.Date, nullable=False)
    warranty_expiry = db.Column(db.Date, nullable=False)
    maintenance_schedule = db.Column(db.String(50), nullable=False)

    # Relationships
    drone = db.relationship('Drone', back_populates='maintenance')
    motor_hours = db.relationship('MotorHours', back_populates='maintenance', cascade='all, delete-orphan')

class MotorHours(db.Model):
    """Motor hours tracking for drone maintenance."""
    
    __tablename__ = 'motor_hours'

    id = db.Column(db.Integer, primary_key=True)
    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance.id'), nullable=False)
    motor_identifier = db.Column(db.String(50), nullable=False)
    hours = db.Column(db.Float, nullable=False)

    # Relationship
    maintenance = db.relationship('Maintenance', back_populates='motor_hours') 