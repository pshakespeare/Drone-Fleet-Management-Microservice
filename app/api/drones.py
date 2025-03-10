from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.drone import Drone
from app.schemas.drone import DroneSchema, DroneOnboardingSchema
from app.utils.error_handlers import handle_validation_error

drones_bp = Blueprint('drones', __name__)
drone_schema = DroneSchema()
drones_schema = DroneSchema(many=True)
drone_onboarding_schema = DroneOnboardingSchema()

@drones_bp.route('/onboard', methods=['POST'])
def onboard_drones():
    """Onboard new drones for a vendor."""
    try:
        data = request.get_json()
        onboarding_data = drone_onboarding_schema.load(data)
        
        # Process vendor information
        vendor = onboarding_data['vendor']
        db.session.add(vendor)
        db.session.flush()  # Get vendor ID without committing
        
        # Process drones
        drones = []
        for drone_data in onboarding_data['drones']:
            drone = Drone(vendor_id=vendor.id, **drone_data)
            drones.append(drone)
            db.session.add(drone)
        
        db.session.commit()
        return jsonify({
            'message': f'Successfully onboarded {len(drones)} drones',
            'vendor': vendor.vendor_id,
            'drones': [drone.drone_id for drone in drones]
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_validation_error(e)

@drones_bp.route('/', methods=['GET'])
def get_drones():
    """Get all drones with optional filtering."""
    query = Drone.query
    
    # Filter by vendor
    vendor_id = request.args.get('vendor_id')
    if vendor_id:
        query = query.filter_by(vendor_id=vendor_id)
    
    # Filter by payload capacity
    min_payload = request.args.get('min_payload', type=float)
    if min_payload:
        query = query.join(Drone.cargo_capabilities).filter(
            CargoCapabilities.max_payload_kg >= min_payload
        )
    
    drones = query.all()
    return jsonify(drones_schema.dump(drones))

@drones_bp.route('/<drone_id>', methods=['GET'])
def get_drone(drone_id):
    """Get a specific drone."""
    drone = Drone.query.filter_by(drone_id=drone_id).first_or_404()
    return jsonify(drone_schema.dump(drone))

@drones_bp.route('/<drone_id>', methods=['PUT'])
def update_drone(drone_id):
    """Update a drone."""
    try:
        drone = Drone.query.filter_by(drone_id=drone_id).first_or_404()
        data = request.get_json()
        drone = drone_schema.load(data, instance=drone, partial=True)
        db.session.commit()
        return jsonify(drone_schema.dump(drone))
    except Exception as e:
        return handle_validation_error(e)

@drones_bp.route('/<drone_id>', methods=['DELETE'])
def delete_drone(drone_id):
    """Delete a drone."""
    drone = Drone.query.filter_by(drone_id=drone_id).first_or_404()
    db.session.delete(drone)
    db.session.commit()
    return '', 204

@drones_bp.route('/<drone_id>/maintenance', methods=['POST'])
def record_maintenance(drone_id):
    """Record maintenance for a drone."""
    try:
        drone = Drone.query.filter_by(drone_id=drone_id).first_or_404()
        data = request.get_json()
        
        maintenance = drone.maintenance
        if not maintenance:
            maintenance = Maintenance(drone_id=drone.id)
            db.session.add(maintenance)
        
        # Update maintenance information
        for key, value in data.items():
            if hasattr(maintenance, key):
                setattr(maintenance, key, value)
        
        # Handle motor hours
        if 'motor_hours' in data:
            # Clear existing motor hours
            MotorHours.query.filter_by(maintenance_id=maintenance.id).delete()
            
            # Add new motor hours
            for motor_id, hours in data['motor_hours'].items():
                motor_hour = MotorHours(
                    maintenance_id=maintenance.id,
                    motor_identifier=motor_id,
                    hours=hours
                )
                db.session.add(motor_hour)
        
        db.session.commit()
        return jsonify({'message': 'Maintenance record updated successfully'})
    except Exception as e:
        db.session.rollback()
        return handle_validation_error(e) 