# from fastapi import FastAPI
# from starlette.middleware import Middleware
# from nocache import ExtendedNoCacheMiddleware  # Replace 'your_module' with the actual module path

# app = FastAPI()

# # Use the ExtendedNoCacheMiddleware
# app.add_middleware(
#     ExtendedNoCacheMiddleware,
#     default_headers={},  # Default caching headers
# )

# # Define a route with custom caching headers
# @app.get("/cached")
# async def cached_data():
#     return {"message": "This response can be cached."}

# # Middleware to set custom caching headers for the "/cached" route
# @app.middleware("http")
# async def extend_cache_headers(request, call_next):
#     if request.url.path == "/cached":
#         # Set caching headers specifically for the "/cached" route
#         request.scope["cache_headers"] = {
#             "Cache-Control": "public, max-age=3600",
#         }
#     response = await call_next(request)
#     return response


from fastapi import FastAPI
from starlette.middleware import Middleware
from nocache import ExtendedNoCacheMiddleware

app = FastAPI()

# Use the ExtendedNoCacheMiddleware
app.add_middleware(
    ExtendedNoCacheMiddleware,
)

# Define a route with custom caching headers
@app.get("/cached")
async def cached_data():
    return {"message": "This response can be cached."}

# Middleware to set custom caching headers for the "/cached" route
@app.middleware("http")
async def extend_cache_headers(request, call_next):
    if request.url.path == "/cached":
        # Set caching headers specifically for the "/cached" route
        request.scope["cache_headers"] = {
            "Cache-Control": "public, max-age=3600",
        }
    response = await call_next(request)
    return response

