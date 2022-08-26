from __future__ import annotations

import logging

from .magichuecloud import MagichueCloud

import voluptuous as vol

from pprint import pformat

import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
  SUPPORT_BRIGHTNESS,
  SUPPORT_COLOR,
  PLATFORM_SCHEMA,
  ColorMode,
  LightEntity
)
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_LIGHTS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger("magichuecloud")

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
  vol.Optional(CONF_EMAIL): cv.string,
  vol.Optional(CONF_PASSWORD): cv.string,
  vol.Optional(CONF_LIGHTS): int,
})

def setup_platform(
  hass: HomeAssistant,
  config: ConfigType,
  add_entities: AddEntitiesCallback,
  discovery_info: DiscoveryInfoType | None = None
) -> None:
  _LOGGER.info(pformat(config))
    
  account = {
    "email": config[CONF_EMAIL],
    "password": config[CONF_PASSWORD]
  }

  light = []

  for i in range(0, config[CONF_LIGHTS]):
    light.append(MagichueLight(account, i-1, 'light'))

  add_entities(light)

class MagichueLight(LightEntity):
  def __init__(self, account, lightNumber, lightName) -> None:
    self._light = MagichueCloud(account["email"], account["password"], lightNumber)
    self._state = self._light.is_on()
    self._brightness = self._light.get_brightness()
    self._hs = self._light.get_hs()
    self._name = lightName

  @property
  def supported_features(self):
    return SUPPORT_BRIGHTNESS | SUPPORT_COLOR

  @property
  def name(self) -> str:
    return self._name

  @property
  def brightness(self):
    return self._brightness

  @property
  def hs_color(self):
    h, s = self._hs
    return h * 360, s * 100

  @property
  def is_on(self) -> bool | None:
    return self._state

  def turn_on(self, **kwargs: Any) -> None:
    if "brightness" in kwargs:
      brightness = kwargs.get(ColorMode.BRIGHTNESS, 255)
      self._light.set_brightness(brightness)

    if "hs_color" in kwargs:
      color = kwargs["hs_color"]
      self._light.set_hs(color[0]/360, color[1]/100)

    self._light.turn_on()

  def turn_off(self, **kwargs: Any) -> None:
    self._light.turn_off()

  def update(self) -> None:
    self._state = self._light.is_on()
    self._brightness = self._light.get_brightness()
    self._hs = self._light.get_hs()
