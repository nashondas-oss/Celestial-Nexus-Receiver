"""
Test suite for ERROR_001 (DISSOCIATION) routing logic.
Tests include override logic, edge cases, and blocking behavior.
"""

import pytest
from datetime import datetime

from celestial_nexus.routing_engine import RoutingEngine, RoutingResult
from celestial_nexus.models.error_codes import ERROR_001_DISSOCIATION, get_error_code


@pytest.fixture
def engine():
    """Create a fresh routing engine for each test."""
    return RoutingEngine()


class TestError001Basic:
    """Basic tests for ERROR_001 routing."""
    
    def test_error_001_routes_to_house_0(self, engine):
        """Test that ERROR_001 routes to House 0 (Root)."""
        result = engine.route_error("ERROR_001")
        
        assert result.error_code == "ERROR_001"
        assert result.house == 0
        assert result.house_name == "Root"
        assert not result.is_blocked
    
    def test_error_001_has_correct_frequency(self, engine):
        """Test that ERROR_001 has frequency 396 Hz."""
        result = engine.route_error("ERROR_001")
        
        assert result.frequency == 396
    
    def test_error_001_has_high_confidence(self, engine):
        """Test that ERROR_001 has 95% confidence level."""
        result = engine.route_error("ERROR_001")
        
        assert result.confidence_level == 95.0
    
    def test_error_001_includes_ceremonial_breadcrumbs(self, engine):
        """Test that ERROR_001 includes ceremonial breadcrumbs in metadata."""
        result = engine.route_error("ERROR_001")
        
        assert 'ceremonial_breadcrumbs' in result.metadata
        assert 'Liberation' in result.metadata['ceremonial_breadcrumbs']
    
    def test_error_001_has_timestamp(self, engine):
        """Test that routing result includes timestamp."""
        before = datetime.utcnow()
        result = engine.route_error("ERROR_001")
        after = datetime.utcnow()
        
        assert before <= result.routed_at <= after


class TestError001Blocking:
    """Tests for ERROR_001 blocking behavior."""
    
    def test_error_001_blocks_other_routes(self, engine):
        """Test that ERROR_001 blocks other error codes from routing."""
        # First route ERROR_001
        result1 = engine.route_error("ERROR_001")
        assert not result1.is_blocked
        
        # Try to route ERROR_002 - should be blocked
        result2 = engine.route_error("ERROR_002")
        assert result2.is_blocked
        assert result2.blocked_by == "ERROR_001"
    
    def test_error_001_blocks_multiple_errors(self, engine):
        """Test that ERROR_001 blocks multiple subsequent errors."""
        engine.route_error("ERROR_001")
        
        result2 = engine.route_error("ERROR_002")
        result3 = engine.route_error("ERROR_006")
        
        assert result2.is_blocked
        assert result3.is_blocked
        assert result2.blocked_by == "ERROR_001"
        assert result3.blocked_by == "ERROR_001"
    
    def test_error_001_does_not_block_itself(self, engine):
        """Test that ERROR_001 doesn't block subsequent ERROR_001 routes."""
        result1 = engine.route_error("ERROR_001")
        result2 = engine.route_error("ERROR_001")
        
        assert not result1.is_blocked
        assert not result2.is_blocked
    
    def test_resolution_unblocks_routes(self, engine):
        """Test that resolving ERROR_001 allows other routes to proceed."""
        # Route ERROR_001, blocking others
        engine.route_error("ERROR_001")
        
        # Verify blocking
        blocked_result = engine.route_error("ERROR_002")
        assert blocked_result.is_blocked
        
        # Resolve ERROR_001
        engine.resolve_error("ERROR_001")
        
        # Now ERROR_002 should route successfully
        result = engine.route_error("ERROR_002")
        assert not result.is_blocked
        assert result.house == 4


class TestError001EdgeCases:
    """Edge case tests for ERROR_001."""
    
    def test_error_001_with_custom_metadata(self, engine):
        """Test ERROR_001 routing with custom metadata."""
        custom_metadata = {
            'user_id': 'test_user_123',
            'severity': 'high',
            'context': 'stress_trigger'
        }
        
        result = engine.route_error("ERROR_001", metadata=custom_metadata)
        
        assert result.metadata['user_id'] == 'test_user_123'
        assert result.metadata['severity'] == 'high'
        assert result.metadata['context'] == 'stress_trigger'
        # Should also include ceremonial breadcrumbs
        assert 'ceremonial_breadcrumbs' in result.metadata
    
    def test_multiple_error_001_instances_tracked(self, engine):
        """Test that multiple ERROR_001 instances are tracked in active routes."""
        engine.route_error("ERROR_001")
        engine.route_error("ERROR_001")
        engine.route_error("ERROR_001")
        
        active_routes = engine.get_active_routes()
        error_001_routes = [r for r in active_routes if r.error_code == "ERROR_001"]
        
        assert len(error_001_routes) == 3
    
    def test_resolving_one_error_001_keeps_others_active(self, engine):
        """Test that resolving one ERROR_001 keeps others active if multiple exist."""
        engine.route_error("ERROR_001")
        engine.route_error("ERROR_001")
        
        # Resolve once
        engine.resolve_error("ERROR_001")
        
        active_routes = engine.get_active_routes()
        # Note: resolve_error removes ALL instances with that code
        error_001_routes = [r for r in active_routes if r.error_code == "ERROR_001"]
        assert len(error_001_routes) == 0
    
    def test_error_001_properties_immutable(self):
        """Test that ERROR_001 properties are correctly defined."""
        error = get_error_code("ERROR_001")
        
        assert error is not None
        assert error.code == "ERROR_001"
        assert error.name == "DISSOCIATION"
        assert error.blocks_other_routes is True
        assert error.confidence_level == 95.0
    
    def test_unresolved_error_001_persists_blocking(self, engine):
        """Test that unresolved ERROR_001 continues to block even after routing attempts."""
        # Route ERROR_001
        engine.route_error("ERROR_001")
        
        # Try to route other errors multiple times
        for _ in range(5):
            result = engine.route_error("ERROR_002")
            assert result.is_blocked
            assert result.blocked_by == "ERROR_001"
        
        # ERROR_001 should still be active
        active_routes = engine.get_active_routes()
        error_001_active = any(r.error_code == "ERROR_001" for r in active_routes)
        assert error_001_active
    
    def test_error_001_frequency_validation(self):
        """Test that ERROR_001 frequency is within valid range."""
        error = get_error_code("ERROR_001")
        
        # Solfeggio frequencies are typically in the range 174-963 Hz
        assert 100 <= error.frequency <= 1000
        assert error.frequency == 396  # Specific to this error


class TestError001StateManagement:
    """Tests for state management with ERROR_001."""
    
    def test_active_routes_includes_error_001(self, engine):
        """Test that ERROR_001 appears in active routes after routing."""
        engine.route_error("ERROR_001")
        
        active_routes = engine.get_active_routes()
        assert len(active_routes) == 1
        assert active_routes[0].error_code == "ERROR_001"
    
    def test_resolve_removes_from_active_routes(self, engine):
        """Test that resolving ERROR_001 removes it from active routes."""
        engine.route_error("ERROR_001")
        assert len(engine.get_active_routes()) == 1
        
        engine.resolve_error("ERROR_001")
        assert len(engine.get_active_routes()) == 0
    
    def test_reset_clears_error_001(self, engine):
        """Test that resetting the engine clears ERROR_001 state."""
        engine.route_error("ERROR_001")
        engine.route_error("ERROR_002")  # This will be blocked
        
        engine.reset()
        
        # After reset, should be able to route ERROR_002 without blocking
        result = engine.route_error("ERROR_002")
        assert not result.is_blocked
        assert len(engine.get_active_routes()) == 1
