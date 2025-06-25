from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class DiseaseEntry(db.Model):
    """Model for storing disease entries with location and time data"""
    __tablename__ = 'disease_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    disease_name = db.Column(db.String(100), nullable=False, index=True)
    patient_age = db.Column(db.Float, nullable=False)
    address = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False, index=True)
    longitude = db.Column(db.Float, nullable=False, index=True)
    additional_info = db.Column(db.Text)
    occurrence_date = db.Column(db.DateTime, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Risk index for different diseases (can be updated based on historical data)
    DISEASE_RISK_INDEX = {
        'dengue': 0.85,
        'malaria': 0.80,
        'chikungunya': 0.75,
        'typhoid': 0.65,
        'hepatitis_a': 0.60,
        'tuberculosis': 0.70,
        'covid19': 0.90,
        'influenza': 0.55,
        'other': 0.50
    }
    
    def __repr__(self):
        return f'<DiseaseEntry {self.disease_name} at {self.address}>'
    
    @property
    def risk_index(self):
        """Get the risk index for this disease"""
        return self.DISEASE_RISK_INDEX.get(self.disease_name, 0.50)
    
    def to_dict(self):
        """Convert entry to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'disease_name': self.disease_name,
            'patient_age': self.patient_age,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'additional_info': self.additional_info,
            'occurrence_date': self.occurrence_date.isoformat() if self.occurrence_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'risk_index': self.risk_index
        }

class RiskPrediction(db.Model):
    """Model for storing risk predictions for specific areas"""
    __tablename__ = 'risk_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    disease_entry_id = db.Column(db.Integer, db.ForeignKey('disease_entries.id'), nullable=False)
    predicted_lat = db.Column(db.Float, nullable=False)
    predicted_lng = db.Column(db.Float, nullable=False)
    risk_score = db.Column(db.Float, nullable=False)
    risk_radius = db.Column(db.Float, nullable=False)  # in meters
    prediction_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    disease_entry = db.relationship('DiseaseEntry', backref=db.backref('risk_predictions', lazy=True))
    
    def __repr__(self):
        return f'<RiskPrediction {self.risk_score} for entry {self.disease_entry_id}>'
