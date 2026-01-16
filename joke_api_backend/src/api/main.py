from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.jokes import router as jokes_router

openapi_tags = [
    {"name": "Health", "description": "Service health and status endpoints."},
    {"name": "Jokes", "description": "Joke retrieval endpoints."},
]

app = FastAPI(
    title="Joke Generator Service",
    description="A backend service that returns a random joke based on a user-provided subject.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(jokes_router)


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["Health"],
    summary="Health check",
    description="Simple health check endpoint to verify the service is running.",
)
def health_check():
    """
    Health check endpoint.

    Returns:
        JSON payload with a simple status message.
    """
    return {"message": "Healthy"}
