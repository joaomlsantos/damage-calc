import pickle
import json



def load_obj(name, folder):
    with open(folder + "/" + name + '.pkl', 'rb') as f:
        return pickle.load(f)
    

usage_dict = load_obj("usage_pikalytics_2024g", "pikalytics_result")
moves_dict = load_obj("moves_pikalytics_2024g", "pikalytics_result")
spreads_dict = load_obj("spreads_pikalytics_2024g", "pikalytics_result")
resistances_dict = load_obj("resistances_pikalytics_2024g", "pikalytics_result")
abilities_dict = load_obj("abilities_pikalytics_2024g", "pikalytics_result")
items_dict = load_obj("items_pikalytics_2024g", "pikalytics_result")
teammates_dict = load_obj("teammates_pikalytics_2024g", "pikalytics_result")
types_dict = load_obj("types_pikalytics_2024g", "pikalytics_result")


total_sets = 0
set_dex = {}

for name_p in usage_dict.keys():

    if(int(usage_dict[name_p][0:-1]) == 0):
        continue

    set_dex[name_p] = {}

    spreads_p = spreads_dict[name_p]
    moves_p = moves_dict[name_p]
    abilities_p = abilities_dict[name_p]
    items_p = items_dict[name_p]

    set_moves = []
    set_ability = ""
    for m in moves_p:
        if(m[0] != "Other"):
            set_moves.append(m[0])
    
    if(len(abilities_p) > 0):
        set_ability = abilities_p[0][0]

    for spread in spreads_p:
        set_nature = spread["Nature"]
        set_evs = {
                    "hp": int(spread["HP"]), 
                    "at": int(spread["ATK"]), 
                    "df": int(spread["DEF"]), 
                    "sa": int(spread["SPATK"]), 
                    "sd": int(spread["SPDEF"]), 
                    "sp": int(spread["SPD"])
                   }
        for item in items_p:
            set_item = item[0]
            if(item[0] == "Other" or item[0] == "Nothing"):
                continue
            
            set_title = "VGC " + set_item + " " + spread["HP"] + "/" + spread["ATK"] + "/" + spread["DEF"] + "/" + spread["SPATK"] + "/" + spread["SPDEF"] + "/" + spread["SPD"]

            cur_set = {}
            cur_set["level"] = 50
            cur_set["evs"] = set_evs
            cur_set["nature"] = set_nature
            
            if(set_ability != ""):
                cur_set["ability"] = set_ability

            cur_set["item"] = set_item
            cur_set["moves"] = set_moves

            set_dex[name_p][set_title] = cur_set
            total_sets += 1


print("Total sets = " + str(total_sets))

with open("gen9_spreads.js", "w") as fp:
    json.dump(set_dex, fp, ensure_ascii=False, indent=4)