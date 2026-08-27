from app.routing.route_types import RouteDestination, RoutingDecision
from app.security.privacy_gate import privacy_gate
from app.security.permissions import ALLOWED_LOCAL_TOOLS, ALLOWED_EXTERNAL_TOOLS

class QueryRouter:
    def route_query(self, query: str) -> RoutingDecision:
        is_sensitive, reason = privacy_gate.evaluate(query)

        if is_sensitive:
            return RoutingDecision(
                route=RouteDestination.LOCAL,
                reason=reason,
                confidence=1.0,
                allowed_tools=list(ALLOWED_LOCAL_TOOLS)
            )

        return RoutingDecision(
            route=RouteDestination.EXTERNAL,
            reason="Public/General knowledge request; safe for external execution",
            confidence=0.95,
            allowed_tools=list(ALLOWED_EXTERNAL_TOOLS)
        )

query_router = QueryRouter()