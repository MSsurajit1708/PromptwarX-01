import re

def sanitize_string(val):
    if not isinstance(val, str):
        return val
    # Strip potential HTML / dangerous script tags
    cleaned = re.sub(r'<[^>]*?>', '', val)
    return cleaned.strip()

def validate_score(score):
    try:
        val = float(score)
        return max(0.0, min(100.0, val))
    except (ValueError, TypeError):
        return 75.0

cat << 'EOF' > backend/app/middleware/rate_limiter.py
import time
from flask import request
from app.utils.helpers import error_response

# Simple in-memory sliding window rate limiter
_request_history = {}

def rate_limit(max_requests=60, window_seconds=60):
    def decorator(f):
        def wrapper(*args, **kwargs):
            ip = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
            key = f"{request.endpoint}:{ip}"
            now = time.time()
            
            timestamps = _request_history.get(key, [])
            # Filter timestamps within window
            timestamps = [t for t in timestamps if now - t < window_seconds]
            
            if len(timestamps) >= max_requests:
                return error_response("RATE_LIMIT_EXCEEDED", f"Rate limit exceeded. Maximum {max_requests} requests per {window_seconds}s.", 429)
            
            timestamps.append(now)
            _request_history[key] = timestamps
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator
