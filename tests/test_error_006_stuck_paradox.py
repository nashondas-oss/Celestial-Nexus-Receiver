"""
Test suite for ERROR_006 (STUCK_PARADOX) routing logic.
Tests include synthesis logic for both/and states and edge cases.
"""

import pytest
from datetime import datetime

from celestial_nexus.routing_engine import RoutingEngine, RoutingResult
from celestial_nexus.models.error_codes import ERROR_006_STUCK_PARADOX, get_error_code


@pytest.fixture
def engine():
    """Create a fresh routing engine for each test."""
    return RoutingEngine()


class TestError006Basic:
    """Basic tests for ERROR_006 routing."""
    
    def test_error_006_routes_to_house_5(self, engine):
        """Test that ERROR_006 routes to House 5 (Jophiel)."""
        result = engine.route_error("ERROR_006")
        
        assert result.error_code == "ERROR_006"
        assert result.house == 5
        assert result.house_name == "Jophiel"
        assert not result.is_blocked
    
    def test_error_006_has_correct_frequency(self, engine):
        """Test that ERROR_006 has frequency 639 Hz."""
        result = engine.route_error("ERROR_006")
        
        assert result.frequency == 639
    
    def test_error_006_has_correct_confidence(self, engine):
        """Test that ERROR_006 has 80% confidence level."""
        result = engine.route_error("ERROR_006")
        
        assert result.confidence_level == 80.0
    
    def test_error_006_includes_ceremonial_breadcrumbs(self, engine):
        """Test that ERROR_006 includes ceremonial breadcrumbs in metadata."""
        result = engine.route_error("ERROR_006")
        
        assert 'ceremonial_breadcrumbs' in result.metadata
        assert 'Harmonizing' in result.metadata['ceremonial_breadcrumbs']
        assert 'relationships' in result.metadata['ceremonial_breadcrumbs']
    
    def test_error_006_does_not_block_other_routes(self, engine):
        """Test that ERROR_006 does not block other error codes."""
        engine.route_error("ERROR_006")
        
        # Should be able to route ERROR_002 without blocking
        result = engine.route_error("ERROR_002")
        assert not result.is_blocked
    
    def test_error_006_properties(self):
        """Test that ERROR_006 properties are correctly defined."""
        error = get_error_code("ERROR_006")
        
        assert error is not None
        assert error.code == "ERROR_006"
        assert error.name == "STUCK_PARADOX"
        assert error.blocks_other_routes is False
        assert 'paradox' in error.description.lower()
        assert 'both/and' in error.description.lower()


class TestParadoxSynthesis:
    """Tests for paradox synthesis logic."""
    
    def test_handle_simple_paradox(self, engine):
        """Test handling a simple both/and paradox."""
        paradox_data = {
            'option_a': 'Focus on career growth',
            'option_b': 'Focus on personal relationships',
            'synthesis_required': True
        }
        
        result = engine.handle_paradox_synthesis(paradox_data)
        
        assert result.error_code == "ERROR_006"
        assert result.house == 5
        assert result.metadata['paradox_type'] == 'both_and'
        assert result.metadata['synthesis_approach'] == 'integrate_perspectives'
        assert result.metadata['option_a'] == 'Focus on career growth'
        assert result.metadata['option_b'] == 'Focus on personal relationships'
    
    def test_synthesis_with_complex_options(self, engine):
        """Test synthesis with complex, nuanced options."""
        paradox_data = {
            'option_a': 'Stay in current stable position with known constraints',
            'option_b': 'Take risky opportunity with uncertain outcomes',
            'synthesis_required': True,
            'context': 'career_transition'
        }
        
        result = engine.handle_paradox_synthesis(paradox_data)
        
        assert result.error_code == "ERROR_006"
        assert 'context' in result.metadata
        assert result.metadata['context'] == 'career_transition'
    
    def test_synthesis_without_explicit_requirement(self, engine):
        """Test synthesis when synthesis_required is not explicitly set."""
        paradox_data = {
            'option_a': 'Independence',
            'option_b': 'Connection'
        }
        
        result = engine.handle_paradox_synthesis(paradox_data)
        
        assert result.error_code == "ERROR_006"
        assert result.metadata['synthesis_approach'] == 'integrate_perspectives'
    
    def test_synthesis_preserves_both_perspectives(self, engine):
        """Test that synthesis preserves both perspectives in metadata."""
        paradox_data = {
            'option_a': 'Logic',
            'option_b': 'Emotion'
        }
        
        result = engine.handle_paradox_synthesis(paradox_data)
        
        # Both should be preserved
        assert 'option_a' in result.metadata
        assert 'option_b' in result.metadata
        assert result.metadata['option_a'] == 'Logic'
        assert result.metadata['option_b'] == 'Emotion'


class TestBothAndStates:
    """Tests for handling both/and states."""
    
    def test_both_and_career_family_balance(self, engine):
        """Test both/and state for career and family balance."""
        paradox_data = {
            'option_a': 'Career advancement',
            'option_b': 'Family time',
            'synthesis_required': True,
            'state_type': 'both_and',
            'resolution': 'integrate_both'
        }
        
        result = engine.handle_paradox_synthesis(paradox_data)
        
        assert result.house == 5
        assert result.frequency == 639
        assert result.metadata['state_type'] == 'both_and'
        assert result.metadata['resolution'] == 'integrate_both'
    
    def test_both_and_strength_vulnerability(self, engine):
        """Test both/and state for strength and vulnerability."""
        paradox_data = {
            'option_a': 'Show strength and confidence',
            'option_b': 'Be vulnerable and authentic',
            'synthesis_required': True
        }
        
        result = engine.handle_paradox_synthesis(paradox_data)
        
        assert result.error_code == "ERROR_006"
        assert 'Harmonizing' in result.metadata['ceremonial_breadcrumbs']
    
    def test_both_and_autonomy_interdependence(self, engine):
        """Test both/and state for autonomy and interdependence."""
        paradox_data = {
            'option_a': 'Maintain personal autonomy',
            'option_b': 'Build interdependent relationships',
            'context': 'relationship_development'
        }
        
        result = engine.handle_paradox_synthesis(paradox_data)
        
        assert result.metadata['paradox_type'] == 'both_and'
        assert result.metadata['context'] == 'relationship_development'
    
    def test_multiple_both_and_states(self, engine):
        """Test handling multiple both/and states simultaneously."""
        paradox1 = {'option_a': 'A1', 'option_b': 'B1'}
        paradox2 = {'option_a': 'A2', 'option_b': 'B2'}
        paradox3 = {'option_a': 'A3', 'option_b': 'B3'}
        
        result1 = engine.handle_paradox_synthesis(paradox1)
        result2 = engine.handle_paradox_synthesis(paradox2)
        result3 = engine.handle_paradox_synthesis(paradox3)
        
        active_routes = engine.get_active_routes()
        error_006_routes = [r for r in active_routes if r.error_code == "ERROR_006"]
        
        assert len(error_006_routes) == 3


class TestError006NormalUseCases:
    """Normal use case tests for ERROR_006."""
    
    def test_decision_making_paradox(self, engine):
        """Test paradox in decision-making scenario."""
        result = engine.route_error("ERROR_006", metadata={
            'scenario': 'decision_paralysis',
            'option_a': 'Path A',
            'option_b': 'Path B',
            'stuck_duration': 'weeks'
        })
        
        assert result.error_code == "ERROR_006"
        assert result.metadata['scenario'] == 'decision_paralysis'
        assert result.metadata['stuck_duration'] == 'weeks'
    
    def test_identity_paradox(self, engine):
        """Test paradox in identity integration."""
        result = engine.route_error("ERROR_006", metadata={
            'scenario': 'identity_integration',
            'aspect_a': 'Professional identity',
            'aspect_b': 'Personal identity',
            'integration_needed': True
        })
        
        assert result.house == 5
        assert result.metadata['integration_needed'] is True
    
    def test_value_conflict_paradox(self, engine):
        """Test paradox from conflicting values."""
        result = engine.route_error("ERROR_006", metadata={
            'scenario': 'value_conflict',
            'value_a': 'Achievement',
            'value_b': 'Rest',
            'culture_factor': 'productivity_pressure'
        })
        
        assert result.error_code == "ERROR_006"
        assert 'culture_factor' in result.metadata
    
    def test_relationship_paradox(self, engine):
        """Test paradox in relationship dynamics."""
        result = engine.route_error("ERROR_006", metadata={
            'scenario': 'relationship_paradox',
            'need_a': 'Closeness',
            'need_b': 'Independence',
            'relationship_type': 'romantic'
        })
        
        assert result.frequency == 639
        assert 'relationships' in result.metadata['ceremonial_breadcrumbs']


class TestError006EdgeCases:
    """Edge case tests for ERROR_006."""
    
    def test_error_006_blocked_by_error_001(self, engine):
        """Test that ERROR_006 is blocked when ERROR_001 is active."""
        engine.route_error("ERROR_001")
        
        result = engine.route_error("ERROR_006")
        assert result.is_blocked
        assert result.blocked_by == "ERROR_001"
        # But metadata should still be correct
        assert result.house == 5
        assert result.frequency == 639
    
    def test_error_006_with_minimal_metadata(self, engine):
        """Test ERROR_006 with minimal metadata."""
        result = engine.route_error("ERROR_006")
        
        assert result.error_code == "ERROR_006"
        # Should still have ceremonial breadcrumbs
        assert 'ceremonial_breadcrumbs' in result.metadata
    
    def test_paradox_with_same_options(self, engine):
        """Test paradox where both options appear similar."""
        paradox_data = {
            'option_a': 'Stay present',
            'option_b': 'Stay present mindfully',
            'synthesis_required': True
        }
        
        result = engine.handle_paradox_synthesis(paradox_data)
        
        # Should still route successfully
        assert result.error_code == "ERROR_006"
        assert result.metadata['option_a'] != result.metadata['option_b']
    
    def test_nested_paradoxes(self, engine):
        """Test handling nested or recursive paradoxes."""
        paradox_data = {
            'option_a': 'Resolve paradox by choosing',
            'option_b': 'Hold paradox without choosing',
            'meta_paradox': True
        }
        
        result = engine.handle_paradox_synthesis(paradox_data)
        
        assert result.error_code == "ERROR_006"
        assert result.metadata['meta_paradox'] is True
    
    def test_error_006_frequency_validation(self):
        """Test that ERROR_006 frequency is valid."""
        error = get_error_code("ERROR_006")
        
        # 639 Hz is a valid Solfeggio frequency (FA - connection/relationships)
        assert error.frequency == 639
        assert 100 <= error.frequency <= 1000
    
    def test_rapid_paradox_routing(self, engine):
        """Test rapid routing of multiple paradoxes."""
        for i in range(10):
            result = engine.route_error("ERROR_006", metadata={
                'iteration': i,
                'rapid_test': True
            })
            assert result.error_code == "ERROR_006"
            assert not result.is_blocked
        
        active_routes = engine.get_active_routes()
        error_006_routes = [r for r in active_routes if r.error_code == "ERROR_006"]
        assert len(error_006_routes) == 10
    
    def test_error_006_resolution_and_reroute(self, engine):
        """Test resolving ERROR_006 and routing again."""
        # Initial route
        result1 = engine.route_error("ERROR_006")
        assert len(engine.get_active_routes()) == 1
        
        # Resolve
        engine.resolve_error("ERROR_006")
        assert len(engine.get_active_routes()) == 0
        
        # Route again
        result2 = engine.route_error("ERROR_006")
        assert len(engine.get_active_routes()) == 1
        assert not result2.is_blocked


class TestError006Integration:
    """Integration tests for ERROR_006 with other error types."""
    
    def test_error_006_with_error_002(self, engine):
        """Test ERROR_006 routing alongside ERROR_002."""
        result1 = engine.route_error("ERROR_002")
        result2 = engine.route_error("ERROR_006")
        
        # Both should route successfully (neither blocks)
        assert not result1.is_blocked
        assert not result2.is_blocked
        assert len(engine.get_active_routes()) == 2
    
    def test_error_006_after_error_001_resolution(self, engine):
        """Test ERROR_006 routing after ERROR_001 is resolved."""
        # Route ERROR_001 (blocks others)
        engine.route_error("ERROR_001")
        
        # ERROR_006 is blocked
        blocked_result = engine.route_error("ERROR_006")
        assert blocked_result.is_blocked
        
        # Resolve ERROR_001
        engine.resolve_error("ERROR_001")
        
        # Now ERROR_006 should route successfully
        result = engine.route_error("ERROR_006")
        assert not result.is_blocked
        assert result.house == 5
    
    def test_all_errors_together(self, engine):
        """Test all three error types routing together (when none block)."""
        # Route ERROR_002 and ERROR_006 (neither blocks)
        result2 = engine.route_error("ERROR_002")
        result6 = engine.route_error("ERROR_006")
        
        assert not result2.is_blocked
        assert not result6.is_blocked
        
        active_routes = engine.get_active_routes()
        assert len(active_routes) == 2
        
        # Now route ERROR_001 (blocks others)
        result1 = engine.route_error("ERROR_001")
        assert not result1.is_blocked
        
        # Try routing others - should be blocked
        blocked_result = engine.route_error("ERROR_002")
        assert blocked_result.is_blocked
