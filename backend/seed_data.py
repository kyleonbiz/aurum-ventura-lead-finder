"""
Seed sample data for testing
Run: python seed_data.py
"""

import os
from app import app, db
from models import Business
from dotenv import load_dotenv

load_dotenv()

# Sample data
SAMPLE_DATA = [
    # New York - Plumbing
    {
        'name': 'NYC Plumbing Pro', 'industry': 'plumbing', 'category': 'Residential',
        'city': 'New York', 'state': 'NY', 'zip_code': '10001',
        'email': 'info@nycplumbingpro.com', 'phone': '(212) 555-0101',
        'website': 'nycplumbingpro.com', 'employee_count': 15,
        'quality_score': 0.95
    },
    {
        'name': 'Emergency Plumbing NYC', 'industry': 'plumbing', 'category': 'Commercial',
        'city': 'New York', 'state': 'NY', 'zip_code': '10002',
        'email': 'help@emergencyplumbingnyc.com', 'phone': '(212) 555-0102',
        'website': 'emergencyplumbingnyc.com', 'employee_count': 8,
        'quality_score': 0.87
    },
    {
        'name': 'Downtown Manhattan Plumbing', 'industry': 'plumbing', 'category': 'Residential',
        'city': 'New York', 'state': 'NY', 'zip_code': '10003',
        'email': 'service@dtplumbing.com', 'phone': '(212) 555-0103',
        'website': 'dtplumbing.com', 'employee_count': 12,
        'quality_score': 0.92
    },
    {
        'name': 'Bronx Plumbing Solutions', 'industry': 'plumbing', 'category': 'Residential',
        'city': 'New York', 'state': 'NY', 'zip_code': '10451',
        'email': 'contact@bronxplumbing.com', 'phone': '(718) 555-0104',
        'website': 'bronxplumbing.com', 'employee_count': 10,
        'quality_score': 0.88
    },

    # New York - Electrician
    {
        'name': 'NYC Electric', 'industry': 'electrician', 'category': 'Commercial',
        'city': 'New York', 'state': 'NY', 'zip_code': '10004',
        'email': 'jobs@nycelectric.com', 'phone': '(212) 555-0201',
        'website': 'nycelectric.com', 'employee_count': 25,
        'quality_score': 0.96
    },
    {
        'name': 'Lightning Electrical Services', 'industry': 'electrician', 'category': 'Residential',
        'city': 'New York', 'state': 'NY', 'zip_code': '10005',
        'email': 'quote@lightningelectric.com', 'phone': '(212) 555-0202',
        'website': 'lightningelectric.com', 'employee_count': 18,
        'quality_score': 0.91
    },
    {
        'name': 'Manhattan Electrical', 'industry': 'electrician', 'category': 'Commercial',
        'city': 'New York', 'state': 'NY', 'zip_code': '10006',
        'email': 'info@manhattanelectric.com', 'phone': '(212) 555-0203',
        'website': 'manhattanelectric.com', 'employee_count': 20,
        'quality_score': 0.94
    },

    # Los Angeles - Plumbing
    {
        'name': 'LA Plumbing Experts', 'industry': 'plumbing', 'category': 'Residential',
        'city': 'Los Angeles', 'state': 'CA', 'zip_code': '90001',
        'email': 'service@laplumbingexperts.com', 'phone': '(213) 555-0301',
        'website': 'laplumbingexperts.com', 'employee_count': 22,
        'quality_score': 0.89
    },
    {
        'name': 'Hollywood Plumbing Co.', 'industry': 'plumbing', 'category': 'Commercial',
        'city': 'Los Angeles', 'state': 'CA', 'zip_code': '90028',
        'email': 'info@hollywoodplumbing.com', 'phone': '(213) 555-0302',
        'website': 'hollywoodplumbing.com', 'employee_count': 17,
        'quality_score': 0.86
    },
    {
        'name': 'Santa Monica Plumbing', 'industry': 'plumbing', 'category': 'Residential',
        'city': 'Los Angeles', 'state': 'CA', 'zip_code': '90401',
        'email': 'contact@smplumbing.com', 'phone': '(310) 555-0303',
        'website': 'smplumbing.com', 'employee_count': 14,
        'quality_score': 0.90
    },

    # Los Angeles - Electrician
    {
        'name': 'LA Electric Solutions', 'industry': 'electrician', 'category': 'Commercial',
        'city': 'Los Angeles', 'state': 'CA', 'zip_code': '90002',
        'email': 'quotes@laelectricsolutions.com', 'phone': '(213) 555-0401',
        'website': 'laelectricsolutions.com', 'employee_count': 30,
        'quality_score': 0.93
    },
    {
        'name': 'Pasadena Electrical', 'industry': 'electrician', 'category': 'Residential',
        'city': 'Los Angeles', 'state': 'CA', 'zip_code': '91101',
        'email': 'service@pasadenaelectric.com', 'phone': '(626) 555-0402',
        'website': 'pasadenaelectric.com', 'employee_count': 16,
        'quality_score': 0.88
    },

    # Chicago - Plumbing
    {
        'name': 'Chicago Plumbing Pros', 'industry': 'plumbing', 'category': 'Residential',
        'city': 'Chicago', 'state': 'IL', 'zip_code': '60601',
        'email': 'info@chicagoplumbingpros.com', 'phone': '(312) 555-0501',
        'website': 'chicagoplumbingpros.com', 'employee_count': 19,
        'quality_score': 0.91
    },
    {
        'name': 'Windy City Plumbing', 'industry': 'plumbing', 'category': 'Commercial',
        'city': 'Chicago', 'state': 'IL', 'zip_code': '60602',
        'email': 'service@windycityplumbing.com', 'phone': '(312) 555-0502',
        'website': 'windycityplumbing.com', 'employee_count': 24,
        'quality_score': 0.92
    },

    # Chicago - Electrician
    {
        'name': 'Chicago Electrical Works', 'industry': 'electrician', 'category': 'Commercial',
        'city': 'Chicago', 'state': 'IL', 'zip_code': '60603',
        'email': 'jobs@chicagoelectricalworks.com', 'phone': '(312) 555-0601',
        'website': 'chicagoelectricalworks.com', 'employee_count': 28,
        'quality_score': 0.95
    },
    {
        'name': 'North Shore Electric', 'industry': 'electrician', 'category': 'Residential',
        'city': 'Chicago', 'state': 'IL', 'zip_code': '60626',
        'email': 'quote@northshoreelectric.com', 'phone': '(773) 555-0602',
        'website': 'northshoreelectric.com', 'employee_count': 13,
        'quality_score': 0.87
    },
]


def seed_database():
    """Insert sample data into database"""
    with app.app_context():
        # Create tables
        db.create_all()

        # Clear existing data
        Business.query.delete()
        db.session.commit()

        # Insert sample data
        for data in SAMPLE_DATA:
            business = Business(
                name=data['name'],
                industry=data['industry'],
                category=data.get('category'),
                city=data['city'],
                state=data['state'],
                zip_code=data.get('zip_code'),
                email=data.get('email'),
                phone=data.get('phone'),
                website=data.get('website'),
                employee_count=data.get('employee_count'),
                quality_score=data.get('quality_score', 0.5),
                source='sample_data'
            )
            db.session.add(business)

        db.session.commit()
        print(f"✓ Seeded {len(SAMPLE_DATA)} businesses")


if __name__ == '__main__':
    seed_database()
