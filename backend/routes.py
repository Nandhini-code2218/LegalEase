
import logging

from fastapi import APIRouter, HTTPException

from backend.schemas import DocumentRequest, DocumentResponse
from backend.ai_core.gemini_generator import (
    GeminiDocumentGenerator,
    GeminiConfigurationError,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/generate", response_model=DocumentResponse)
def generate_document(payload: DocumentRequest):
    try:
        generator = GeminiDocumentGenerator()
        document = generator.generate_document(payload)

        return DocumentResponse(
            document=document,
            model=generator.model,
        )

    except GeminiConfigurationError as exc:
        logger.error("Gemini configuration error: %s", exc)
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        # Log the full traceback in the backend terminal.
        # Do not return exception details to the browser.
        logger.exception("LegalEase Gemini generation failed")

        raise HTTPException(
            status_code=502,
            detail=(
                f"AI generation failed ({type(exc).__name__}). "
                "Check the backend terminal for details."
            ),
        ) from exc