from ledfx.effects.audio import AudioReactiveEffect
from ledfx.effects.gradient import GradientEffect
import voluptuous as vol
import numpy as np


class PowerAudioEffect(AudioReactiveEffect, GradientEffect):

    NAME = "Power"

    # There is no additional configuration here, but override the blur
    # default to be 3.0 so blurring is enabled.
    CONFIG_SCHEMA = vol.Schema({
        vol.Optional('blur', description='Amount to blur the effect', default = 3.0): vol.All(vol.Coerce(float), vol.Range(min=0.0, max=10))
    })

    def config_updated(self, config):

        # Create the filters used for the effect
        self._r_filter = self.create_filter(
            alpha_decay = 0.2,
            alpha_rise = 0.99)

        self._bass_filter = self.create_filter(
            alpha_decay = 0.1,
            alpha_rise = 0.99)

    def audio_data_updated(self, data):

        # Grab the filtered and interpolated melbank data
        y = data.interpolated_melbank(self.pixel_count, filtered = False)
        filtered_y = data.interpolated_melbank(self.pixel_count, filtered = True)

        # Grab the filtered difference between the filtered melbank and the
        # raw melbank.
        r = self._r_filter.update(y - filtered_y)

        # Apply the melbank data to the gradient curve
        out = self.apply_gradient(r)

        # Get bass power through filter
        bass = np.max(data.melbank_lows()) * (1/5)
        bass = self._bass_filter.update(bass)
        # Grab corresponding color
        color = self.get_gradient_color(bass)
        # Map it to the length of the strip and apply it
        bass_idx = int(bass * self.pixel_count)
        out[:bass_idx] = color

        onsets = data.onset()

        # Update the pixels
        self.pixels = out


