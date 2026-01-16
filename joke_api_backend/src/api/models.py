from pydantic import BaseModel, Field


class Joke(BaseModel):
    """A joke entity returned by the API."""

    id: int = Field(..., description="Unique identifier for the joke.")
    subject: str = Field(..., description="The subject/category of the joke.")
    setup: str = Field(..., description="The setup (question/statement) of the joke.")
    punchline: str = Field(..., description="The punchline of the joke.")


class ErrorResponse(BaseModel):
    """Standard error payload returned by the API."""

    code: str = Field(..., description="A stable, machine-readable error code.")
    message: str = Field(..., description="A human-readable description of the error.")
