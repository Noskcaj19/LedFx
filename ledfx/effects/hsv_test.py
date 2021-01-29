import voluptuous as vol

from ledfx.effects.audio import AudioReactiveEffect
from ledfx.effects.hsv_effect import HSVEffect


class HSVTest(AudioReactiveEffect, HSVEffect):

    NAME = "HSV Test"
    CONFIG_SCHEMA = vol.Schema(
        {
            vol.Optional(
                "speed",
                description="Effect Speed",
                default=0.1,
            ): vol.All(vol.Coerce(float), vol.Range(min=0.00001, max=1.0)),
        }
    )

    lows_power = 0

    def config_updated(self, config):
        self._p_filter = self.create_filter(alpha_decay=0.2, alpha_rise=0.2)

    def audio_data_updated(self, data):
        self._dirty = True
        self.lows_power = self._p_filter.update(
            min(data.melbank_lows().max(), 1)
        )

    def render(self):
        # "Global expression"

        t1 = self.time(self._config["speed"])

        # "Pixel expression"
        for i in range(self.pixel_count):
            v = self.triangle(
                (2.0 * self.sin(t1) + i / self.pixel_count) % 1.0
            )
            v **= 5.0
            s = v < 0.9
            self.hsv_array[i] = (self.lows_power, s, v)