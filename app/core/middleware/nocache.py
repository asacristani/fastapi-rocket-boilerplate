# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request


# class NoCacheMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         response = await call_next(request)
#         response.headers[
#             "Cache-Control"
#         ] = "no-cache, no-store, must-revalidate"
#         response.headers["Pragma"] = "no-cache"
#         response.headers["Expires"] = "0"
#         return response

# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request
# from starlette.responses import Response

# class ExtendedNoCacheMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         # Call the next middleware or route handler
#         response = await call_next(request)

#         # Get custom caching headers specified in the request scope
#         route_cache_headers = request.scope.get("cache_headers", {})

#         # Merge custom caching headers with the default no-cache headers
#         merged_cache_headers = {
#             "Cache-Control": "no-cache, no-store, must-revalidate",
#             "Pragma": "no-cache",
#             "Expires": "0",
#             **route_cache_headers,  # Merge with route-specific headers
#         }

#         # Update the response headers with the merged caching headers
#         response.headers.update(merged_cache_headers)

#         return response


from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class ExtendedNoCacheMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, default_headers=None):
        self.default_headers = default_headers or {}
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Call the next middleware or route handler
        response = await call_next(request)

        # Get custom caching headers specified in the request scope
        route_cache_headers = request.scope.get("cache_headers", {})

        # Merge custom caching headers with the default no-cache headers
        merged_cache_headers = {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            **route_cache_headers,  # Merge with route-specific headers
        }

        # Update the response headers with the merged caching headers
        response.headers.update(merged_cache_headers)

        return response


