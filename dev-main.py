import itertools
import json
import os
import glob
import pprint
import sys
import time
from src.artifact import Artifact
from src.character import Character
from src.weapon import Weapon
from src.utils.evaluator import (
  equip_art_combination,
  evaluate_arts
)

# db_dir = os.path.join(os.getcwd(), "data", '*')
# files = glob.glob(db_dir)
# print(files)
# latest_file = max(files, key=os.path.getctime)
# print(latest_file)

# f_char = open("./templates/characters/wanderer.json")
f_char = open("./templates/riska/wanderer.json")
charObj = json.load(f_char)
char = Character(charObj)

# print(char.art_stat_values)

# f_weapon = open("./templates/weapons/tulaytullah.json")
f_weapon = open("./templates/riska/widsith.json")
weapObj = json.load(f_weapon)
weapon = Weapon(weapObj)
char.weapon = weapon

# f_all_artifacts = open("./templates/artifacts/all_artifacts.json")
f_all_artifacts = open("./templates/riska/all-artifacts.json")
artObjs = json.load(f_all_artifacts)["artifacts"]
arts = [Artifact(artObj) for artObj in artObjs]
candidate_flower_arts = []
candidate_plume_arts = []
candidate_sands_arts = []
candidate_goblet_arts = []
candidate_circlet_arts = []
for art in arts :
  # if art.slot_key == "flower" :
  #   candidate_flower_arts.append(art)
  if art.slot_key == "plume" :
    candidate_plume_arts.append(art)
  # if art.slot_key == "sands" :
  #   candidate_sands_arts.append(art)
  # if art.slot_key == "goblet":
  #   candidate_goblet_arts.append(art)
  # if art.slot_key == "circlet" :
  #   candidate_circlet_arts.append(art)
  # if art.slot_key == "goblet" and art.main_stat == "anemo_dmg_bonus" :
  #   candidate_goblet_arts.append(art)
  if art.set_key == "DesertPavilionChronicle" :
    if art.slot_key == "flower" :
      candidate_flower_arts.append(art)
    # if art.slot_key == "plume" :
    #   candidate_plume_arts.append(art)
    if art.slot_key == "sands" :
      candidate_sands_arts.append(art)
    if art.slot_key == "goblet":
      candidate_goblet_arts.append(art)
    if art.slot_key == "circlet" :
      candidate_circlet_arts.append(art)

# candidate_flower_arts = candidate_flower_arts[:50]
# candidate_plume_arts = candidate_plume_arts[:10]
# candidate_sands_arts = candidate_sands_arts[:10]
# candidate_goblet_arts = candidate_goblet_arts[:10]
# candidate_circlet_arts = candidate_circlet_arts[:10]

# print(candidate_flower_arts)
# print(candidate_plume_arts)
# print(candidate_sands_arts)
# print(candidate_goblet_arts)
# print(candidate_circlet_arts)

print(len(candidate_flower_arts))
print(len(candidate_plume_arts))
print(len(candidate_sands_arts))
print(len(candidate_goblet_arts))
print(len(candidate_circlet_arts))

all_art_combinations = list(itertools.product(candidate_flower_arts, candidate_plume_arts, candidate_sands_arts, candidate_goblet_arts, candidate_circlet_arts))
print(len(all_art_combinations))
if len(all_art_combinations) >= 200000 :
  confirm = input(f"{len(all_art_combinations)} artifact combinations found.\nIt will probably take a long time to evaluate (ETA {round((len(all_art_combinations)/200000), 1)} min(s)).\nDo you want to continue? (y/n): ")
  while confirm != 'y' and confirm != 'n' :
    confirm = input(f"Invalid input. Do you want to continue? (y/n): ")
  if confirm == 'y' :
    best_val, best_art_combination = evaluate_arts(char, all_art_combinations)
  elif confirm == 'n' :
    sys.exit()
else :
  best_val, best_art_combination = evaluate_arts(char, all_art_combinations)

print(best_val, best_art_combination)

# print(char.hp, char.atk, char.defense, char.crit_rate, char.crit_dmg, char.elemental_dmg_bonus)
# print(char.art_stat_values)
# print(best_val, best_art_combination)
equip_art_combination(char, best_art_combination)
print(char.hp, char.atk, char.defense, char.crit_rate, char.crit_dmg, char.elemental_dmg_bonus)
print(char.art_stat_values)
# print(best_art_combination)
