"""
Database models for Aurum Ventura Lead Finder
"""

from app import db
from datetime import datetime


class Business(db.Model):
    """Business/Lead record"""
    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    industry = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(100))

    # Location info
    city = db.Column(db.String(100), nullable=False, index=True)
    state = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), default='US')
    zip_code = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    # Contact info
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    website = db.Column(db.String(255))

    # Business details
    employee_count = db.Column(db.Integer)
    revenue_range = db.Column(db.String(50))
    description = db.Column(db.Text)

    # Quality & tracking
    quality_score = db.Column(db.Float, default=0.5)
    source = db.Column(db.String(100))
    last_verified = db.Column(db.DateTime, default=datetime.utcnow)

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            'id': self.id,
            'name': self.name,
            'industry': self.industry,
            'category': self.category,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'zip_code': self.zip_code,
            'email': self.email,
            'phone': self.phone,
            'website': self.website,
            'employee_count': self.employee_count,
            'revenue_range': self.revenue_range,
            'quality_score': self.quality_score,
            'description': self.description,
        }


class SearchHistory(db.Model):
    """Track user searches"""
    __tablename__ = 'search_history'

    id = db.Column(db.Integer, primary_key=True)
    industry = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    results_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'industry': self.industry,
            'city': self.city,
            'state': self.state,
            'results_count': self.results_count,
            'created_at': self.created_at.isoformat(),
        }


class Export(db.Model):
    """Track exports"""
    __tablename__ = 'exports'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    format = db.Column(db.String(20))  # csv, xlsx, json
    record_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'format': self.format,
            'record_count': self.record_count,
            'created_at': self.created_at.isoformat(),
        }
