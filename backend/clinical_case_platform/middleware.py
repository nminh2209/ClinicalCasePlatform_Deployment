"""
Custom middleware for performance optimization
"""
import gzip
import time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

logger = logging.getLogger('performance')


class ResponseCompressionMiddleware(MiddlewareMixin):
    """
    Compress responses using gzip when client supports it
    """
    
    def process_response(self, request, response):
        # Don't compress if already compressed
        if response.get('Content-Encoding'):
            return response
        
        # Check if client accepts gzip
        accept_encoding = request.META.get('HTTP_ACCEPT_ENCODING', '')
        if 'gzip' not in accept_encoding.lower():
            return response
        
        # Only compress certain content types
        content_type = response.get('Content-Type', '')
        compressible_types = [
            'text/html', 'text/css', 'text/javascript',
            'application/json', 'application/javascript',
            'text/xml', 'application/xml'
        ]
        
        if not any(ct in content_type for ct in compressible_types):
            return response
        
        # Only compress if response is large enough
        if len(response.content) < 1024:  # Don't compress < 1KB
            return response
        
        # Compress the response
        compressed_content = gzip.compress(response.content)
        
        response.content = compressed_content
        response['Content-Encoding'] = 'gzip'
        response['Content-Length'] = str(len(compressed_content))
        
        return response


class RequestTimingMiddleware(MiddlewareMixin):
    """
    Log request processing time for performance monitoring
    """
    
    def process_request(self, request):
        request._start_time = time.time()
        return None
    
    def process_response(self, request, response):
        if hasattr(request, '_start_time'):
            duration = time.time() - request._start_time
            
            # Log slow requests (> 1 second)
            if duration > 1.0:
                logger.warning(
                    f"SLOW REQUEST: {request.method} {request.path} "
                    f"took {duration:.2f}s - Status: {response.status_code}"
                )
            else:
                logger.info(
                    f"{request.method} {request.path} "
                    f"took {duration:.3f}s - Status: {response.status_code}"
                )
            
            # Add timing header for debugging
            response['X-Request-Duration'] = f"{duration:.3f}"
        
        return response


class CacheControlMiddleware(MiddlewareMixin):
    """
    Add appropriate cache control headers based on content type
    """
    
    def process_response(self, request, response):
        # Skip if cache control is already set
        if response.get('Cache-Control'):
            return response
        
        path = request.path
        
        # API responses - short cache for dynamic content
        if path.startswith('/api/'):
            if request.method == 'GET':
                # Different caching for different endpoints
                if 'notifications' in path:
                    response['Cache-Control'] = 'private, max-age=60'  # 1 minute
                elif 'cases' in path and not any(x in path for x in ['create', 'update', 'delete']):
                    response['Cache-Control'] = 'private, max-age=300'  # 5 minutes
                elif 'departments' in path or 'templates' in path:
                    response['Cache-Control'] = 'public, max-age=1800'  # 30 minutes
                else:
                    response['Cache-Control'] = 'private, max-age=0, no-cache'
            else:
                # POST/PUT/DELETE shouldn't be cached
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        
        # Static files - long cache
        elif path.startswith('/static/') or path.startswith('/media/'):
            response['Cache-Control'] = 'public, max-age=31536000'  # 1 year
        
        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to all responses
    """
    
    def process_response(self, request, response):
        # Prevent clickjacking
        if not response.get('X-Frame-Options'):
            response['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME type sniffing
        if not response.get('X-Content-Type-Options'):
            response['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        if not response.get('X-XSS-Protection'):
            response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer policy
        if not response.get('Referrer-Policy'):
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
