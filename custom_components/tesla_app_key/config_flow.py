"""Config flow for Tesla App Key integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from homeassistant.helpers import selector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

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
        key_input = user_input[CONF_PUBLIC_KEY].strip()
        
        # specific fix for when line returns are stripped
        if "-----BEGIN PUBLIC KEY-----" in key_input and "\n" not in key_input:
             key_input = key_input.replace("-----BEGIN PUBLIC KEY-----", "-----BEGIN PUBLIC KEY-----\n")
             key_input = key_input.replace("-----END PUBLIC KEY-----", "\n-----END PUBLIC KEY-----")

        try:
             # Validate and normalize the key
             loaded_key = serialization.load_pem_public_key(
                 key_input.encode(), backend=default_backend()
             )
             
             # Re-serialize to ensures it matches the exact expected format
             pem_bytes = loaded_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
             )
             user_input[CONF_PUBLIC_KEY] = pem_bytes.decode('utf-8')
             
        except Exception:
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
