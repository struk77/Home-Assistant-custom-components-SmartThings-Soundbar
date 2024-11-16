import logging
import voluptuous as vol

from .api import SoundbarApi

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerDeviceClass,
    PLATFORM_SCHEMA,
)
from homeassistant.const import (
    CONF_NAME, CONF_API_KEY, CONF_DEVICE_ID
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "SmartThings Soundbar"
CONF_MAX_VOLUME = "max_volume"

SUPPORT_SMARTTHINGS_SOUNDBAR = (
        MediaPlayerEntityFeature.PAUSE
        | MediaPlayerEntityFeature.VOLUME_STEP
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.SELECT_SOURCE
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.PLAY
        | MediaPlayerEntityFeature.SELECT_SOUND_MODE
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_DEVICE_ID): cv.string,
        vol.Optional(CONF_MAX_VOLUME, default=1): cv.positive_int,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    api_key = config.get(CONF_API_KEY)
    device_id = config.get(CONF_DEVICE_ID)
    max_volume = config.get(CONF_MAX_VOLUME)
    add_entities([SmartThingsSoundbarMediaPlayer(name, api_key, device_id, max_volume)])


class SmartThingsSoundbarMediaPlayer(MediaPlayerEntity):

    def __init__(self, name, api_key, device_id, max_volume):
        self._name = name
        self._device_id = device_id
        self._api_key = api_key
        self._max_volume = max_volume
        self._volume = 1
        self._muted = False
        self._playing = True
        self._state = "on"
        self._source = ""
        self._source_list = []
        self._media_title = ""

    def update(self):
        SoundbarApi.device_update(self)

    @property
    def unique_id(self) -> str | None:
        return f"SmartThings_Soundbar_{self._device_id}"

    def turn_off(self):
        arg = ""
        cmdtype = "switch_off"
        SoundbarApi.send_command(self, arg, cmdtype)

    def turn_on(self):
        arg = ""
        cmdtype = "switch_on"
        SoundbarApi.send_command(self, arg, cmdtype)

    def set_volume_level(self, arg, cmdtype="setvolume"):
        SoundbarApi.send_command(self, arg, cmdtype)

    def mute_volume(self, mute, cmdtype="audiomute"):
        SoundbarApi.send_command(self, mute, cmdtype)

    def volume_up(self, cmdtype="stepvolume"):
        arg = "up"
        SoundbarApi.send_command(self, arg, cmdtype)

    def volume_down(self, cmdtype="stepvolume"):
        arg = ""
        SoundbarApi.send_command(self, arg, cmdtype)

    def select_source(self, source, cmdtype="selectsource"):
        SoundbarApi.send_command(self, source, cmdtype)

    def select_sound_mode(self, sound_mode):
        SoundbarApi.send_command(self, sound_mode, "selectsoundmode")

    @property
    def device_class(self):
        return MediaPlayerDeviceClass.SPEAKER

    @property
    def supported_features(self):
        return SUPPORT_SMARTTHINGS_SOUNDBAR

    @property
    def name(self):
        return self._name

    @property
    def media_title(self):
        return self._media_title

    def media_play(self):
        arg = ""
        cmdtype = "play"
        SoundbarApi.send_command(self, arg, cmdtype)

    def media_pause(self):
        arg = ""
        cmdtype = "pause"
        SoundbarApi.send_command(self, arg, cmdtype)

    @property
    def state(self):
        return self._state

    @property
    def is_volume_muted(self):
        return self._muted

    @property
    def volume_level(self):
        return self._volume

    @property
    def source(self):
        return self._source

    @property
    def source_list(self):
        return self._source_list
