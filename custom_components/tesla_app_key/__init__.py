"""The Tesla App Key integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_PUBLIC_KEY, DOMAIN
from .views import TeslaPublicKeyView

PLATFORMS: list[str] = []

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Tesla App Key from a config entry."""
    
    public_key = entry.data[CONF_PUBLIC_KEY]
    
    # Register the view
    hass.http.register_view(TeslaPublicKeyView(public_key))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # We cannot easily unregister a view in HA, but since this is a global singleton path
    # practically speaking, it's fine. If the user removes the integration, the path will still exist
    # until restart unless we wanted to monkeypatch the view registry which is risky.
    # For now, we just return True.
    return True
