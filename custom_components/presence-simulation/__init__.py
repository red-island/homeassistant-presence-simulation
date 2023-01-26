"""The Presence Simulator integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_SOURCE, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, UNDO_UPDATE_LISTENER

# List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.SWITCH]

# Logger
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Import integration from YAML config."""

    if DOMAIN in config:
        for entry in config[DOMAIN]:
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    DOMAIN, context={CONF_SOURCE: SOURCE_IMPORT}, data=entry
                )
            )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Presence Simulator using config flow."""
    _LOGGER.debug("async setup entry")

    hass.data.setdefault(DOMAIN, {})

    data = hass.data.setdefault(DOMAIN, {})
    update_listener = entry.add_update_listener(async_update_options)
    data[entry.entry_id] = {UNDO_UPDATE_LISTENER: update_listener}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_update_options(hass, entry: ConfigEntry):
    """Reload component after options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
