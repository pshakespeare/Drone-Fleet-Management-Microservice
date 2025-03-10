from marshmallow import Schema, fields, post_load
from app.models.drone import (
    Drone, TechnicalSpecs, RegulatoryInfo, CargoCapabilities,
    Equipment, Maintenance, MotorHours, ApprovedJurisdiction,
    ApprovedCargoType, RedundancyFeature, SafetyFeature, Sensor
)
from app.schemas.vendor import VendorSchema

class MotorHoursSchema(Schema):
    """Schema for motor hours data."""
    
    id = fields.Int(dump_only=True)
    motor_identifier = fields.Str(required=True)
    hours = fields.Float(required=True)

class MaintenanceSchema(Schema):
    """Schema for maintenance data."""
    
    id = fields.Int(dump_only=True)
    last_maintenance_date = fields.Date(required=True)
    flight_hours = fields.Float(required=True)
    load_cycles = fields.Int(required=True)
    frame_inspection_date = fields.Date(required=True)
    warranty_expiry = fields.Date(required=True)
    maintenance_schedule = fields.Str(required=True)
    motor_hours = fields.Nested(MotorHoursSchema, many=True)

class RedundancyFeatureSchema(Schema):
    """Schema for redundancy features."""
    
    id = fields.Int(dump_only=True)
    feature = fields.Str(required=True)

class SafetyFeatureSchema(Schema):
    """Schema for safety features."""
    
    id = fields.Int(dump_only=True)
    feature = fields.Str(required=True)

class SensorSchema(Schema):
    """Schema for sensors."""
    
    id = fields.Int(dump_only=True)
    sensor_type = fields.Str(required=True)

class EquipmentSchema(Schema):
    """Schema for equipment data."""
    
    id = fields.Int(dump_only=True)
    motor_type = fields.Str(required=True)
    number_of_motors = fields.Int(required=True)
    motor_power_kw = fields.Float(required=True)
    redundancy_features = fields.Nested(RedundancyFeatureSchema, many=True)
    safety_features = fields.Nested(SafetyFeatureSchema, many=True)
    sensors = fields.Nested(SensorSchema, many=True)

class ApprovedJurisdictionSchema(Schema):
    """Schema for approved jurisdictions."""
    
    id = fields.Int(dump_only=True)
    jurisdiction = fields.Str(required=True)

class ApprovedCargoTypeSchema(Schema):
    """Schema for approved cargo types."""
    
    id = fields.Int(dump_only=True)
    cargo_type = fields.Str(required=True)

class RegulatoryInfoSchema(Schema):
    """Schema for regulatory information."""
    
    id = fields.Int(dump_only=True)
    registration_number = fields.Str(required=True)
    certification_type = fields.Str(required=True)
    special_airworthiness_cert = fields.Bool(required=True)
    registration_expiry = fields.Date(required=True)
    operation_type = fields.Str(required=True)
    jurisdictions = fields.Nested(ApprovedJurisdictionSchema, many=True)

class CargoCapabilitiesSchema(Schema):
    """Schema for cargo capabilities."""
    
    id = fields.Int(dump_only=True)
    max_payload_kg = fields.Float(required=True)
    cargo_volume_m3 = fields.Float(required=True)
    lift_mechanism = fields.Str(required=True)
    cargo_securing_method = fields.Str(required=True)
    load_distribution = fields.Str(required=True)
    ground_clearance_cm = fields.Float(required=True)
    approved_cargo_types = fields.Nested(ApprovedCargoTypeSchema, many=True)

class TechnicalSpecsSchema(Schema):
    """Schema for technical specifications."""
    
    id = fields.Int(dump_only=True)
    empty_weight_kg = fields.Float(required=True)
    length_cm = fields.Float(required=True)
    width_cm = fields.Float(required=True)
    height_cm = fields.Float(required=True)
    max_takeoff_weight_kg = fields.Float(required=True)
    max_speed_loaded_kph = fields.Float(required=True)
    max_flight_time_loaded_minutes = fields.Int(required=True)
    operational_range_loaded_km = fields.Float(required=True)

class DroneSchema(Schema):
    """Schema for drone data."""
    
    id = fields.Int(dump_only=True)
    drone_id = fields.Str(required=True)
    vendor_id = fields.Int(required=True)
    manufacturer = fields.Str(required=True)
    model = fields.Str(required=True)
    serial_number = fields.Str(required=True)
    manufacture_date = fields.Date(required=True)
    drone_type = fields.Str(required=True)
    lift_system = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    technical_specs = fields.Nested(TechnicalSpecsSchema)
    regulatory_info = fields.Nested(RegulatoryInfoSchema)
    cargo_capabilities = fields.Nested(CargoCapabilitiesSchema)
    equipment = fields.Nested(EquipmentSchema)
    maintenance = fields.Nested(MaintenanceSchema)

    @post_load
    def make_drone(self, data, **kwargs):
        """Create a Drone instance from validated data."""
        return Drone(**data)

class DroneOnboardingSchema(Schema):
    """Schema for onboarding multiple drones."""
    
    vendor = fields.Nested(VendorSchema, required=True)
    drones = fields.Nested(DroneSchema, many=True, required=True) 