"""
Search routes for finding businesses by industry and location
"""

from flask import Blueprint, request, jsonify
import logging
from app import db
from models import Business, SearchHistory

logger = logging.getLogger(__name__)

search_bp = Blueprint('search', __name__)


@search_bp.route('/businesses', methods=['GET'])
def search_businesses():
    """
    Search businesses by industry and location

    Query Parameters:
    - industry: Required, business industry (e.g., 'plumbing', 'electrician')
    - city: Required, city name
    - state: Optional, state abbreviation (default: all states)
    - limit: Optional, max results (default: 100, max: 1000)
    - offset: Optional, pagination offset (default: 0)
    """
    try:
        industry = request.args.get('industry', '').strip()
        city = request.args.get('city', '').strip()
        state = request.args.get('state', '').strip()
        limit = min(int(request.args.get('limit', 100)), 1000)
        offset = int(request.args.get('offset', 0))

        # Validate required parameters
        if not industry or not city:
            return jsonify({
                'error': 'Missing required parameters: industry and city'
            }), 400

        # Build query
        query = Business.query.filter_by(industry=industry.lower()).filter(
            db.func.lower(Business.city) == city.lower()
        )

        # Filter by state if provided
        if state:
            query = query.filter_by(state=state.upper())

        # Get total count
        total = query.count()

        # Apply pagination
        businesses = query.offset(offset).limit(limit).all()

        # Log search
        try:
            search_history = SearchHistory(
                industry=industry,
                city=city,
                state=state or 'ALL',
                results_count=total
            )
            db.session.add(search_history)
            db.session.commit()
        except Exception as e:
            logger.error(f'Error logging search: {e}')
            db.session.rollback()

        return jsonify({
            'success': True,
            'total': total,
            'limit': limit,
            'offset': offset,
            'results': [b.to_dict() for b in businesses]
        }), 200

    except ValueError as e:
        return jsonify({'error': f'Invalid parameter: {str(e)}'}), 400
    except Exception as e:
        logger.error(f'Search error: {e}')
        return jsonify({'error': 'Search failed'}), 500


@search_bp.route('/industries', methods=['GET'])
def get_industries():
    """Get list of available industries"""
    try:
        industries = db.session.query(Business.industry).distinct().all()
        industry_list = sorted([i[0] for i in industries if i[0]])

        return jsonify({
            'success': True,
            'industries': industry_list,
            'count': len(industry_list)
        }), 200

    except Exception as e:
        logger.error(f'Error getting industries: {e}')
        return jsonify({'error': 'Failed to get industries'}), 500


@search_bp.route('/locations', methods=['GET'])
def get_locations():
    """
    Get list of available city/state combinations

    Query Parameters:
    - industry: Optional, filter by industry
    """
    try:
        industry = request.args.get('industry', '').strip()

        query = db.session.query(
            Business.city,
            Business.state
        ).distinct()

        if industry:
            query = query.filter_by(industry=industry.lower())

        locations = query.all()
        location_list = sorted([
            {'city': loc[0], 'state': loc[1]}
            for loc in locations
            if loc[0] and loc[1]
        ], key=lambda x: (x['state'], x['city']))

        return jsonify({
            'success': True,
            'locations': location_list,
            'count': len(location_list)
        }), 200

    except Exception as e:
        logger.error(f'Error getting locations: {e}')
        return jsonify({'error': 'Failed to get locations'}), 500


@search_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        total_businesses = Business.query.count()
        total_industries = db.session.query(
            Business.industry
        ).distinct().count()
        total_searches = SearchHistory.query.count()

        return jsonify({
            'success': True,
            'total_businesses': total_businesses,
            'total_industries': total_industries,
            'total_searches': total_searches
        }), 200

    except Exception as e:
        logger.error(f'Error getting stats: {e}')
        return jsonify({'error': 'Failed to get stats'}), 500
