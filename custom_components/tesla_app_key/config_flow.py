"""Config flow for Tesla App Key integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from homeassistant.helpers import selector

from .const import CONF_PUBLIC_KEY, DOMAIN

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tesla App Key."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_PUBLIC_KEY): selector.TextSelector(
                            selector.TextSelectorConfig(multiline=True)
                        ),
                    }
                ),
            )

        # Basic validation: Check if it looks like a PEM key
        key = user_input[CONF_PUBLIC_KEY]
        if "-----BEGIN" not in key or "-----END" not in key:
             return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_PUBLIC_KEY): selector.TextSelector(
                            selector.TextSelectorConfig(multiline=True)
                        ),
                    }
                ),
                errors={"base": "invalid_pem"},
            )
        
        await self.async_set_unique_id("tesla_app_key_unique_id")
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title="Tesla App Key", data=user_input)
