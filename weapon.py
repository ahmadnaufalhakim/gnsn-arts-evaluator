from constants import weapon as cnt

class Weapon(object) :
  count = 0
  def __init__(self, weapObj) -> None:
    self._key = weapObj["key"]
    self._name = cnt.key_to_name[self._key]
    self._level = weapObj["level"]
    self._ascension = weapObj["ascension"]
    self._refinement = weapObj["refinement"]
    self._location = weapObj["location"]
    self._weapon_type = cnt.weapons[self._key]["weapon_type"]
    self._star = cnt.weapons[self._key]["star"]
    self._type = cnt.weapons[self._key]["type"]
    self._substat = cnt.weapons[self._key]["substat"]
    Weapon.count += 1
    # # this id is for self development
    # self._id = f"weapon_{Weapon.count}"
    # this id is for GOOD format
    self._id = weapObj["id"]

  def __eq__(self, other) -> bool:
    self._id == other.id

  @property
  def key(self) :
    return self._key
  @key.setter
  def key(self, key) :
    self._key = key

  @property
  def name(self) :
    return self._name
  @name.setter
  def name(self, name) :
    self._name = name

  @property
  def level(self) :
    return self._level
  @level.setter
  def level(self, level) :
    self._level = level

  @property
  def ascension(self) :
    return self._ascension
  @ascension.setter
  def ascension(self, ascension) :
    self._ascension = ascension

  @property
  def refinement(self) :
    return self._refinement
  @refinement.setter
  def refinement(self, refinement) :
    self._refinement = refinement

  @property
  def location(self) :
    return self._location
  @location.setter
  def location(self, location) :
    self._location = location

  @property
  def weapon_type(self) :
    return self._weapon_type
  @weapon_type.setter
  def weapon_type(self, weapon_type) :
    self._weapon_type = weapon_type

  @property
  def star(self) :
    return self._star
  @star.setter
  def star(self, star) :
    self._star = star

  @property
  def type(self) :
    return self._type
  @type.setter
  def type(self, type) :
    self._type = type

  @property
  def substat(self) :
    return self._substat
  @substat.setter
  def substat(self, substat) :
    self._substat = substat

  @property
  def id(self) :
    return self._id

  @property
  def base_atk(self) :
    return cnt.type_to_base_atk[self._type]*cnt.level_multipliers[self._type][self._level-1] \
      + cnt.ascension_values[self._star][self._ascension]

  @property
  def substat_value(self) :
    return cnt.type_to_substat_base_values[self._type][self._substat]*cnt.substat_level_multipliers[self._level//5]

  @property
  def substat(self) :
    return self._substat
  @substat.setter
  def substat(self, substat) :
    self._substat = substat

def default_weapon_obj(character_key, weapon_type) : 
  weapon_type_to_default_weapon = {
    "bow": {
      "key": "HuntersBow",
      "level": 1,
      "ascension": 0,
      "refinement": 1,
      "location": character_key
    },
    "catalyst": {
      "key": "ApprenticesNotes",
      "level": 1,
      "ascension": 0,
      "refinement": 1,
      "location": character_key
    },
    "claymore": {
      "key": "WasterGreatsword",
      "level": 1,
      "ascension": 0,
      "refinement": 1,
      "location": character_key
    },
    "polearm": {
      "key": "BeginnersProtector",
      "level": 1,
      "ascension": 0,
      "refinement": 1,
      "location": character_key
    },
    "sword": {
      "key": "DullBlade",
      "level": 1,
      "ascension": 0,
      "refinement": 1,
      "location": character_key
    }
  }
  return weapon_type_to_default_weapon[weapon_type]
