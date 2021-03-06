"""Offer sun based automation rules."""
from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.const import (
    CONF_EVENT,
    CONF_OFFSET,
    CONF_PLATFORM,
    SUN_EVENT_SUNRISE,
)
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.event import async_track_sunrise, async_track_sunset

# mypy: allow-untyped-defs, no-check-untyped-defs

_LOGGER = logging.getLogger(__name__)

TRIGGER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PLATFORM): "sun",
        vol.Required(CONF_EVENT): cv.sun_event,
        vol.Required(CONF_OFFSET, default=timedelta(0)): cv.time_period,
    }
)


async def async_attach_trigger(hass, config, action, automation_info):
    """Listen for events based on configuration."""
    event = config.get(CONF_EVENT)
    offset = config.get(CONF_OFFSET)
    description = event
    if offset:
        description = f"{description} with offset"

    @callback
    def call_action():
        """Call action with right context."""
        hass.async_run_job(
            action,
            {
                "trigger": {
                    "platform": "sun",
                    "event": event,
                    "offset": offset,
                    "description": description,
                }
            },
        )

    if event == SUN_EVENT_SUNRISE:
        return async_track_sunrise(hass, call_action, offset)
    return async_track_sunset(hass, call_action, offset)
