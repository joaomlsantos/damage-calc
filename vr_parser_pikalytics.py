from bs4 import BeautifulSoup
import urllib
import urllib.request
import urllib.parse
import collections
import PokemonList
import pickle
import numpy as np


weaknesses_dict = {"Normal": np.array([1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]), "Fighting": np.array([1, 1, 2, 1, 1, 0.5, 0.5, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0.5, 2]), "Flying": np.array([1, 0.5, 1, 1, 0, 2, 0.5, 1, 1, 1, 1, 0.5, 2, 1, 2, 1, 1, 1]), "Poison": np.array([1, 0.5, 1, 0.5, 2, 1, 0.5, 1, 1, 1, 1, 0.5, 1, 2, 1, 1, 1, 0.5]), "Ground": np.array([1, 1, 1, 0.5, 1, 0.5, 1, 1, 1, 1, 2, 2, 0, 1, 2, 1, 1, 1]), "Rock": np.array([0.5, 2, 0.5, 0.5, 2, 1, 1, 1, 2, 0.5, 2, 2, 1, 1, 1, 1, 1, 1]), "Bug": np.array([1, 0.5, 2, 1, 0.5, 2, 1, 1, 1, 2, 1, 0.5, 1, 1, 1, 1, 1, 1]), "Ghost": np.array([0, 0, 1, 0.5, 1, 1, 0.5, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1]), "Steel": np.array([0.5, 2, 0.5, 0, 2, 0.5, 0.5, 1, 0.5, 2, 1, 0.5, 1, 0.5, 0.5, 0.5, 1, 0.5]), "Fire": np.array([1, 1, 1, 1, 2, 2, 0.5, 1, 0.5, 0.5, 2, 0.5, 1, 1, 0.5, 1, 1, 0.5]), "Water": np.array([1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5, 2, 2, 1, 0.5, 1, 1, 1]), "Grass": np.array([1, 1, 2, 2, 0.5, 1, 2, 1, 1, 2, 0.5, 0.5, 0.5, 1, 2, 1, 1, 1]), "Electric": np.array([1, 1, 0.5, 1, 2, 1, 1, 1, 0.5, 1, 1, 1, 0.5, 1, 1, 1, 1, 1]), "Psychic": np.array([1, 0.5, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 0.5, 1, 1, 2, 1]), "Ice": np.array([1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 0.5, 1, 1, 1]), "Dragon": np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5, 1, 2, 2, 1, 2]), "Dark": np.array([1, 2, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 1, 1, 0, 1, 1, 0.5, 2]), "Fairy": np.array([1, 0.5, 1, 2, 1, 1, 0.5, 1, 2, 1, 1, 1, 1, 1, 1, 0, 0.5, 1])}


def get_moves(soup):
    res_moves = []
    html_moves = soup.find("div",id="moves_wrapper").find_all("div",{"class": "pokedex-move-entry-new"})
    for move in html_moves:
        move_name = move.contents[1].get_text()
        move_type = move.contents[3].get_text()
        move_percentage = move.contents[5].get_text()
        res_moves.append((move_name, move_type, move_percentage))
    return res_moves


def get_teammates(soup):
    res_teammates = []
    html_teammates = soup.find("div",id="dex_team_wrapper")
    teammates = html_teammates.find_all("a")
    for m in teammates:
        teammate_name = m.contents[3].get_text().strip('\n')
        teammate_percentage = m.contents[7].get_text()
        res_teammates.append((teammate_name, teammate_percentage))
    return res_teammates


def get_items(soup):
    res_items = []
    html_items = soup.find("div", id="items_wrapper").find_all("div",{"class": "pokedex-move-entry-new"})
    for item in html_items:
        res_items.append((item.contents[3].get_text(), item.contents[5].get_text()))
    return res_items

def get_abilities(soup):
    res_abilities = []
    html_abilities = soup.find("div", id="abilities_wrapper").find_all("div",{"class": "pokedex-move-entry-new"})
    for ability in html_abilities:
        res_abilities.append((ability.contents[1].get_text(), ability.contents[3].get_text()))
    return res_abilities

def get_types(soup):
    res_types = []
    html_types = soup.find("span", {"class": "inline-block pokedex-header-types"})
    for t in html_types.contents:
        res_types.append(t.get_text().capitalize())
    return res_types

def get_spreads(soup):
    res_spreads = []
    html_spreads = soup.find("div", id="dex_spreads_wrapper").find_all("div",{"class": "pokedex-move-entry-new"})
    for spread in html_spreads:
        temp_spread = []
        temp_spread.append(("Nature", spread.contents[1].get_text()))
        temp_spread.append(("HP", spread.contents[3].get_text().strip('/')))
        temp_spread.append(("ATK", spread.contents[4].get_text().strip('/')))
        temp_spread.append(("DEF", spread.contents[5].get_text().strip('/')))
        temp_spread.append(("SPATK", spread.contents[6].get_text().strip('/')))
        temp_spread.append(("SPDEF", spread.contents[7].get_text().strip('/')))
        temp_spread.append(("SPD", spread.contents[8].get_text().strip('/')))
        temp_spread.append(("USAGE", spread.contents[10].get_text().strip('/')))
        res_spreads.append(collections.OrderedDict(temp_spread))
    return res_spreads

def print_spreads(res_spreads):
    for spread in res_spreads:
        list_spr = list(spread.values())
        f_string = list_spr[0] + " "
        evs = list_spr[1:len(list_spr)-1]
        f_string += "/".join(evs)
        f_string += " : " + list_spr[-1]
        print(f_string)
    

def save_obj(obj, name):
    with open('obj\\' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj\\' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def get_resistances(types_dict):
    resistances_dict = {}
    for pokemon in types_dict.keys():
        resistances_dict[pokemon] = calc_resistances(types_dict[pokemon])
    return resistances_dict

def calc_resistances(types_list):
    res_resistances = np.ones(18)
    for t in types_list:
        res_resistances *= weaknesses_dict[t]
    return res_resistances

def generate_moves_data():
    url = "https://bulbapedia.bulbagarden.net/wiki/List_of_moves_by_availability_(Generation_IX)"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    moves = {}

    table = soup.find_all("table")
    trs = table[1].find_all('tr')
    for tr in trs:
        move_data = {}
        tds = tr.find_all("td")
        if(len(tds) < 8):
            continue
        move_data["Category"] = tds[3].text.strip()
        move_data["Type"] = tds[2].text.strip()
        move_data["PP"] = tds[4].text.strip()
        move_data["Power"] = tds[5].text.strip()
        move_data["Accuracy"] = tds[6].text.strip()
        moves[tds[1].text.strip()] = move_data
    
    save_obj(moves, "moves_data_gen8.pkl")



main_url = "https://pikalytics.com/pokedex/gen9vgc2024regg"

req = urllib.request.Request(main_url, headers={'User-Agent': 'Mozilla/5.0'})
main_page = urllib.request.urlopen(req)
main_soup = BeautifulSoup(main_page, 'html.parser')
poke_entries = main_soup.find_all("a",attrs={"class":"pokedex_entry"})
pokemon_names = PokemonList.pokemon_list.copy()
read_pokemon = []


usage_dict = {}
moves_dict = {}
abilities_dict = {}
teammates_dict = {}
items_dict = {}
spreads_dict = {}
types_dict = {}


for pokemon in pokemon_names:
    try:
        temp_url = main_url + "/" + urllib.parse.quote(pokemon.lower())
        temp_req = urllib.request.Request(temp_url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urllib.request.urlopen(temp_req)
        soup = BeautifulSoup(page, 'html.parser')
        moves = get_moves(soup)
        usage_el = soup.find("div",{"class": "pokemon-ind-summary-text gold-font"})
        usage_percentage = "0%"
        if(not usage_el is None):
            usage_percentage = usage_el.contents[0] + "%"

        teammates = get_teammates(soup)
        items = get_items(soup)
        abilities = get_abilities(soup)
        spreads = get_spreads(soup)
        types = get_types(soup)
        print(pokemon + ": " + usage_percentage)
        print(pokemon + "\'s moves:")
        for i in range(len(moves)):
            print(moves[i][0] + ": " + moves[i][2] + " (" + moves[i][1].capitalize() + ")")
        print()
        print(pokemon + '\'s teammates:')
        for i in range(len(teammates)):
            print(teammates[i][0] + ": " + teammates[i][1])
        print()
        print(pokemon + '\'s items:')
        for i in range(len(items)):
            print(items[i][0] + ": " + items[i][1])
        print()
        print(pokemon + '\'s abilities:')
        for i in range(len(abilities)):
            print(abilities[i][0] + ": " + abilities[i][1])
        print()
        print_spreads(spreads)
        print("\n")

        usage_dict[pokemon] = usage_percentage
        moves_dict[pokemon] = moves
        teammates_dict[pokemon] = teammates
        items_dict[pokemon] = items
        spreads_dict[pokemon] = spreads
        abilities_dict[pokemon] = abilities
        types_dict[pokemon] = types
        read_pokemon.append(pokemon)

    except urllib.error.HTTPError:
        print(pokemon + " skipped; no url found")
        continue
    except AttributeError:
        print(pokemon + " skipped: error in data processing")
        continue

resistances_dict = get_resistances(types_dict)


print(read_pokemon)
save_obj(usage_dict, "usage_pikalytics_2024g")
save_obj(moves_dict, "moves_pikalytics_2024g")
save_obj(teammates_dict, "teammates_pikalytics_2024g")
save_obj(items_dict, "items_pikalytics_2024g")
save_obj(abilities_dict, "abilities_pikalytics_2024g")
save_obj(spreads_dict, "spreads_pikalytics_2024g")
save_obj(types_dict, "types_pikalytics_2024g")
save_obj(resistances_dict, "resistances_pikalytics_2024g")


