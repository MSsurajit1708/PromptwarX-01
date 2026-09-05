from app.utils.helpers import error_response

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return error_response("BAD_REQUEST", str(e.description) if hasattr(e, 'description') else "Bad request", 400)

    @app.errorhandler(404)
    def not_found(e):
        return error_response("NOT_FOUND", "Requested resource was not found", 404)

    @app.errorhandler(429)
    def rate_limited(e):
        return error_response("RATE_LIMITED", "Too many requests. Please try again later.", 429)

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f"Server Error: {str(e)}")
        return error_response("INTERNAL_SERVER_ERROR", "An unexpected server error occurred", 500)
