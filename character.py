import re
from typing import Union
from weapon import Weapon, default_weapon_obj
from artifact import Artifact
from constants import character as cnt

class Character(object) :
  def __init__(self, charObj) -> None:
    self._key = charObj["key"]
    self._name = ' '.join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', self._key)).split())
    self._level = charObj["level"]
    self._ascension = charObj["ascension"]
    self._constellation = charObj["constellation"]
    self._base_hp = cnt.characters[self._key]["base_hp"]
    self._base_atk = cnt.characters[self._key]["base_atk"]
    self._base_def = cnt.characters[self._key]["base_def"]
    self._star = cnt.characters[self._key]["star"]
    self._element = cnt.characters[self._key]["element"]
    self._special_stat = cnt.characters[self._key]["special_stat"]
    self._weapon_type = cnt.characters[self._key]["weapon_type"]
    self._weapon = Weapon(default_weapon_obj(self._key, self._weapon_type))
    self._artifacts = {
      "flower": None,
      "plume": None,
      "sands": None,
      "goblet": None,
      "circlet": None
    }

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
  def constellation(self) :
    return self._constellation
  @constellation.setter
  def constellation(self, constellation) :
    self._constellation = constellation

  @property
  def base_hp(self) :
    return self._base_hp
  @base_hp.setter
  def base_hp(self, base_hp) :
    self._base_hp = base_hp

  @property
  def base_atk(self) :
    return self._base_atk
  @base_atk.setter
  def base_atk(self, base_atk) :
    self._base_atk = base_atk

  @property
  def base_def(self) :
    return self._base_def
  @base_def.setter
  def base_def(self, base_def) :
    self._base_def = base_def

  @property
  def star(self) :
    return self._star
  @star.setter
  def star(self, star) :
    self._star = star

  @property
  def element(self) :
    return self._element
  @element.setter
  def element(self, element) :
    self._element = element

  @property
  def special_stat(self) :
    return self._special_stat
  @special_stat.setter
  def special_stat(self, special_stat) :
    self._special_stat = special_stat

  @property
  def weapon_type(self) :
    return self._weapon_type
  @weapon_type.setter
  def weapon_type(self, weapon_type) :
    self._weapon_type = weapon_type

  @property
  def weapon(self) :
    return self._weapon
  @weapon.setter
  def weapon(self, weapon: Weapon) :
    print(self._weapon.location, weapon.location)
    if self._weapon_type != weapon.weapon_type :
      raise Exception(f"Character's weapon type doesn't match: {self._weapon_type}({self._key}) != {weapon.weapon_type}({weapon._key})")
    if self._weapon.location != weapon.location :
      self._weapon.location, weapon.location = weapon.location, self._weapon.location
    else :
      self._weapon.location, weapon.location = '', self._key
    self._weapon = weapon

  @property
  def artifacts(self) :
    return self._artifacts
  @artifacts.setter
  def artifacts(self, val) :
    try :
      slot_key, artifact: Union[Artifact, None] = val
    except Exception as e :
      raise e
    if artifact is not None :
      if slot_key != artifact.slot_key :
        raise Exception(f"Artifact slot key doesn't match: {slot_key} != {artifact.slot_key}")
      if self._artifacts[slot_key] is not None :
        if self._artifacts[slot_key].location != artifact.location :
          self._artifacts[slot_key].location, artifact.location = artifact.location, self._artifacts[slot_key].location
        else :
          self._artifacts[slot_key].location, artifact.location = '', self._key
      else :
        artifact.location = self._key
    else :
      if self._artifacts[slot_key] is not None :
        self._artifacts[slot_key].location = ''
    self._artifacts[slot_key] = artifact

  @property
  def hp(self) :
    char_hp = \
      self._base_hp*cnt.level_multipliers[self._star][self._level-1] \
      + cnt.ascension_phase_to_total_section[self._ascension]*cnt.max_ascension_values[self._key]["hp"] \
      + (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
        if self._special_stat == "hp" else 0)
    weap_hp = (self._weapon.substat_value if self._weapon.substat == "hp" else 0)
    art_hp, art_hp_flat = 0, 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "hp%" in artifact.stat_values :
          art_hp += artifact.stat_values["hp%"]
        if "hp" in artifact.stat_values :
          art_hp_flat += artifact.stat_values["hp"]
    # print(f"HP: {char_hp}*(1 + {weap_hp} + {art_hp}) + {art_hp_flat}")
    hp = char_hp*(1 + weap_hp + art_hp) + art_hp_flat
    #TODO: add from art set bonus
    return hp

  @property
  def atk(self) :
    base_atk = \
      self._base_atk*cnt.level_multipliers[self._star][self._level-1] \
      + cnt.ascension_phase_to_total_section[self._ascension]*cnt.max_ascension_values[self._key]["atk"] \
      + (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
        if self._special_stat == "atk" else 0) \
      + self._weapon.base_atk
    weap_atk = (self._weapon.substat_value if self._weapon.substat == "atk" else 0)
    art_atk, art_atk_flat = 0, 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "atk%" in artifact.stat_values :
          art_atk += artifact.stat_values["atk%"]
        if "atk" in artifact.stat_values :
          art_atk_flat += artifact.stat_values["atk"]
    # print(f"ATK: {base_atk}*(1 + {weap_atk} + {art_atk}) + {art_atk_flat}")
    atk = base_atk*(1 + weap_atk + art_atk) + art_atk_flat
    #TODO: add from art set bonus
    return atk

  @property
  def defense(self) :
    char_def = \
      self._base_def*cnt.level_multipliers[self._star][self._level-1] \
      + cnt.ascension_phase_to_total_section[self._ascension]*cnt.max_ascension_values[self._key]["def"] \
      + (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
        if self._special_stat == "def" else 0)
    weap_def = (self._weapon.substat_value if self._weapon.substat == "def" else 0)
    art_def, art_def_flat = 0, 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "def%" in artifact.stat_values :
          art_def += artifact.stat_values["def%"]
        if "def" in artifact.stat_values :
          art_def_flat += artifact.stat_values["def"]
    # print(f"DEF: {char_def}*(1 + {weap_def} + {art_def}) + {art_def_flat}")
    defense = char_def*(1 + weap_def + art_def) + art_def_flat
    #TODO: add from art set bonus
    return defense

  @property
  def em(self) :
    char_em = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "em" else 0)
    weap_em = (self._weapon.substat_value if self._weapon.substat == "em" else 0)
    art_em = 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "em" in artifact.stat_values :
          art_em += artifact.stat_values["em"]
    # print(f"EM: {char_em} + {weap_em} + {art_em}")
    em = char_em + weap_em + art_em
    #TODO: add from art set bonus
    return em

  @property
  def crit_rate(self) :
    char_crit_rate = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "crit_rate" else 0) \
      + (-1 if self._key == "SangonomiyaKokomi" else 0)
    weap_crit_rate = (self._weapon.substat_value if self._weapon.substat == "crit_rate" else 0)
    art_crit_rate = 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "crit_rate" in artifact.stat_values :
          art_crit_rate += artifact.stat_values["crit_rate"]
    # print(f"CRIT Rate: {char_crit_rate} + .05 + {weap_crit_rate} + {art_crit_rate}")
    crit_rate = char_crit_rate + .05 + weap_crit_rate + art_crit_rate
    #TODO: add from art set bonus
    return 0 if crit_rate <= 0 else crit_rate if 0 < crit_rate < 1 else 1

  @property
  def crit_dmg(self) :
    char_crit_dmg = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "crit_dmg" else 0)
    weap_crit_dmg = (self._weapon.substat_value if self._weapon.substat == "crit_dmg" else 0)
    art_crit_dmg = 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "crit_dmg" in artifact.stat_values :
          art_crit_dmg += artifact.stat_values["crit_dmg"]
    # print(f"CRIT DMG: {char_crit_dmg} + .5 + {weap_crit_dmg} + {art_crit_dmg}")
    crit_dmg = char_crit_dmg + .5 + weap_crit_dmg + art_crit_dmg
    #TODO: add from art set bonus
    return crit_dmg

  @property
  def healing_bonus(self) :
    char_healing_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "healing_bonus" else 0)
    art_healing_bonus = 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "healing_bonus" in artifact.stat_values :
          art_healing_bonus += artifact.stat_values["healing_bonus"]
    # print(f"Healing Bonus: {char_healing_bonus} + {art_healing_bonus}")
    healing_bonus = char_healing_bonus + art_healing_bonus
    #TODO: add from art set bonus
    return healing_bonus

  @property
  def er(self) :
    char_er = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "er" else 0)
    weap_er = (self._weapon.substat_value if self._weapon.substat == "er" else 0)
    art_er = 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "er" in artifact.stat_values :
          art_er += artifact.stat_values["er"]
    # print(f"ER: {char_er} + 1 + {weap_er} + {art_er}")
    er = char_er + 1 + weap_er + art_er
    #TODO: add from art set bonus
    return er

  @property
  def pyro_dmg_bonus(self) :
    char_pyro_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "elemental_dmg_bonus" and self._element == "pyro" else 0)
    art_pyro_dmg_bonus = 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "pyro_dmg_bonus" in artifact.stat_values :
          art_pyro_dmg_bonus += artifact.stat_values["pyro_dmg_bonus"]
    # print(f"Pyro DMG Bonus: {char_pyro_dmg_bonus} + {art_pyro_dmg_bonus}")
    pyro_dmg_bonus = char_pyro_dmg_bonus + art_pyro_dmg_bonus
    #TODO: add from art set bonus
    return pyro_dmg_bonus

  @property
  def hydro_dmg_bonus(self) :
    char_hydro_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "elemental_dmg_bonus" and self._element == "hydro" else 0)
    art_hydro_dmg_bonus = 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "hydro_dmg_bonus" in artifact.stat_values :
          art_hydro_dmg_bonus += artifact.stat_values["hydro_dmg_bonus"]
    # print(f"Hydro DMG Bonus: {char_hydro_dmg_bonus} + {art_hydro_dmg_bonus}")
    hydro_dmg_bonus = char_hydro_dmg_bonus + art_hydro_dmg_bonus
    #TODO: add from art set bonus
    return hydro_dmg_bonus

  @property
  def dendro_dmg_bonus(self) :
    char_dendro_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "elemental_dmg_bonus" and self._element == "dendro" else 0)
    art_dendro_dmg_bonus = 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "dendro_dmg_bonus" in artifact.stat_values :
          art_dendro_dmg_bonus += artifact.stat_values["dendro_dmg_bonus"]
    # print(f"Dendro DMG Bonus: {char_dendro_dmg_bonus} + {art_dendro_dmg_bonus}")
    dendro_dmg_bonus = char_dendro_dmg_bonus + art_dendro_dmg_bonus
    #TODO: add from art set bonus
    return dendro_dmg_bonus

  @property
  def electro_dmg_bonus(self) :
    char_electro_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "elemental_dmg_bonus" and self._element == "electro" else 0)
    art_electro_dmg_bonus = 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "electro_dmg_bonus" in artifact.stat_values :
          art_electro_dmg_bonus += artifact.stat_values["electro_dmg_bonus"]
    # print(f"Electro DMG Bonus: {char_electro_dmg_bonus} + {art_electro_dmg_bonus}")
    electro_dmg_bonus = char_electro_dmg_bonus + art_electro_dmg_bonus
    #TODO: add from art set bonus
    return electro_dmg_bonus

  @property
  def anemo_dmg_bonus(self) :
    char_anemo_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "elemental_dmg_bonus" and self._element == "anemo" else 0)
    art_anemo_dmg_bonus = 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "anemo_dmg_bonus" in artifact.stat_values :
          art_anemo_dmg_bonus += artifact.stat_values["anemo_dmg_bonus"]
    # print(f"Anemo DMG Bonus: {char_anemo_dmg_bonus} + {art_anemo_dmg_bonus}")
    anemo_dmg_bonus = char_anemo_dmg_bonus + art_anemo_dmg_bonus
    #TODO: add from art set bonus
    return anemo_dmg_bonus

  @property
  def cryo_dmg_bonus(self) :
    char_cryo_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "elemental_dmg_bonus" and self._element == "cryo" else 0)
    art_cryo_dmg_bonus = 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "cryo_dmg_bonus" in artifact.stat_values :
          art_cryo_dmg_bonus += artifact.stat_values["cryo_dmg_bonus"]
    # print(f"Cryo DMG Bonus: {char_cryo_dmg_bonus} + {art_cryo_dmg_bonus}")
    cryo_dmg_bonus = char_cryo_dmg_bonus + art_cryo_dmg_bonus
    #TODO: add from art set bonus
    return cryo_dmg_bonus

  @property
  def geo_dmg_bonus(self) :
    char_geo_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "elemental_dmg_bonus" and self._element == "geo" else 0)
    art_geo_dmg_bonus = 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "geo_dmg_bonus" in artifact.stat_values :
          art_geo_dmg_bonus += artifact.stat_values["geo_dmg_bonus"]
    # print(f"Geo DMG Bonus: {char_geo_dmg_bonus} + {art_geo_dmg_bonus}")
    geo_dmg_bonus = char_geo_dmg_bonus + art_geo_dmg_bonus
    #TODO: add from art set bonus
    return geo_dmg_bonus

  @property
  def elemental_dmg_bonus(self) :
    if self._element == "pyro" :
      return self.pyro_dmg_bonus
    if self._element == "hydro" :
      return self.hydro_dmg_bonus
    if self._element == "dendro" :
      return self.dendro_dmg_bonus
    if self._element == "electro" :
      return self.electro_dmg_bonus
    if self._element == "anemo" :
      return self.anemo_dmg_bonus
    if self._element == "cryo" :
      return self.cryo_dmg_bonus
    if self._element == "geo" :
      return self.geo_dmg_bonus

  @property
  def physical_dmg_bonus(self) :
    char_physical_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "physical_dmg_bonus" else 0)
    weap_physical_dmg_bonus = (self._weapon.substat_value if self._weapon.substat == "physical_dmg_bonus" else 0)
    art_physical_dmg_bonus = 0
    for artifact in self._artifacts.values() :
      if artifact is not None :
        if "physical_dmg_bonus" in artifact.stat_values :
          art_physical_dmg_bonus += artifact.stat_values["physical_dmg_bonus"]
    # print(f"Physical DMG Bonus: {char_physical_dmg_bonus} + {weap_physical_dmg_bonus} + {art_physical_dmg_bonus}")
    physical_dmg_bonus = char_physical_dmg_bonus + weap_physical_dmg_bonus + art_physical_dmg_bonus
    #TODO: add from art set bonus
    return physical_dmg_bonus
