from datetime import datetime
from app.extensions import db

class Vendor(db.Model):
    """Vendor model for storing drone vendor information."""
    
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(120), unique=True, nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    specialization = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    drones = db.relationship('Drone', back_populates='vendor', lazy='dynamic')

    def __repr__(self):
        return f'<Vendor {self.vendor_id}>' 