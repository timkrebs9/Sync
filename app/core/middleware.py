from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from app.core.security import get_current_user
from app.models.user_model import SubscriptionTier, UserRole
from app.core.database import get_db

class SubscriptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Allow authentication endpoints
        if path.startswith("/api/v2/auth"):
            return await call_next(request)

        # Allow all subscription management endpoints for free users
        if path.startswith("/api/v2/subscription"):
            return await call_next(request)

        # Check if accessing V2 API
        if path.startswith("/api/v2"):
            try:
                auth_header = request.headers.get("Authorization")
                if not auth_header:
                    raise HTTPException(status_code=401, detail="Not authenticated")
                
                db = next(get_db())
                try:
                    token = auth_header.split(" ")[1]
                    user = await get_current_user(token, db)
                    
                    # Allow admin users to bypass subscription check
                    if user.role != UserRole.ADMIN and user.subscription != SubscriptionTier.PREMIUM:
                        raise HTTPException(
                            status_code=403,
                            detail="Premium subscription required for V2 API access"
                        )
                finally:
                    db.close()
            except Exception as e:
                if isinstance(e, HTTPException):
                    raise e
                raise HTTPException(
                    status_code=403,
                    detail="Premium subscription required for V2 API access"
                )

        return await call_next(request)
