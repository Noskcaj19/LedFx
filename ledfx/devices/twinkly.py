import logging
import xled.control

import numpy as np
import voluptuous as vol

from ledfx.devices import NetworkedDevice

from itertools import zip_longest

BYTES_PER_PIXEL = 4


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

_LOGGER = logging.getLogger(__name__)


class TwinklyCurtainDevice(NetworkedDevice):
    """Twinkly Curtain device support"""

    CONFIG_SCHEMA = vol.Schema(
        {
            vol.Required(
                "name", description="Friendly name for the device"
            ): str,
            vol.Required(
                "pixel_count",
                description="Number of individual pixels",
            ): vol.All(vol.Coerce(int), vol.Range(min=1)),
            vol.Optional(
                "hw_address",
                description="MAC address of the device",
            ): str,
        }
    )

    def activate(self):
        self._control = xled.control.ControlInterface(self._config["ip_address"], self._config["hw_address"])
        self._rtc = realtime.RealtimeChannel(control, self._config["pixel_count"], BYTES_PER_PIXEL)
        self._rtc.start_realtime()
        _LOGGER.info(f"xled rt control for {self.config['name']} created.")
        super().activate()

    def deactivate(self):
        self._rtc.send_frame(bytes(BYTES_PER_PIXEL * self._config["pixel_count"] * [0]))
        super().deactivate()
        _LOGGER.info(f"xled rt control for {self.config['name']} stopped.")
        self._control = None
        self._rtc = None

    def flush(self, data):
        wrgb_pixels = [[0, *p] for p in utils.grouper(data, 3, 0)]
        self._rtc.send_frame(wrgb_pixels)