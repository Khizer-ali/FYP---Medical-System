from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    reference_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    documents = db.relationship('Document', backref='patient', lazy=True, cascade='all, delete-orphan')
    vitals = db.relationship('Vital', backref='patient', lazy=True, cascade='all, delete-orphan')
    family_history = db.relationship('FamilyHistory', backref='patient', lazy=True, cascade='all, delete-orphan')
    images = db.relationship('MedicalImage', backref='patient', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'reference_number': self.reference_number,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    parsed_text = db.Column(db.Text)
    document_type = db.Column(db.String(100))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'filename': self.filename,
            'parsed_text': self.parsed_text,
            'document_type': self.document_type,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }

class Vital(db.Model):
    __tablename__ = 'vitals'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    temperature = db.Column(db.Float)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    blood_pressure_systolic = db.Column(db.Integer)
    blood_pressure_diastolic = db.Column(db.Integer)
    heart_rate = db.Column(db.Integer)
    respiratory_rate = db.Column(db.Integer)
    oxygen_saturation = db.Column(db.Float)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'temperature': self.temperature,
            'weight': self.weight,
            'height': self.height,
            'blood_pressure_systolic': self.blood_pressure_systolic,
            'blood_pressure_diastolic': self.blood_pressure_diastolic,
            'heart_rate': self.heart_rate,
            'respiratory_rate': self.respiratory_rate,
            'oxygen_saturation': self.oxygen_saturation,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None
        }

class FamilyHistory(db.Model):
    __tablename__ = 'family_history'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    condition = db.Column(db.String(200), nullable=False)
    relation = db.Column(db.String(100))
    age_of_onset = db.Column(db.Integer)
    notes = db.Column(db.Text)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'condition': self.condition,
            'relation': self.relation,
            'age_of_onset': self.age_of_onset,
            'notes': self.notes,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None
        }

class MedicalImage(db.Model):
    __tablename__ = 'medical_images'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    image_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'filename': self.filename,
            'image_type': self.image_type,
            'description': self.description,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }

