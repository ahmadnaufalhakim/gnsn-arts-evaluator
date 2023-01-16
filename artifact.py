from constants import artifact as cnt

artifacts = {}

class Artifact(object) :
  count = 0
  def __init__(self, artObj) -> None :
    self._set_key = artObj["setKey"]
    self._set_name = cnt.set_key_to_set_name[self._set_key]
    self._slot_key = artObj["slotKey"]
    self._name = cnt.set_key_to_name[self._slot_key][self._set_key]
    self._level = artObj["level"]
    self._star = artObj["rarity"]
    self._main_stat = cnt.good_stat_key_to_main_stat[artObj["mainStatKey"]]
    self._substats = []
    for substat in artObj["substats"] :
      self._substats.append({
        "key": cnt.good_stat_key_to_main_stat[substat["key"]] if substat["key"] in cnt.good_stat_key_to_main_stat else substat["key"],
        "value": substat["value"]/100 if len(substat["key"]) > 0 and substat["key"][-1] == '_' else substat["value"]
      })
    self._location = artObj["location"]
    Artifact.count += 1
    # # this id is for self development
    # self._id = f"artifact_{Artifact.count}"
    # this id is for GOOD format
    self._id = artObj["id"]
    artifacts[self._id] = self

  def __eq__(self, other) -> bool :
    return self._id == other.id

  # Returns sum of stat values of two artifacts
  def __add__(self, other: dict) -> dict :
    return {key: self.stat_values.get(key) + other.get(key) for key in set(self.stat_values)}

  # Returns first artifact's stat values for the first addition
  def __radd__(self, other) :
    if other == 0 :
      return self.stat_values
    elif type(other) == dict :
      return self.__add__(other)

  def __str__(self) -> str:
    return self._id

  def __repr__(self) -> str:
    return self._id

  @property
  def set_key(self) :
    return self._set_key
  @set_key.setter
  def set_key(self, set_key) :
    self._set_key = set_key

  @property
  def set_name(self) :
    return self._set_name
  @set_name.setter
  def set_name(self, set_name) :
    self._set_name = set_name

  @property
  def slot_key(self) :
    return self._slot_key
  @slot_key.setter
  def slot_key(self, slot_key) :
    self._slot_key = slot_key

  @property
  def level(self) :
    return self._level
  @level.setter
  def level(self, level) :
    self._level = level

  @property
  def star(self) :
    return self._star
  @star.setter
  def star(self, star) :
    self._star = star

  @property
  def main_stat(self) :
    return self._main_stat
  @main_stat.setter
  def main_stat(self, main_stat) :
    self._main_stat = main_stat

  @property
  def substats(self) :
    return self._substats
  @substats.setter
  def substats(self, substats) :
    self._substats = substats

  @property
  def location(self) :
    return self._location
  @location.setter
  def location(self, location) :
    self._location = location

  @property
  def id(self) :
    return self._id

  @property
  def stat_values(self) :
    res = cnt.zero_stat_values.copy()
    res[self._main_stat] += cnt.main_stat_values[self._star][self._main_stat][self._level]
    for substat in self._substats :
      if substat["key"] in res :
        res[substat["key"]] += substat["value"]
    return res

zero_stat_values = cnt.zero_stat_values
set_key_to_set_bonus = cnt.set_key_to_set_bonus
