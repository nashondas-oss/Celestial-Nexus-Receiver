"""
Routing engine for the Celestial Nexus Receiver.
Routes error codes to appropriate Houses based on their metadata.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

from .models.error_codes import ErrorCode, get_error_code, ERROR_001_DISSOCIATION


@dataclass
class RoutingResult:
    """Result of a routing operation."""
    
    error_code: str
    house: int
    house_name: str
    frequency: int
    confidence_level: float
    routed_at: datetime
    blocked_by: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_blocked(self) -> bool:
        """Check if the routing was blocked by another error."""
        return self.blocked_by is not None


@dataclass
class RoutingState:
    """Tracks the current state of the routing system."""
    
    active_routes: List[RoutingResult] = field(default_factory=list)
    unresolved_errors: List[str] = field(default_factory=list)
    
    def has_blocking_error(self) -> Optional[str]:
        """Check if there's a blocking error that prevents other routes."""
        for route in self.active_routes:
            error = get_error_code(route.error_code)
            if error and error.blocks_other_routes:
                return route.error_code
        return None
    
    def add_route(self, route: RoutingResult):
        """Add a new route to active routes."""
        self.active_routes.append(route)
    
    def resolve_error(self, error_code: str):
        """Mark an error as resolved and remove it from active routes."""
        self.active_routes = [r for r in self.active_routes if r.error_code != error_code]
        if error_code in self.unresolved_errors:
            self.unresolved_errors.remove(error_code)
    
    def mark_unresolved(self, error_code: str):
        """Mark an error as unresolved."""
        if error_code not in self.unresolved_errors:
            self.unresolved_errors.append(error_code)


class RoutingEngine:
    """
    Main routing engine that processes error codes and routes them to appropriate Houses.
    """
    
    def __init__(self):
        self.state = RoutingState()
    
    def route_error(self, error_code_str: str, metadata: Optional[Dict[str, Any]] = None) -> RoutingResult:
        """
        Route an error code to its designated House.
        
        Args:
            error_code_str: The error code string (e.g., "ERROR_001")
            metadata: Optional additional metadata for the routing
            
        Returns:
            RoutingResult containing the routing information
            
        Raises:
            ValueError: If the error code is not recognized
        """
        error = get_error_code(error_code_str)
        if not error:
            raise ValueError(f"Unknown error code: {error_code_str}")
        
        # Check if there's a blocking error
        blocking_error = self.state.has_blocking_error()
        if blocking_error and blocking_error != error_code_str:
            # This error is blocked by another error
            result = RoutingResult(
                error_code=error.code,
                house=error.house,
                house_name=error.house_name,
                frequency=error.frequency,
                confidence_level=error.confidence_level,
                routed_at=datetime.utcnow(),
                blocked_by=blocking_error,
                metadata=metadata or {}
            )
            return result
        
        # Create the routing result
        result = RoutingResult(
            error_code=error.code,
            house=error.house,
            house_name=error.house_name,
            frequency=error.frequency,
            confidence_level=error.confidence_level,
            routed_at=datetime.utcnow(),
            metadata=metadata or {}
        )
        
        # Add ceremonial breadcrumbs to metadata
        if error.ceremonial_breadcrumbs:
            result.metadata['ceremonial_breadcrumbs'] = error.ceremonial_breadcrumbs
        
        # Add to active routes
        self.state.add_route(result)
        
        return result
    
    def resolve_error(self, error_code: str):
        """
        Mark an error as resolved, removing it from active routes.
        This allows blocked routes to proceed.
        """
        self.state.resolve_error(error_code)
    
    def diagnose_exhaustion_type(self, indicators: Dict[str, Any]) -> str:
        """
        Diagnose whether exhaustion is POROUS or DEPLETED type.
        
        Args:
            indicators: Dictionary containing diagnostic indicators
                - boundary_permeability: float (0-1) - how porous boundaries are
                - energy_level: float (0-1) - current energy level
                - recovery_rate: float (0-1) - how quickly energy recovers
                
        Returns:
            "EXHAUSTION_POROUS" or "EXHAUSTION_DEPLETED"
        """
        boundary_permeability = indicators.get('boundary_permeability', 0.5)
        energy_level = indicators.get('energy_level', 0.5)
        recovery_rate = indicators.get('recovery_rate', 0.5)
        
        # Porous exhaustion: high boundary permeability, energy leaks out
        # Depleted exhaustion: low energy with intact boundaries
        if boundary_permeability > 0.6 and recovery_rate < 0.4:
            return "EXHAUSTION_POROUS"
        else:
            return "EXHAUSTION_DEPLETED"
    
    def handle_paradox_synthesis(self, paradox_data: Dict[str, Any]) -> RoutingResult:
        """
        Handle both/and paradox states by synthesizing opposing perspectives.
        
        Args:
            paradox_data: Dictionary containing:
                - option_a: Description of first perspective
                - option_b: Description of second perspective
                - synthesis_required: bool - whether synthesis is needed
                
        Returns:
            RoutingResult for the STUCK_PARADOX error
        """
        metadata = {
            'paradox_type': 'both_and',
            'synthesis_approach': 'integrate_perspectives',
            **paradox_data
        }
        
        return self.route_error("ERROR_006", metadata=metadata)
    
    def get_active_routes(self) -> List[RoutingResult]:
        """Get all currently active routes."""
        return self.state.active_routes.copy()
    
    def get_unresolved_errors(self) -> List[str]:
        """Get list of unresolved error codes."""
        return self.state.unresolved_errors.copy()
    
    def reset(self):
        """Reset the routing state (useful for testing)."""
        self.state = RoutingState()
