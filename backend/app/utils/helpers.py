from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code

def error_response(code="ERROR", message="An error occurred", status_code=400, details=None):
    response = {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }
    if details:
        response["error"]["details"] = details
    return jsonify(response), status_code
