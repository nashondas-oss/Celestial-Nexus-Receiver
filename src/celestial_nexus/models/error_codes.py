"""
Error code definitions for the Celestial Nexus Receiver.
Each error code maps to a specific House and frequency for routing.
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class ErrorCode:
    """Represents an error code with routing metadata."""
    
    code: str
    name: str
    house: int
    house_name: str
    frequency: int  # in Hz
    confidence_level: float  # 0-100%
    description: str
    ceremonial_breadcrumbs: Optional[str] = None
    blocks_other_routes: bool = False
    
    def __post_init__(self):
        """Validate error code attributes."""
        if not 0 <= self.confidence_level <= 100:
            raise ValueError(f"Confidence level must be between 0 and 100, got {self.confidence_level}")
        if self.frequency <= 0:
            raise ValueError(f"Frequency must be positive, got {self.frequency}")


# Define the three primary error codes
ERROR_001_DISSOCIATION = ErrorCode(
    code="ERROR_001",
    name="DISSOCIATION",
    house=0,
    house_name="Root",
    frequency=396,
    confidence_level=95.0,
    description="Dissociation state requiring immediate grounding",
    ceremonial_breadcrumbs="Liberation from fear and guilt",
    blocks_other_routes=True  # Highest priority, blocks all other routes
)

ERROR_002_EXHAUSTION_POROUS = ErrorCode(
    code="ERROR_002",
    name="EXHAUSTION_POROUS",
    house=4,
    house_name="Michael",
    frequency=741,
    confidence_level=85.0,
    description="Porous exhaustion state - energy leaks through boundaries",
    ceremonial_breadcrumbs="Awakening intuition and consciousness expansion"
)

ERROR_006_STUCK_PARADOX = ErrorCode(
    code="ERROR_006",
    name="STUCK_PARADOX",
    house=5,
    house_name="Jophiel",
    frequency=639,
    confidence_level=80.0,
    description="Paradox state requiring synthesis of both/and thinking",
    ceremonial_breadcrumbs="Harmonizing relationships and connecting hearts"
)

# Registry of all error codes
ERROR_CODE_REGISTRY = {
    "ERROR_001": ERROR_001_DISSOCIATION,
    "ERROR_002": ERROR_002_EXHAUSTION_POROUS,
    "ERROR_006": ERROR_006_STUCK_PARADOX,
}


def get_error_code(code: str) -> Optional[ErrorCode]:
    """Retrieve an error code by its code string."""
    return ERROR_CODE_REGISTRY.get(code)
