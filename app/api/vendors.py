from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.vendor import Vendor
from app.schemas.vendor import VendorSchema
from app.utils.error_handlers import handle_validation_error

vendors_bp = Blueprint('vendors', __name__)
vendor_schema = VendorSchema()
vendors_schema = VendorSchema(many=True)

@vendors_bp.route('/', methods=['POST'])
def create_vendor():
    """Create a new vendor."""
    try:
        data = request.get_json()
        vendor = vendor_schema.load(data)
        db.session.add(vendor)
        db.session.commit()
        return jsonify(vendor_schema.dump(vendor)), 201
    except Exception as e:
        return handle_validation_error(e)

@vendors_bp.route('/', methods=['GET'])
def get_vendors():
    """Get all vendors."""
    vendors = Vendor.query.all()
    return jsonify(vendors_schema.dump(vendors))

@vendors_bp.route('/<vendor_id>', methods=['GET'])
def get_vendor(vendor_id):
    """Get a specific vendor."""
    vendor = Vendor.query.filter_by(vendor_id=vendor_id).first_or_404()
    return jsonify(vendor_schema.dump(vendor))

@vendors_bp.route('/<vendor_id>', methods=['PUT'])
def update_vendor(vendor_id):
    """Update a vendor."""
    try:
        vendor = Vendor.query.filter_by(vendor_id=vendor_id).first_or_404()
        data = request.get_json()
        vendor = vendor_schema.load(data, instance=vendor, partial=True)
        db.session.commit()
        return jsonify(vendor_schema.dump(vendor))
    except Exception as e:
        return handle_validation_error(e)

@vendors_bp.route('/<vendor_id>', methods=['DELETE'])
def delete_vendor(vendor_id):
    """Delete a vendor."""
    vendor = Vendor.query.filter_by(vendor_id=vendor_id).first_or_404()
    db.session.delete(vendor)
    db.session.commit()
    return '', 204 