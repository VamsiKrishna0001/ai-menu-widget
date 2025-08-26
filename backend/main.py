from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from routes.generate import router as generate_router

app = FastAPI(
    title="AI-Powered Menu Intelligence Widget API",
    description="Backend API for generating food item descriptions with AI intelligence, caching, and data persistence",
    version="2.0.0"
)

# Configure rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the generate router
app.include_router(generate_router, prefix="/api/v1", tags=["generate"])

@app.get("/")
async def root():
    return {
        "message": "AI-Powered Menu Intelligence Widget API",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "Food item description generation",
            "Caching and data persistence",
            "Cache management",
            "Rate limiting (5 requests/minute)"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/v1/rate-limit/status")
@limiter.limit("5/minute")
async def rate_limit_status(request: Request):
    """Get current rate limit status for the client"""
    return {
        "rate_limit": "5 requests per minute",
        "client_ip": get_remote_address(request),
        "remaining_requests": "Check response headers for details"
    }

@app.get("/api-info")
async def api_info():
    """Get detailed API information"""
    return {
        "api_name": "AI-Powered Menu Intelligence Widget API",
        "version": "2.0.0",
        "description": "Advanced API for food item description generation with intelligent caching",
        "endpoints": {
            "generate": "/api/v1/generate-description",
            "regenerate": "/api/v1/regenerate-description",
        },
        "models": {
            "gpt-3.5-turbo": "Light and fresh description style",
            "gpt-4.1-mini": "Dark and sophisticated description style"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
