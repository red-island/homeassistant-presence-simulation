"""Config flow for Presence Simulator integration."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_AUTOMATIONS,
    CONF_AWAY_TOGGLE,
    CONF_LIGHTS,
    DOMAIN,
    EXTRA_VALIDATION,
    NONE_STR,
    VALIDATION_TUPLES,
)
from .switch import _supported_features, validate

# from typing import Any


# from homeassistant.data_entry_flow import FlowResult

# from homeassistant.exceptions import HomeAssistantError
# from homeassistant.helpers.selector import selector

_LOGGER = logging.getLogger(__name__)


class PresenceSimulatorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Presence Simulator."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_NAME])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_NAME): str}),
            errors=errors,
        )

    async def async_step_import(self, user_input=None) -> FlowResult:
        """Handle configuration by YAML file."""

        await self.async_set_unique_id(user_input[CONF_NAME])
        for config_entry in self._async_current_entries():
            if config_entry.unique_id == self.unique_id:
                self.hass.config_entries.async_update_entry(
                    config_entry, data=user_input
                )
                self._abort_if_unique_id_configured()
        return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlowHandler:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


def validate_options(user_input, errors):
    """Validate the options in the OptionsFlow. This is an extra validation step because the validators in `EXTRA_VALIDATION` cannot be serialized to json."""
    for key, (_validate, _) in EXTRA_VALIDATION.items():
        # these are unserializable validators
        value = user_input.get(key)
        try:
            if value is not None and value != NONE_STR:
                _validate(value)
        except vol.Invalid:
            _LOGGER.exception("Configuration option %s=%s is incorrect", key, value)
            errors["base"] = "option_error"


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a option flow for Presence Simulator."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Handle options flow."""
        conf = self.config_entry
        data = validate(conf)
        if conf.source == config_entries.SOURCE_IMPORT:
            return self.async_show_form(step_id="init", data_schema=None)

        errors: dict[str, str] = {}
        if user_input is not None:
            validate_options(user_input, errors)
            if not errors:
                return self.async_create_entry(title="", data=user_input)

        # automations
        all_automation = self.hass.states.async_entity_ids("automation")
        for configured_automation in data[CONF_AUTOMATIONS]:
            if configured_automation not in all_automation:
                errors = {CONF_AUTOMATIONS: "entity_missing"}
                _LOGGER.error(
                    "%s: automation entity %s is configured, but was not found",
                    data[CONF_NAME],
                    configured_automation,
                )

        # lights
        all_lights = [
            light
            for light in self.hass.states.async_entity_ids("light")
            if _supported_features(self.hass, light)
        ]
        for configured_light in data[CONF_LIGHTS]:
            if configured_light not in all_lights:
                errors = {CONF_LIGHTS: "entity_missing"}
                _LOGGER.error(
                    "%s: light entity %s is configured, but was not found",
                    data[CONF_NAME],
                    configured_light,
                )
        all_lights.append("configured_light")
        all_lights.append("configured_light2")
        all_lights.append("configured_light3")
        all_lights.append("configured_light4")
        all_lights.append("configured_light5")
        all_lights.append("configured_light6")
        all_lights.append("configured_light7")
        all_lights.append("configured_light8")
        all_lights.append("configured_light9")

        # toggles
        all_toggles = self.hass.states.async_entity_ids("input_boolean")

        to_replace = {
            CONF_AWAY_TOGGLE: cv.multi_select(sorted(all_toggles)),
            CONF_AUTOMATIONS: cv.multi_select(sorted(all_automation)),
            CONF_LIGHTS: cv.multi_select(sorted(all_lights)),
        }

        options_schema = {}
        for name, default, validation in VALIDATION_TUPLES:
            key = vol.Optional(name, default=conf.options.get(name, default))
            value = to_replace.get(name, validation)
            options_schema[key] = value

        return self.async_show_form(
            step_id="init", data_schema=vol.Schema(options_schema), errors=errors
        )
