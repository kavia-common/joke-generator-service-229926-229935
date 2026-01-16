import random
from typing import List

from fastapi import APIRouter, HTTPException, Query, status

from src.api.models import ErrorResponse, Joke

router = APIRouter(prefix="/jokes", tags=["Jokes"])

# Simple in-memory dataset. In a real service, this could come from a database.
_JOKES: List[Joke] = [
    Joke(
        id=1,
        subject="programming",
        setup="Why do programmers prefer dark mode?",
        punchline="Because light attracts bugs.",
    ),
    Joke(
        id=2,
        subject="programming",
        setup="How many programmers does it take to change a light bulb?",
        punchline="None. It's a hardware problem.",
    ),
    Joke(
        id=3,
        subject="math",
        setup="Why was the equal sign so humble?",
        punchline="Because it knew it wasn't less than or greater than anyone else.",
    ),
    Joke(
        id=4,
        subject="science",
        setup="Why can't you trust atoms?",
        punchline="They make up everything.",
    ),
    Joke(
        id=5,
        subject="cats",
        setup="Why did the cat sit on the computer?",
        punchline="To keep an eye on the mouse.",
    ),
]


def _normalize_subject(subject: str) -> str:
    """Normalize a subject for case-insensitive comparisons."""
    return subject.strip().lower()


# PUBLIC_INTERFACE
@router.get(
    "/random",
    response_model=Joke,
    summary="Get a random joke by subject",
    description=(
        "Returns a random joke matching the provided `subject` (case-insensitive). "
        "Example: `/jokes/random?subject=programming`."
    ),
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Invalid request (missing/empty subject).",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No jokes found for the requested subject.",
        },
    },
)
def get_random_joke(
    subject: str = Query(
        ...,
        description="Subject/category to filter jokes by (case-insensitive).",
        min_length=1,
        examples=["programming"],
    ),
) -> Joke:
    """
    Return a random joke filtered by subject.

    Parameters:
        subject: Subject/category to filter jokes by (case-insensitive). Must be provided and non-empty.

    Returns:
        A randomly selected joke matching the subject.

    Raises:
        HTTPException(400): If the subject is missing or empty/whitespace.
        HTTPException(404): If no jokes match the provided subject.
    """
    # Query(..., min_length=1) already enforces presence + non-empty,
    # but we also guard against whitespace-only values for a clearer error payload.
    normalized = _normalize_subject(subject)
    if not normalized:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(
                code="INVALID_SUBJECT",
                message="Query parameter `subject` must be provided and non-empty.",
            ).model_dump(),
        )

    matching = [j for j in _JOKES if _normalize_subject(j.subject) == normalized]
    if not matching:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(
                code="NO_JOKES_FOR_SUBJECT",
                message=f"No jokes found for subject '{subject}'.",
            ).model_dump(),
        )

    return random.choice(matching)
