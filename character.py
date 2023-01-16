from collections import Counter
import re
from weapon import (
  Weapon,
  default_weapon
)
from artifact import (
  Artifact,
  zero_stat_values,
  set_key_to_set_bonus
)
from constants import character as cnt

characters = {}

class Character(object) :
  count = 0
  def __init__(self, charObj) -> None :
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
    self._weapon = default_weapon(self._key, self._weapon_type)
    self._arts = {
      "flower": None,
      "plume": None,
      "sands": None,
      "goblet": None,
      "circlet": None
    }
    self._art_set_bonuses = {}
    Character.count += 1
    self._id = charObj["id"]
    characters[self._id] = self

  def __eq__(self, other) -> bool :
    return self._id == other.id

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
  def arts(self) :
    return self._arts
  @arts.setter
  def arts(self, val) :
    try :
      slot_key, art = val
      assert isinstance(art, (Artifact, type(None)))
    except Exception as e :
      raise e
    # Swapping the artifact location
    if art is not None :
      if slot_key != art.slot_key :
        raise Exception(f"Artifact slot key doesn't match: {slot_key} != {art.slot_key}")
      if self._arts[slot_key] is not None :
        if self._arts[slot_key].location != art.location :
          self._arts[slot_key].location, art.location = art.location, self._arts[slot_key].location
        else :
          self._arts[slot_key].location, art.location = '', self._key
      else :
        art.location = self._key
    else :
      if self._arts[slot_key] is not None :
        self._arts[slot_key].location = ''
    # Equipping the artifact
    self._arts[slot_key] = art
    # Getting artifact sets bonuses
    self._art_set_bonuses = {}
    arts = [art for art in self._arts.values() if art is not None]
    art_sets = Counter((art.set_key) for art in arts).items()
    for art_set, n_pc in art_sets :
      self._art_set_bonuses[art_set] = {}
      for n_pc_bonus in set_key_to_set_bonus[art_set] :
        if n_pc >= n_pc_bonus :
          self._art_set_bonuses[art_set][n_pc_bonus] = set_key_to_set_bonus[art_set][n_pc_bonus]

  @property
  def art_set_bonuses(self) :
    return self._art_set_bonuses

  @property
  def id(self) :
    return self._id

  @property
  def art_stat_values(self) :
    if all(art is None for art in self._arts.values()) :
      return zero_stat_values
    art_stat_values = sum(art for art in self._arts.values() if art is not None)
    for art_set in self._art_set_bonuses :
      for n_pc in self._art_set_bonuses[art_set] :
        if len(list(self._art_set_bonuses[art_set][n_pc]["set_bonus"])) > 0 :
          bonus_stat = list(self._art_set_bonuses[art_set][n_pc]["set_bonus"])[0]
          art_stat_values[bonus_stat] += self._art_set_bonuses[art_set][n_pc]["set_bonus"][bonus_stat]
    return art_stat_values

  @property
  def hp(self) :
    char_hp = \
      self._base_hp*cnt.level_multipliers[self._star][self._level-1] \
      + cnt.ascension_phase_to_total_section[self._ascension]*cnt.max_ascension_values[self._key]["hp"] \
      + (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
        if self._special_stat == "hp" else 0)
    weap_hp = (self._weapon.substat_value if self._weapon.substat == "hp" else 0)
    art_stat_values = self.art_stat_values
    art_hp = art_stat_values["hp%"]
    art_hp_flat = art_stat_values["hp"]
    # print(f"HP: {char_hp}*(1 + {weap_hp} + {art_hp}) + {art_hp_flat}")
    hp = char_hp*(1 + weap_hp + art_hp) + art_hp_flat
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
    art_stat_values = self.art_stat_values
    art_atk = art_stat_values["atk%"]
    art_atk_flat = art_stat_values["atk"]
    # print(f"ATK: {base_atk}*(1 + {weap_atk} + {art_atk}) + {art_atk_flat}")
    atk = base_atk*(1 + weap_atk + art_atk) + art_atk_flat
    return atk

  @property
  def defense(self) :
    char_def = \
      self._base_def*cnt.level_multipliers[self._star][self._level-1] \
      + cnt.ascension_phase_to_total_section[self._ascension]*cnt.max_ascension_values[self._key]["def"] \
      + (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
        if self._special_stat == "def" else 0)
    weap_def = (self._weapon.substat_value if self._weapon.substat == "def" else 0)
    art_stat_values = self.art_stat_values
    art_def = art_stat_values["def%"]
    art_def_flat = art_stat_values["def"]
    # print(f"DEF: {char_def}*(1 + {weap_def} + {art_def}) + {art_def_flat}")
    defense = char_def*(1 + weap_def + art_def) + art_def_flat
    return defense

  @property
  def em(self) :
    char_em = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "em" else 0)
    weap_em = (self._weapon.substat_value if self._weapon.substat == "em" else 0)
    art_stat_values = self.art_stat_values
    art_em = art_stat_values["em"]
    # print(f"EM: {char_em} + {weap_em} + {art_em}")
    em = char_em + weap_em + art_em
    return em

  @property
  def crit_rate(self) :
    char_crit_rate = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "crit_rate" else 0) \
      + (-1 if self._key == "SangonomiyaKokomi" else 0)
    weap_crit_rate = (self._weapon.substat_value if self._weapon.substat == "crit_rate" else 0)
    art_stat_values = self.art_stat_values
    art_crit_rate = art_stat_values["crit_rate"]
    # print(f"CRIT Rate: {char_crit_rate} + .05 + {weap_crit_rate} + {art_crit_rate}")
    crit_rate = char_crit_rate + .05 + weap_crit_rate + art_crit_rate
    return 0 if crit_rate <= 0 else crit_rate if 0 < crit_rate < 1 else 1

  @property
  def crit_dmg(self) :
    char_crit_dmg = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "crit_dmg" else 0)
    weap_crit_dmg = (self._weapon.substat_value if self._weapon.substat == "crit_dmg" else 0)
    art_stat_values = self.art_stat_values
    art_crit_dmg = art_stat_values["crit_dmg"]
    # print(f"CRIT DMG: {char_crit_dmg} + .5 + {weap_crit_dmg} + {art_crit_dmg}")
    crit_dmg = char_crit_dmg + .5 + weap_crit_dmg + art_crit_dmg
    return crit_dmg

  @property
  def healing_bonus(self) :
    char_healing_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "healing_bonus" else 0)
    art_stat_values = self.art_stat_values
    art_healing_bonus = art_stat_values["healing_bonus"]
    # print(f"Healing Bonus: {char_healing_bonus} + {art_healing_bonus}")
    healing_bonus = char_healing_bonus + art_healing_bonus
    return healing_bonus

  @property
  def er(self) :
    char_er = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "er" else 0)
    weap_er = (self._weapon.substat_value if self._weapon.substat == "er" else 0)
    art_stat_values = self.art_stat_values
    art_er = art_stat_values["er"]
    # print(f"ER: {char_er} + 1 + {weap_er} + {art_er}")
    er = char_er + 1 + weap_er + art_er
    return er

  @property
  def pyro_dmg_bonus(self) :
    char_pyro_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "elemental_dmg_bonus" and self._element == "pyro" else 0)
    art_stat_values = self.art_stat_values
    art_pyro_dmg_bonus = art_stat_values["pyro_dmg_bonus"]
    # print(f"Pyro DMG Bonus: {char_pyro_dmg_bonus} + {art_pyro_dmg_bonus}")
    pyro_dmg_bonus = char_pyro_dmg_bonus + art_pyro_dmg_bonus
    return pyro_dmg_bonus

  @property
  def hydro_dmg_bonus(self) :
    char_hydro_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "elemental_dmg_bonus" and self._element == "hydro" else 0)
    art_stat_values = self.art_stat_values
    art_hydro_dmg_bonus = art_stat_values["hydro_dmg_bonus"]
    # print(f"Hydro DMG Bonus: {char_hydro_dmg_bonus} + {art_hydro_dmg_bonus}")
    hydro_dmg_bonus = char_hydro_dmg_bonus + art_hydro_dmg_bonus
    return hydro_dmg_bonus

  @property
  def dendro_dmg_bonus(self) :
    char_dendro_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "elemental_dmg_bonus" and self._element == "dendro" else 0)
    art_stat_values = self.art_stat_values
    art_dendro_dmg_bonus = art_stat_values["dendro_dmg_bonus"]
    # print(f"Dendro DMG Bonus: {char_dendro_dmg_bonus} + {art_dendro_dmg_bonus}")
    dendro_dmg_bonus = char_dendro_dmg_bonus + art_dendro_dmg_bonus
    return dendro_dmg_bonus

  @property
  def electro_dmg_bonus(self) :
    char_electro_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "elemental_dmg_bonus" and self._element == "electro" else 0)
    art_stat_values = self.art_stat_values
    art_electro_dmg_bonus = art_stat_values["electro_dmg_bonus"]
    # print(f"Electro DMG Bonus: {char_electro_dmg_bonus} + {art_electro_dmg_bonus}")
    electro_dmg_bonus = char_electro_dmg_bonus + art_electro_dmg_bonus
    return electro_dmg_bonus

  @property
  def anemo_dmg_bonus(self) :
    char_anemo_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "elemental_dmg_bonus" and self._element == "anemo" else 0)
    art_stat_values = self.art_stat_values
    art_anemo_dmg_bonus = art_stat_values["anemo_dmg_bonus"]
    # print(f"Anemo DMG Bonus: {char_anemo_dmg_bonus} + {art_anemo_dmg_bonus}")
    anemo_dmg_bonus = char_anemo_dmg_bonus + art_anemo_dmg_bonus
    return anemo_dmg_bonus

  @property
  def cryo_dmg_bonus(self) :
    char_cryo_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "elemental_dmg_bonus" and self._element == "cryo" else 0)
    art_stat_values = self.art_stat_values
    art_cryo_dmg_bonus = art_stat_values["cryo_dmg_bonus"]
    # print(f"Cryo DMG Bonus: {char_cryo_dmg_bonus} + {art_cryo_dmg_bonus}")
    cryo_dmg_bonus = char_cryo_dmg_bonus + art_cryo_dmg_bonus
    return cryo_dmg_bonus

  @property
  def geo_dmg_bonus(self) :
    char_geo_dmg_bonus = \
      (cnt.ascension_phase_to_ascension_multipliers[self._ascension]*cnt.special_stat_base_values[self._star][self._special_stat]
      if self._special_stat == "elemental_dmg_bonus" and self._element == "geo" else 0)
    art_stat_values = self.art_stat_values
    art_geo_dmg_bonus = art_stat_values["geo_dmg_bonus"]
    # print(f"Geo DMG Bonus: {char_geo_dmg_bonus} + {art_geo_dmg_bonus}")
    geo_dmg_bonus = char_geo_dmg_bonus + art_geo_dmg_bonus
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
    art_stat_values = self.art_stat_values
    art_physical_dmg_bonus = art_stat_values["physical_dmg_bonus"]
    # print(f"Physical DMG Bonus: {char_physical_dmg_bonus} + {weap_physical_dmg_bonus} + {art_physical_dmg_bonus}")
    physical_dmg_bonus = char_physical_dmg_bonus + weap_physical_dmg_bonus + art_physical_dmg_bonus
    return physical_dmg_bonus
