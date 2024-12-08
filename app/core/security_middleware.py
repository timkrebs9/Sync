from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict
from datetime import datetime

# Storage for rate limiting with defaultdict
rate_limit_storage = defaultdict(lambda: {"count": 0, "window_start": 0})

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.window_size = 60  # 1 minute in seconds

    async def dispatch(self, request: Request, call_next):
        # Only apply rate limiting to V2 API endpoints
        if "/api/v2/" in request.url.path:
            client_ip = request.client.host
            current_time = int(time.time())
            
            # Reset window if needed
            if current_time - rate_limit_storage[client_ip]["window_start"] >= self.window_size:
                rate_limit_storage[client_ip] = {
                    "count": 0,
                    "window_start": current_time
                }
            
            # Increment request count
            rate_limit_storage[client_ip]["count"] += 1
            
            # Check if limit exceeded
            if rate_limit_storage[client_ip]["count"] > self.requests_per_minute:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded"
                )

        response = await call_next(request)
        return response 