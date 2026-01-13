"""
Example demonstrating the routing engine for the three error codes.
This validates the narrative and technical alignment of the routing system.
"""

from celestial_nexus.routing_engine import RoutingEngine


def main():
    """Demonstrate routing logic for all three error codes."""
    
    print("=" * 70)
    print("CELESTIAL NEXUS RECEIVER - ROUTING ENGINE DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Initialize the routing engine
    engine = RoutingEngine()
    
    # Example 1: ERROR_001 (DISSOCIATION) - Highest Priority
    print("1. ERROR_001: DISSOCIATION")
    print("-" * 70)
    result = engine.route_error("ERROR_001")
    print(f"   Error Code: {result.error_code}")
    print(f"   House: {result.house} ({result.house_name})")
    print(f"   Frequency: {result.frequency} Hz")
    print(f"   Confidence Level: {result.confidence_level}%")
    print(f"   Ceremonial Breadcrumbs: {result.metadata.get('ceremonial_breadcrumbs', 'N/A')}")
    print(f"   Blocked: {result.is_blocked}")
    print()
    
    # Example 2: Attempting ERROR_002 while ERROR_001 is active
    print("2. ERROR_002: EXHAUSTION_POROUS (While ERROR_001 is active)")
    print("-" * 70)
    result = engine.route_error("ERROR_002")
    print(f"   Error Code: {result.error_code}")
    print(f"   House: {result.house} ({result.house_name})")
    print(f"   Frequency: {result.frequency} Hz")
    print(f"   Blocked: {result.is_blocked}")
    if result.is_blocked:
        print(f"   Blocked By: {result.blocked_by}")
        print(f"   Note: ERROR_001 blocks all other routes until resolved.")
    print()
    
    # Example 3: Resolve ERROR_001 and route ERROR_002
    print("3. Resolving ERROR_001 and routing ERROR_002")
    print("-" * 70)
    engine.resolve_error("ERROR_001")
    print("   ERROR_001 resolved.")
    
    result = engine.route_error("ERROR_002")
    print(f"   Error Code: {result.error_code}")
    print(f"   House: {result.house} ({result.house_name})")
    print(f"   Frequency: {result.frequency} Hz")
    print(f"   Confidence Level: {result.confidence_level}%")
    print(f"   Ceremonial Breadcrumbs: {result.metadata.get('ceremonial_breadcrumbs', 'N/A')}")
    print(f"   Blocked: {result.is_blocked}")
    print()
    
    # Example 4: Exhaustion type differentiation
    print("4. Exhaustion Type Differentiation")
    print("-" * 70)
    indicators_porous = {
        'boundary_permeability': 0.8,
        'energy_level': 0.3,
        'recovery_rate': 0.2
    }
    diagnosis = engine.diagnose_exhaustion_type(indicators_porous)
    print(f"   Indicators: {indicators_porous}")
    print(f"   Diagnosis: {diagnosis}")
    print()
    
    indicators_depleted = {
        'boundary_permeability': 0.3,
        'energy_level': 0.2,
        'recovery_rate': 0.2
    }
    diagnosis = engine.diagnose_exhaustion_type(indicators_depleted)
    print(f"   Indicators: {indicators_depleted}")
    print(f"   Diagnosis: {diagnosis}")
    print()
    
    # Example 5: ERROR_006 (STUCK_PARADOX) - Both/And Synthesis
    print("5. ERROR_006: STUCK_PARADOX - Both/And Synthesis")
    print("-" * 70)
    paradox_data = {
        'option_a': 'Focus on career growth',
        'option_b': 'Focus on personal relationships',
        'synthesis_required': True
    }
    result = engine.handle_paradox_synthesis(paradox_data)
    print(f"   Error Code: {result.error_code}")
    print(f"   House: {result.house} ({result.house_name})")
    print(f"   Frequency: {result.frequency} Hz")
    print(f"   Confidence Level: {result.confidence_level}%")
    print(f"   Paradox Type: {result.metadata.get('paradox_type', 'N/A')}")
    print(f"   Synthesis Approach: {result.metadata.get('synthesis_approach', 'N/A')}")
    print(f"   Option A: {result.metadata.get('option_a', 'N/A')}")
    print(f"   Option B: {result.metadata.get('option_b', 'N/A')}")
    print(f"   Ceremonial Breadcrumbs: {result.metadata.get('ceremonial_breadcrumbs', 'N/A')}")
    print()
    
    # Example 6: Active Routes Summary
    print("6. Active Routes Summary")
    print("-" * 70)
    active_routes = engine.get_active_routes()
    print(f"   Total Active Routes: {len(active_routes)}")
    for i, route in enumerate(active_routes, 1):
        print(f"   Route {i}:")
        print(f"     - Error: {route.error_code}")
        print(f"     - House: {route.house} ({route.house_name})")
        print(f"     - Frequency: {route.frequency} Hz")
    print()
    
    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
