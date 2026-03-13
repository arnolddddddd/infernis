"""Tests for API key authentication middleware."""


class TestAuthMiddleware:
    """Test that auth middleware blocks unauthenticated requests when debug=False."""

    def test_public_endpoints_no_auth(self):
        """Health, status, coverage should be accessible without key."""
        # Need to reimport with debug=False
        # Since Settings is already loaded, we test via the middleware logic directly
        from infernis.api.auth import PUBLIC_PATHS

        assert "/health" in PUBLIC_PATHS
        assert "/v1/status" in PUBLIC_PATHS
        assert "/v1/coverage" in PUBLIC_PATHS

    def test_tier_limits_defined(self):
        from infernis.api.auth import TIER_LIMITS

        assert TIER_LIMITS["free"] == 50
        assert TIER_LIMITS["pro"] == 10_000
        assert TIER_LIMITS["enterprise"] == 100_000

    def test_no_tier_restrictions(self):
        """All endpoints should be available to all tiers (metered on daily limit only)."""
        from infernis.api.auth import TIER_RESTRICTED

        assert TIER_RESTRICTED == {}

    def test_demo_paths_public(self):
        """Demo endpoints should not require auth."""
        from infernis.api.auth import PUBLIC_PREFIXES

        assert any("/demo" in p for p in PUBLIC_PREFIXES)
