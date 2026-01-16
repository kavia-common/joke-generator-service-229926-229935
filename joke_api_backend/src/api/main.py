from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette import status

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

# Ensure required query parameter validation errors match the service contract (400 + top-level payload).
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(_request, exc: RequestValidationError):
    """
    Convert FastAPI/Pydantic request validation errors into the service's ErrorResponse shape.

    Notes:
        Tests expect a 400 (not 422) when the required `subject` query parameter is missing/invalid,
        and the error payload must be top-level (not nested under `detail`).

    Returns:
        JSONResponse with {"code": "INVALID_REQUEST", "message": "..."}.
    """
    # Provide a concise, stable message tailored to this service's only required query param.
    msg = "Query parameter `subject` is required and must be a non-empty string."
    try:
        # If validation isn't about `subject`, keep a generic-but-concise message.
        # FastAPI error loc often looks like: ("query", "subject")
        has_subject_error = any(
            isinstance(err.get("loc"), (list, tuple)) and "subject" in err.get("loc", [])
            for err in (exc.errors() or [])
        )
        if not has_subject_error:
            msg = "Invalid request."
    except Exception:
        # Defensive: never fail the handler.
        msg = "Invalid request."

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": "INVALID_REQUEST", "message": msg},
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
