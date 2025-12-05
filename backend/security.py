from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # 1. HSTS
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # 2. X-Content-Type-Options
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # 3. X-Frame-Options
        response.headers["X-Frame-Options"] = "DENY"
        
        # 4. Content-Security-Policy (CSP) - CORRECTION ICI
        # On ajoute "script-src 'self' 'unsafe-inline'" pour autoriser nos <script>load...()</script>
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "style-src 'self' 'unsafe-inline';"
        )
        
        # 5. Referrer-Policy
        response.headers["Referrer-Policy"] = "same-origin"

        return response
