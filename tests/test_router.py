import pytest
from app.routing.query_router import query_router
from app.routing.route_types import RouteDestination

def test_sensitive_query_routes_to_local():
    decision = query_router.route_query("Summarize my private project document.")
    assert decision.route == RouteDestination.LOCAL
    assert "project_database" in decision.allowed_tools

def test_general_query_routes_to_external():
    decision = query_router.route_query("What is the speed of light?")
    assert decision.route == RouteDestination.EXTERNAL
    assert "weather" in decision.allowed_tools
