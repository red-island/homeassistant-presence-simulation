"""Event parser and human readable log generator."""
from __future__ import annotations

from datetime import datetime as dt
import logging

from homeassistant.components.logbook.helpers import (
    async_determine_event_types,
    async_filter_entities,
)
from homeassistant.components.logbook.processor import EventProcessor
from homeassistant.components.recorder import get_instance
from homeassistant.core import HomeAssistant
import homeassistant.util.dt as dt_util

_LOGGER = logging.getLogger(__name__)


async def get_events(
    hass: HomeAssistant,
    start_time: dt,
    end_time: dt,
    # device_ids: list[str],
    entity_ids: list[str],
    context_id: str | None,
):
    """Handle logbook get events command."""

    device_ids: list[str] = []
    utc_now = dt_util.utcnow()

    if start_time > utc_now:
        _LOGGER.error("Start time in future")
        return

    if start_time > end_time:
        _LOGGER.error("Start time after end time")
        return

    if entity_ids:
        entity_ids = async_filter_entities(hass, entity_ids)
        if not entity_ids and not device_ids:
            # Everything has been filtered away
            _LOGGER.debug("No entity_ids and no device_ids left after filtering")
            return

    event_types = async_determine_event_types(hass, entity_ids, device_ids)

    event_processor = EventProcessor(
        hass,
        event_types,
        entity_ids,
        device_ids,
        context_id,
        timestamp=True,
        include_entity_name=False,
    )

    return await get_instance(hass).async_add_executor_job(
        _formatted_get_events,
        0,
        start_time,
        end_time,
        event_processor,
    )


def _formatted_get_events(
    msg_id: int,
    start_time: dt,
    end_time: dt,
    event_processor: EventProcessor,
):
    """Fetch events and convert them to json in the executor."""
    return event_processor.get_events(start_time, end_time)
