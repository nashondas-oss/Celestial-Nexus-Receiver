"""
Test suite for ERROR_002 (EXHAUSTION_POROUS) routing logic.
Tests include differentiation from EXHAUSTION_DEPLETED and escalation sequences.
"""

import pytest
from datetime import datetime

from celestial_nexus.routing_engine import RoutingEngine, RoutingResult
from celestial_nexus.models.error_codes import ERROR_002_EXHAUSTION_POROUS, get_error_code


@pytest.fixture
def engine():
    """Create a fresh routing engine for each test."""
    return RoutingEngine()


class TestError002Basic:
    """Basic tests for ERROR_002 routing."""
    
    def test_error_002_routes_to_house_4(self, engine):
        """Test that ERROR_002 routes to House 4 (Michael)."""
        result = engine.route_error("ERROR_002")
        
        assert result.error_code == "ERROR_002"
        assert result.house == 4
        assert result.house_name == "Michael"
        assert not result.is_blocked
    
    def test_error_002_has_correct_frequency(self, engine):
        """Test that ERROR_002 has frequency 741 Hz."""
        result = engine.route_error("ERROR_002")
        
        assert result.frequency == 741
    
    def test_error_002_has_correct_confidence(self, engine):
        """Test that ERROR_002 has 85% confidence level."""
        result = engine.route_error("ERROR_002")
        
        assert result.confidence_level == 85.0
    
    def test_error_002_includes_ceremonial_breadcrumbs(self, engine):
        """Test that ERROR_002 includes ceremonial breadcrumbs in metadata."""
        result = engine.route_error("ERROR_002")
        
        assert 'ceremonial_breadcrumbs' in result.metadata
        assert 'Awakening' in result.metadata['ceremonial_breadcrumbs']
        assert 'intuition' in result.metadata['ceremonial_breadcrumbs']
    
    def test_error_002_does_not_block_other_routes(self, engine):
        """Test that ERROR_002 does not block other error codes."""
        engine.route_error("ERROR_002")
        
        # Should be able to route ERROR_006 without blocking
        result = engine.route_error("ERROR_006")
        assert not result.is_blocked
    
    def test_error_002_properties(self):
        """Test that ERROR_002 properties are correctly defined."""
        error = get_error_code("ERROR_002")
        
        assert error is not None
        assert error.code == "ERROR_002"
        assert error.name == "EXHAUSTION_POROUS"
        assert error.blocks_other_routes is False
        assert 'porous' in error.description.lower()


class TestExhaustionDifferentiation:
    """Tests for differentiating EXHAUSTION_POROUS from EXHAUSTION_DEPLETED."""
    
    def test_diagnose_porous_exhaustion_high_permeability(self, engine):
        """Test diagnosis of porous exhaustion with high boundary permeability."""
        indicators = {
            'boundary_permeability': 0.8,
            'energy_level': 0.3,
            'recovery_rate': 0.2
        }
        
        diagnosis = engine.diagnose_exhaustion_type(indicators)
        assert diagnosis == "EXHAUSTION_POROUS"
    
    def test_diagnose_depleted_exhaustion_low_permeability(self, engine):
        """Test diagnosis of depleted exhaustion with low boundary permeability."""
        indicators = {
            'boundary_permeability': 0.3,
            'energy_level': 0.2,
            'recovery_rate': 0.2
        }
        
        diagnosis = engine.diagnose_exhaustion_type(indicators)
        assert diagnosis == "EXHAUSTION_DEPLETED"
    
    def test_diagnose_porous_energy_leakage(self, engine):
        """Test diagnosis when energy leaks through boundaries."""
        # High permeability + low recovery = porous
        indicators = {
            'boundary_permeability': 0.7,
            'energy_level': 0.5,
            'recovery_rate': 0.3
        }
        
        diagnosis = engine.diagnose_exhaustion_type(indicators)
        assert diagnosis == "EXHAUSTION_POROUS"
    
    def test_diagnose_depleted_with_good_recovery(self, engine):
        """Test diagnosis when recovery is good but energy is low."""
        indicators = {
            'boundary_permeability': 0.4,
            'energy_level': 0.2,
            'recovery_rate': 0.6
        }
        
        diagnosis = engine.diagnose_exhaustion_type(indicators)
        assert diagnosis == "EXHAUSTION_DEPLETED"
    
    def test_diagnose_edge_case_moderate_values(self, engine):
        """Test diagnosis with moderate values across all indicators."""
        indicators = {
            'boundary_permeability': 0.5,
            'energy_level': 0.5,
            'recovery_rate': 0.5
        }
        
        diagnosis = engine.diagnose_exhaustion_type(indicators)
        # Should default to EXHAUSTION_DEPLETED with moderate values
        assert diagnosis == "EXHAUSTION_DEPLETED"
    
    def test_diagnose_with_missing_indicators(self, engine):
        """Test diagnosis with missing indicators uses defaults."""
        indicators = {}
        
        diagnosis = engine.diagnose_exhaustion_type(indicators)
        # Should work with default values
        assert diagnosis in ["EXHAUSTION_POROUS", "EXHAUSTION_DEPLETED"]


class TestError002Escalation:
    """Tests for ERROR_002 escalation sequences."""
    
    def test_single_error_002_route(self, engine):
        """Test routing a single ERROR_002 instance."""
        result = engine.route_error("ERROR_002")
        
        active_routes = engine.get_active_routes()
        assert len(active_routes) == 1
        assert active_routes[0].error_code == "ERROR_002"
    
    def test_escalation_multiple_instances(self, engine):
        """Test escalation with multiple ERROR_002 instances."""
        metadata1 = {'severity': 'mild', 'duration': 'short'}
        metadata2 = {'severity': 'moderate', 'duration': 'medium'}
        metadata3 = {'severity': 'severe', 'duration': 'long'}
        
        result1 = engine.route_error("ERROR_002", metadata=metadata1)
        result2 = engine.route_error("ERROR_002", metadata=metadata2)
        result3 = engine.route_error("ERROR_002", metadata=metadata3)
        
        active_routes = engine.get_active_routes()
        error_002_routes = [r for r in active_routes if r.error_code == "ERROR_002"]
        
        assert len(error_002_routes) == 3
        assert result1.metadata['severity'] == 'mild'
        assert result2.metadata['severity'] == 'moderate'
        assert result3.metadata['severity'] == 'severe'
    
    def test_escalation_with_time_tracking(self, engine):
        """Test that escalation tracks timing of each route."""
        result1 = engine.route_error("ERROR_002")
        result2 = engine.route_error("ERROR_002")
        
        # Second route should be after or equal to first
        assert result2.routed_at >= result1.routed_at
    
    def test_partial_resolution_escalation(self, engine):
        """Test escalation when some instances are resolved."""
        engine.route_error("ERROR_002")
        engine.route_error("ERROR_002")
        engine.route_error("ERROR_002")
        
        # Resolve all ERROR_002 instances
        engine.resolve_error("ERROR_002")
        
        # Route again (new escalation)
        result = engine.route_error("ERROR_002")
        
        active_routes = engine.get_active_routes()
        error_002_routes = [r for r in active_routes if r.error_code == "ERROR_002"]
        
        assert len(error_002_routes) == 1


class TestError002RealWorldSimulation:
    """Real-world simulation tests for ERROR_002."""
    
    def test_work_overload_scenario(self, engine):
        """Simulate work overload causing porous exhaustion."""
        # Initial state: moderate workload
        indicators_day1 = {
            'boundary_permeability': 0.5,
            'energy_level': 0.6,
            'recovery_rate': 0.5
        }
        diagnosis1 = engine.diagnose_exhaustion_type(indicators_day1)
        
        # After week: boundaries weakening
        indicators_week1 = {
            'boundary_permeability': 0.7,
            'energy_level': 0.4,
            'recovery_rate': 0.3
        }
        diagnosis2 = engine.diagnose_exhaustion_type(indicators_week1)
        
        # Should progress to porous exhaustion
        assert diagnosis2 == "EXHAUSTION_POROUS"
        
        # Route the error
        result = engine.route_error("ERROR_002", metadata={
            'scenario': 'work_overload',
            'indicators': indicators_week1
        })
        
        assert result.house == 4
        assert result.frequency == 741
    
    def test_boundary_repair_progression(self, engine):
        """Simulate boundary repair reducing porous exhaustion."""
        # Start with porous exhaustion
        indicators_start = {
            'boundary_permeability': 0.8,
            'energy_level': 0.3,
            'recovery_rate': 0.2
        }
        
        result = engine.route_error("ERROR_002", metadata={
            'phase': 'initial',
            'indicators': indicators_start
        })
        
        # After intervention: boundaries strengthening
        indicators_recovery = {
            'boundary_permeability': 0.4,
            'energy_level': 0.5,
            'recovery_rate': 0.6
        }
        
        diagnosis = engine.diagnose_exhaustion_type(indicators_recovery)
        # Should transition to depleted type
        assert diagnosis == "EXHAUSTION_DEPLETED"
    
    def test_chronic_porous_exhaustion(self, engine):
        """Simulate chronic porous exhaustion with multiple episodes."""
        # Simulate multiple episodes over time
        for episode in range(5):
            metadata = {
                'episode': episode + 1,
                'boundary_permeability': 0.7 + (episode * 0.02),
                'energy_level': 0.5 - (episode * 0.05)
            }
            result = engine.route_error("ERROR_002", metadata=metadata)
            assert result.house == 4
        
        active_routes = engine.get_active_routes()
        error_002_routes = [r for r in active_routes if r.error_code == "ERROR_002"]
        
        assert len(error_002_routes) == 5
    
    def test_caregiver_burnout_scenario(self, engine):
        """Simulate caregiver burnout leading to porous exhaustion."""
        # Caregiver scenario: high empathy = high permeability
        indicators = {
            'boundary_permeability': 0.85,  # Very porous boundaries
            'energy_level': 0.25,
            'recovery_rate': 0.15  # Difficulty recovering
        }
        
        diagnosis = engine.diagnose_exhaustion_type(indicators)
        assert diagnosis == "EXHAUSTION_POROUS"
        
        result = engine.route_error("ERROR_002", metadata={
            'scenario': 'caregiver_burnout',
            'boundary_state': 'highly_porous',
            'indicators': indicators
        })
        
        assert 'scenario' in result.metadata
        assert result.metadata['boundary_state'] == 'highly_porous'
        assert 'Awakening' in result.metadata['ceremonial_breadcrumbs']


class TestError002EdgeCases:
    """Edge case tests for ERROR_002."""
    
    def test_error_002_blocked_by_error_001(self, engine):
        """Test that ERROR_002 is blocked when ERROR_001 is active."""
        engine.route_error("ERROR_001")
        
        result = engine.route_error("ERROR_002")
        assert result.is_blocked
        assert result.blocked_by == "ERROR_001"
        # But metadata should still be correct
        assert result.house == 4
        assert result.frequency == 741
    
    def test_error_002_with_empty_metadata(self, engine):
        """Test ERROR_002 routing with empty metadata."""
        result = engine.route_error("ERROR_002", metadata={})
        
        assert result.error_code == "ERROR_002"
        # Should still have ceremonial breadcrumbs
        assert 'ceremonial_breadcrumbs' in result.metadata
    
    def test_error_002_frequency_validation(self):
        """Test that ERROR_002 frequency is valid."""
        error = get_error_code("ERROR_002")
        
        # 741 Hz is a valid Solfeggio frequency
        assert error.frequency == 741
        assert 100 <= error.frequency <= 1000
