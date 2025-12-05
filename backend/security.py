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
        
        # 4. Content-Security-Policy (CSP) - CORRIGÉ POUR LES IMAGES
        # On ajoute les domaines externes autorisés pour les images, les scripts et les styles
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://unpkg.com; "
            "img-src 'self' data: https://images.unsplash.com https://ui-avatars.com; "  # <--- AJOUT ICI
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com;"
        )
        
        # 5. Referrer-Policy
        response.headers["Referrer-Policy"] = "same-origin"

        return response
