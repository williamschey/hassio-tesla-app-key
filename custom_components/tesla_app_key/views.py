"""View to serve the Tesla Public Key."""
from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .const import URL_PATH

class TeslaPublicKeyView(HomeAssistantView):
    """View to serve the Tesla Public Key."""

    requires_auth = False
    url = URL_PATH
    name = "tesla_app_key:public_key"

    def __init__(self, public_key: str) -> None:
        """Initialize the view."""
        self._public_key = public_key

    async def get(self, request: web.Request) -> web.Response:
        """Handle GET request."""
        return web.Response(text=self._public_key, content_type="application/x-pem-file")
