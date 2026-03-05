from flask import Blueprint, request, jsonify
from services.traffic_service import (
    get_diversion_logic,
    get_locations_logic,
    get_route_logic,
    get_roads_by_area_logic,
)
from services.llm_service import get_model_name

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health():
    try:
        model = get_model_name()
        return jsonify({"status": "healthy", "model": model})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/get_diversion', methods=['POST'])
def get_diversion():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body cannot be empty"}), 400
            
        closed_road = data.get('closed_road', '').strip()
        area = data.get('area', '').strip()
        
        if not closed_road or not area:
            return jsonify({"error": "Please provide 'closed_road' and 'area'"}), 400

        result = get_diversion_logic(closed_road, area)
        if not isinstance(result, dict):
            return jsonify({"error": "Internal server error"}), 500

        if "error" in result:
            return jsonify(result), result.get("status", 500)
            
        return jsonify(result), 200
    except Exception as e:
        print(f"Error in get_diversion: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@api_bp.route('/get_locations', methods=['GET'])
def get_locations():
    try:
        result = get_locations_logic()
        if not result or "error" in result:
            return jsonify(result if result else {"areas": [], "roads": []})
        return jsonify(result), 200
    except Exception as e:
        print(f"Error in get_locations: {str(e)}")
        return jsonify({"areas": [], "roads": [], "error": str(e)}), 500

@api_bp.route('/roads_by_area', methods=['GET'])
def roads_by_area():
    try:
        area = request.args.get('area', '').strip()
        if not area:
            return jsonify({"roads": []})
        roads = get_roads_by_area_logic(area)
        return jsonify({"roads": roads}), 200
    except Exception as e:
        print(f"Error in roads_by_area: {str(e)}")
        return jsonify({"roads": [], "error": str(e)}), 500

@api_bp.route('/get_route', methods=['POST'])
def get_route():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body cannot be empty"}), 400
            
        source = data.get('source', '').strip()
        destination = data.get('destination', '').strip()
        
        if not source or not destination:
            return jsonify({"error": "Please provide 'source' and 'destination'"}), 400

        result = get_route_logic(source, destination)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error in get_route: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
