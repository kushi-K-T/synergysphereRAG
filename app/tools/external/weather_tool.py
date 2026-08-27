import httpx
from typing import Dict, Any
from app.tools.base_tool import BaseTool

class WeatherTool(BaseTool):
    @property
    def name(self) -> str:
        return "weather"

    @property
    def description(self) -> str:
        return "Fetches public weather updates."

    @property
    def is_internal(self) -> bool:
        return False

    async def execute(self, location: str = "London", **kwargs) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(f"https://wttr.in/{location}?format=j1")
                if res.status_code == 200:
                    data = res.json()
                    current = data["current_condition"][0]
                    return {
                        "location": location,
                        "temperature_C": current["temp_C"],
                        "condition": current["weatherDesc"][0]["value"]
                    }
        except Exception:
            pass
        return {"location": location, "temperature_C": "21", "condition": "Partly Cloudy (Mock Fallback)"}