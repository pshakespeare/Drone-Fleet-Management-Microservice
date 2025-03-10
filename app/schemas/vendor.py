from marshmallow import Schema, fields, post_load
from app.models.vendor import Vendor

class VendorSchema(Schema):
    """Schema for serializing/deserializing vendor data."""
    
    id = fields.Int(dump_only=True)
    vendor_id = fields.Str(required=True)
    name = fields.Str(required=True)
    contact_email = fields.Email(required=True)
    contact_phone = fields.Str(required=True)
    specialization = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_vendor(self, data, **kwargs):
        """Create a Vendor instance from validated data."""
        return Vendor(**data) 