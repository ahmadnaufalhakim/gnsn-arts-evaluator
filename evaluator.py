from character import Character

def equip_art_combination(char: Character, art_combination) :
  for art in art_combination :
    char.arts = (art.slot_key, art)

def unequip_art_combination(char: Character) :
  for slot_key in ["flower", "plume", "sands", "goblet", "circlet"] :
    char.arts = (slot_key, None)

def evaluate_dmg(char: Character) :
  res = char.atk*(1+char.crit_rate*char.crit_dmg)*(1+char.elemental_dmg_bonus)
  return res

def evaluate_arts(char: Character, art_combinations, top_n = None) :
  best_val = 0 if top_n is None else [0]
  best_art_combination = None if top_n is None else [None]
  for art_combination in art_combinations :
    equip_art_combination(char, art_combination)
    val = evaluate_dmg(char)
    if top_n is None :
      if best_val <= val :
        best_val = val
        best_art_combination = art_combination
    else :
      if min(best_val) <= val :
        best_val.append(val)
        best_art_combination.append(art_combination)
        best_val, best_art_combination = (list(tup)[:top_n] for tup in zip(*sorted(zip(best_val, best_art_combination), reverse=True)))
    unequip_art_combination(char)
  return best_val, best_art_combination
