"""
Export routes for generating CSV and Excel files
"""

from flask import Blueprint, request, jsonify, send_file
import logging
from datetime import datetime
import csv
import json
from io import StringIO, BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from database import db
from models import Business, Export

logger = logging.getLogger(__name__)

export_bp = Blueprint('export', __name__)


def get_business_records(industry, city, state=None):
    """Get business records matching search criteria"""
    query = Business.query.filter_by(industry=industry.lower()).filter(
        db.func.lower(Business.city) == city.lower()
    )
    if state:
        query = query.filter_by(state=state.upper())
    return query.all()


def log_export(filename, format_type, record_count):
    """Log export to database"""
    try:
        export = Export(
            filename=filename,
            format=format_type,
            record_count=record_count
        )
        db.session.add(export)
        db.session.commit()
    except Exception as e:
        logger.error(f'Error logging export: {e}')
        db.session.rollback()


@export_bp.route('/csv', methods=['POST'])
def export_csv():
    """
    Export search results to CSV

    JSON Body:
    {
        "industry": "plumbing",
        "city": "New York",
        "state": "NY"  // optional
    }
    """
    try:
        data = request.get_json() or {}
        industry = data.get('industry', '').strip()
        city = data.get('city', '').strip()
        state = data.get('state', '').strip()

        if not industry or not city:
            return jsonify({
                'error': 'Missing required fields: industry, city'
            }), 400

        # Get records
        businesses = get_business_records(industry, city, state)

        if not businesses:
            return jsonify({
                'error': f'No results found for {industry} in {city}'
            }), 404

        # Generate CSV
        output = StringIO()
        fieldnames = [
            'name', 'industry', 'category', 'city', 'state', 'zip_code',
            'email', 'phone', 'website', 'employee_count', 'revenue_range',
            'quality_score', 'description'
        ]

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for business in businesses:
            writer.writerow({
                'name': business.name,
                'industry': business.industry,
                'category': business.category or '',
                'city': business.city,
                'state': business.state,
                'zip_code': business.zip_code or '',
                'email': business.email or '',
                'phone': business.phone or '',
                'website': business.website or '',
                'employee_count': business.employee_count or '',
                'revenue_range': business.revenue_range or '',
                'quality_score': business.quality_score or '',
                'description': business.description or '',
            })

        # Log export
        filename = f"{industry}_{city}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        log_export(filename, 'csv', len(businesses))

        # Return file
        output_bytes = BytesIO(output.getvalue().encode('utf-8'))
        output_bytes.seek(0)
        return send_file(
            output_bytes,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        logger.error(f'CSV export error: {e}')
        return jsonify({'error': 'Export failed'}), 500


@export_bp.route('/excel', methods=['POST'])
def export_excel():
    """
    Export search results to Excel

    JSON Body:
    {
        "industry": "plumbing",
        "city": "New York",
        "state": "NY"  // optional
    }
    """
    try:
        data = request.get_json() or {}
        industry = data.get('industry', '').strip()
        city = data.get('city', '').strip()
        state = data.get('state', '').strip()

        if not industry or not city:
            return jsonify({
                'error': 'Missing required fields: industry, city'
            }), 400

        # Get records
        businesses = get_business_records(industry, city, state)

        if not businesses:
            return jsonify({
                'error': f'No results found for {industry} in {city}'
            }), 404

        # Create workbook
        wb = Workbook()
        ws = wb.active
        ws.title = 'Leads'

        # Header styling
        header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
        header_font = Font(bold=True, color='FFFFFF')

        # Headers
        headers = [
            'Name', 'Industry', 'Category', 'City', 'State', 'ZIP',
            'Email', 'Phone', 'Website', 'Employees', 'Revenue', 'Quality', 'Description'
        ]

        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')

        # Data
        for row_num, business in enumerate(businesses, 2):
            ws.cell(row=row_num, column=1).value = business.name
            ws.cell(row=row_num, column=2).value = business.industry
            ws.cell(row=row_num, column=3).value = business.category
            ws.cell(row=row_num, column=4).value = business.city
            ws.cell(row=row_num, column=5).value = business.state
            ws.cell(row=row_num, column=6).value = business.zip_code
            ws.cell(row=row_num, column=7).value = business.email
            ws.cell(row=row_num, column=8).value = business.phone
            ws.cell(row=row_num, column=9).value = business.website
            ws.cell(row=row_num, column=10).value = business.employee_count
            ws.cell(row=row_num, column=11).value = business.revenue_range
            ws.cell(row=row_num, column=12).value = business.quality_score
            ws.cell(row=row_num, column=13).value = business.description

        # Auto-adjust column widths
        for col_num, header in enumerate(headers, 1):
            ws.column_dimensions[chr(64 + col_num)].width = 18

        # Log export
        filename = f"{industry}_{city}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.xlsx"
        log_export(filename, 'xlsx', len(businesses))

        # Return file
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        logger.error(f'Excel export error: {e}')
        return jsonify({'error': 'Export failed'}), 500


@export_bp.route('/json', methods=['POST'])
def export_json():
    """
    Export search results to JSON

    JSON Body:
    {
        "industry": "plumbing",
        "city": "New York",
        "state": "NY"  // optional
    }
    """
    try:
        data = request.get_json() or {}
        industry = data.get('industry', '').strip()
        city = data.get('city', '').strip()
        state = data.get('state', '').strip()

        if not industry or not city:
            return jsonify({
                'error': 'Missing required fields: industry, city'
            }), 400

        # Get records
        businesses = get_business_records(industry, city, state)

        if not businesses:
            return jsonify({
                'error': f'No results found for {industry} in {city}'
            }), 404

        # Build JSON
        json_data = {
            'search': {
                'industry': industry,
                'city': city,
                'state': state or 'All',
                'timestamp': datetime.utcnow().isoformat(),
                'total_results': len(businesses)
            },
            'results': [b.to_dict() for b in businesses]
        }

        # Log export
        filename = f"{industry}_{city}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        log_export(filename, 'json', len(businesses))

        # Return file
        output = BytesIO(json.dumps(json_data, indent=2).encode('utf-8'))
        output.seek(0)

        return send_file(
            output,
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        logger.error(f'JSON export error: {e}')
        return jsonify({'error': 'Export failed'}), 500
