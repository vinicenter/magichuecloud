import sys
sys.path.insert(1, '/config/custom_components/magichuecloud/python-magichue-0.3.2')

import magichue

class MagichueCloud:
  def __init__(self, user, password, lightNumber) -> None:
    self._user = user
    self._password = password
    self._api = magichue.RemoteAPI.login_with_user_password(
      user=self._user,
      password=self._password
    )
    self._light = self._api.get_online_bulbs()[lightNumber]

  def is_on(self):
    return self._light.on

  def turn_on(self):
    self._light.on = True

  def turn_off(self):
    self._light.on = False

  def get_brightness(self):
    return self._light.brightness

  def set_brightness(self, v):
    self._light.brightness = v

  def get_rgb(self):
    return self._light.rgb

  def set_rgb(self, rgb):
    self._light.rgb = rgb
  
  def get_hs(self):
    return self._light.hue, self._light.saturation
  
  def set_hs(self, h, s):
    self._light.hue = h
    self._light.saturation = s

