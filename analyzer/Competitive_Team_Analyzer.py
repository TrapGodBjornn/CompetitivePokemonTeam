import json
from pprint import pprint
from collections import defaultdict
import os

def load_pokemon_data(base_path):
    """Load all Pokemon data files from the given base path"""
    global pokemon_data
    with open(os.path.join(base_path, "pokedex.json"), "r", encoding="utf-8") as f:
        pokemon_data = json.load(f)
    with open(os.path.join(base_path, "converted_uber.json"), "r", encoding="utf-8") as f:
        uber_data = json.load(f)
    with open(os.path.join(base_path, "converted_OU.json"), "r", encoding="utf-8") as f:
        ou_data = json.load(f)
    with open(os.path.join(base_path, "converted_UU.json"), "r", encoding="utf-8") as f:
        uu_data = json.load(f)
    return pokemon_data, uber_data, ou_data, uu_data

ALL_TYPES = [
    "Normal", "Fire", "Water", "Electric", "Grass",
    "Ice", "Fighting", "Poison", "Ground", "Flying",
    "Psychic", "Bug", "Rock", "Ghost", "Dragon",
    "Dark", "Steel", "Fairy"
]

# Add tier rankings as a global constant
TIER_RANKINGS = {
    "S": 7,
    "S-": 6,
    "A+": 5,
    "A": 4,
    "A-": 3,
    "B+": 2,
    "B": 1,
    "Unknown": 0
}


def type_effectiveness():
    weaknesses = {
        "Water": {"Electric": 2.0, "Grass": 2.0},
        "Fire": {"Water": 2.0, "Rock": 2.0, "Ground": 2.0},
        "Grass": {"Fire": 2.0, "Flying": 2.0, "Bug": 2.0, "Poison": 2.0, "Ice": 2.0},
        "Electric": {"Ground": 2.0},
        "Rock": {"Water": 2.0, "Grass": 2.0, "Fighting": 2.0, "Ground": 2.0, "Steel": 2.0},
        "Ground": {"Water": 2.0, "Grass": 2.0, "Ice": 2.0},
        "Steel": {"Fire": 2.0, "Fighting": 2.0, "Ground": 2.0},
        "Fighting": {"Flying": 2.0, "Psychic": 2.0, "Fairy": 2.0},
        "Flying": {"Electric": 2.0, "Ice": 2.0, "Rock": 2.0},
        "Bug": {"Fire": 2.0, "Flying": 2.0, "Rock": 2.0},
        "Poison": {"Ground": 2.0, "Psychic": 2.0},
        "Ice": {"Fire": 2.0, "Fighting": 2.0, "Rock": 2.0, "Steel": 2.0},
        "Psychic": {"Bug": 2.0, "Ghost": 2.0, "Dark": 2.0},
        "Ghost": {"Ghost": 2.0, "Dark": 2.0},
        "Dark": {"Fighting": 2.0, "Bug": 2.0, "Fairy": 2.0},
        "Dragon": {"Ice": 2.0, "Dragon": 2.0, "Fairy": 2.0},
        "Fairy": {"Poison": 2.0, "Steel": 2.0},
        "Normal": {"Fighting": 2.0},
    }

    strengths = {
        "Water": {"Fire": 2.0, "Rock": 2.0, "Ground": 2.0},
        "Fire": {"Grass": 2.0, "Bug": 2.0, "Ice": 2.0, "Steel": 2.0},
        "Grass": {"Water": 2.0, "Ground": 2.0, "Rock": 2.0},
        "Electric": {"Water": 2.0, "Flying": 2.0},
        "Rock": {"Fire": 2.0, "Ice": 2.0, "Flying": 2.0, "Bug": 2.0},
        "Ground": {"Fire": 2.0, "Electric": 2.0, "Poison": 2.0, "Rock": 2.0, "Steel": 2.0},
        "Steel": {"Ice": 2.0, "Rock": 2.0, "Fairy": 2.0},
        "Fighting": {"Normal": 2.0, "Ice": 2.0, "Rock": 2.0, "Dark": 2.0, "Steel": 2.0},
        "Flying": {"Grass": 2.0, "Fighting": 2.0, "Bug": 2.0},
        "Bug": {"Grass": 2.0, "Psychic": 2.0, "Dark": 2.0},
        "Poison": {"Grass": 2.0, "Fairy": 2.0},
        "Ice": {"Grass": 2.0, "Flying": 2.0, "Dragon": 2.0, "Ground": 2.0},
        "Psychic": {"Fighting": 2.0, "Poison": 2.0},
        "Ghost": {"Psychic": 2.0, "Ghost": 2.0},
        "Dark": {"Psychic": 2.0, "Ghost": 2.0},
        "Dragon": {"Dragon": 2.0},
        "Fairy": {"Fighting": 2.0, "Dragon": 2.0, "Dark": 2.0},
        "Normal": {},
    }

    resistances = {
        "Water": {"Fire": 0.5, "Water": 0.5, "Ice": 0.5, "Steel": 0.5},
        "Fire": {"Fire": 0.5, "Grass": 0.5, "Ice": 0.5, "Bug": 0.5, "Steel": 0.5, "Fairy": 0.5},
        "Grass": {"Water": 0.5, "Grass": 0.5, "Electric": 0.5, "Ground": 0.5},
        "Electric": {"Electric": 0.5, "Steel": 0.5, "Flying": 0.5},
        "Rock": {"Normal": 0.5, "Fire": 0.5, "Flying": 0.5, "Poison": 0.5},
        "Ground": {"Poison": 0.5, "Rock": 0.5},
        "Steel": {"Normal": 0.5, "Grass": 0.5, "Ice": 0.5, "Flying": 0.5, "Psychic": 0.5,
                  "Bug": 0.5, "Rock": 0.5, "Dragon": 0.5, "Steel": 0.5, "Fairy": 0.5},
        "Fighting": {"Bug": 0.5, "Rock": 0.5, "Dark": 0.5},
        "Flying": {"Grass": 0.5, "Fighting": 0.5, "Bug": 0.5},
        "Bug": {"Grass": 0.5, "Fighting": 0.5, "Ground": 0.5},
        "Poison": {"Grass": 0.5, "Fighting": 0.5, "Poison": 0.5, "Bug": 0.5, "Fairy": 0.5},
        "Ice": {"Ice": 0.5},
        "Psychic": {"Fighting": 0.5, "Psychic": 0.5},
        "Ghost": {"Poison": 0.5, "Bug": 0.5},
        "Dark": {"Ghost": 0.5, "Dark": 0.5},
        "Dragon": {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Grass": 0.5},
        "Fairy": {"Fighting": 0.5, "Bug": 0.5, "Dark": 0.5},
        "Normal": {},
    }

    immunities = {
        "Water": {},
        "Fire": {},
        "Grass": {},
        "Electric": {},
        "Rock": {},
        "Ground": {"Electric": 0.0},
        "Steel": {"Poison": 0.0},
        "Fighting": {},
        "Flying": {"Ground": 0.0},
        "Bug": {},
        "Poison": {},
        "Ice": {},
        "Psychic": {},
        "Ghost": {"Fighting": 0.0, "Normal": 0.0},
        "Dark": {"Psychic": 0.0},
        "Dragon": {},
        "Fairy": {"Dragon": 0.0},
        "Normal": {"Ghost": 0.0},
    }

    return weaknesses, strengths, resistances, immunities


def capitalize_name(name):
    """Helper to properly capitalize Pokemon names"""
    return name[0].upper() + name[1:].lower() if name else name

def get_weaknesses(pokemon_name, pokemon_data):
    # Get type effectiveness data
    weaknesses, _, resistances, immunities = type_effectiveness()
    
    # Always look up with lowercase
    name_lower = pokemon_name.lower().strip()
    pokemon = pokemon_data.get(name_lower)
    
    if not pokemon:
        return f"{pokemon_name} not found in data."
    
    pokemon_types = pokemon.get("types", [])
    if not pokemon_types:
        return f"No types found for {pokemon_name}."
    
    # Initialize sets to store the results
    x4_weak = set()
    x2_weak = set()
    x05_resist = set()
    x0_immune = set()
    neutral = set()
    
    # For each potential attacking type in the game:
    for attacking_type in ALL_TYPES:
        # Start with a 1.0 multiplier
        net_multiplier = 1.0
        
        # For each defensive type 
        for def_type in pokemon_types:
            # 1) Check immunity first (0.0 overrides everything)
            if def_type in immunities:
                if attacking_type in immunities[def_type]:
                    net_multiplier = 0.0
                    break  # no need to check further types
                
            # 2) If not immune, check weaknesses
            if def_type in weaknesses:
                # If attacking_type is in this dictionary, multiply by e.g. 2.0
                net_multiplier *= weaknesses[def_type].get(attacking_type, 1.0)
            
            # 3) Check resistances
            if def_type in resistances:
                # e.g. 0.5 if found
                net_multiplier *= resistances[def_type].get(attacking_type, 1.0)
            
        
        # Net multiplier:
        if net_multiplier == 0.0:
            x0_immune.add(attacking_type)
        elif net_multiplier == 4.0:
            x4_weak.add(attacking_type)
        elif net_multiplier == 2.0:
            x2_weak.add(attacking_type)
        elif net_multiplier == 0.5:
            x05_resist.add(attacking_type)
        #else:
        #    neutral.add(attacking_type)
    
    return {
        "4x": x4_weak,
        "2x": x2_weak,
        "0x": x0_immune,
        "0.5x": x05_resist,
        #"neutral_or_other": neutral
    }




def all_combos(pokemon_data, team_list, team_size=6):
    from collections import defaultdict

    resultys = []
    names = []

    totals = {
        "4x": defaultdict(int),
        "2x": defaultdict(int),
        "0x": defaultdict(int),
        "0.5x": defaultdict(int),
    } 

    for name in team_list:
        names.append(name)
        resultado = get_weaknesses(name, pokemon_data)
        resultys.append(resultado)

    print(resultys)

    for res in resultys:
        if isinstance(res, str):
            print("Error cousin", res)
            continue 

        for category in ["4x", "2x", "0.5x", "0x"]:
            for atk_type in res[category]:
                totals[category][atk_type] += 1

    print("\n=== Team Totals ===")
    for category in ["4x", "2x", "0.5x", "0x"]:
        print(f"\n{category} results:")
        lines = []
        for atk_type, count in totals[category].items():
            lines.append(f"{atk_type}({count})")
        if lines:
            print(", ".join(lines))
        else:
            print("None")
    return totals, names

    #Check weaknesses. For (4x), if more than 1, suggest replacement. For (2x), if more than 2, suggest replacement. 
    #Combos
    #If a single (4x), no more than 1 (2x) weakness
    #If there are 2 (2x), no (4x) allowed


def aggregate_roles(tierdata, names, team_size=6):
    role_counts = defaultdict(int)
    
    for name in names:
        # Convert to lowercase for data lookup
        name_lower = name.lower().strip()
        mon_data = tierdata.get(name_lower)
        
        if mon_data and "Movesets" in mon_data and mon_data["Movesets"]:
            role = mon_data["Movesets"][0].get("role")
            if role:
                role_counts[role] += 1
    
    return role_counts


def calculate_vulnerability_multiplier(num_weak_pokemon):
    """Returns multiplier based on how many Pokemon share a weakness"""
    if num_weak_pokemon >= 6: return 2.5
    if num_weak_pokemon == 5: return 2.0
    if num_weak_pokemon == 4: return 1.5
    if num_weak_pokemon == 3: return 1.2
    return 1.0

def calculate_role_multiplier(num_same_role):
    """Returns multiplier for role overlap"""
    if num_same_role >= 4: return 2.0
    if num_same_role == 3: return 1.5
    return 0

def calculate_pokemon_score(pokemon, team_weaknesses, role_counts, tier_data):
    """Calculate how problematic a Pokemon is based on its weaknesses and role"""
    score = 0
    weaknesses = get_weaknesses(pokemon, pokemon_data)
    
    # Type vulnerability score
    for type, pokemon_weak in team_weaknesses.items():
        if pokemon in pokemon_weak:
            num_weak = len(pokemon_weak)
            multiplier = calculate_vulnerability_multiplier(num_weak)
            
            if isinstance(weaknesses, dict):
                if type in weaknesses['4x']:
                    score += 2 * multiplier
                elif type in weaknesses['2x']:
                    score += 1 * multiplier
    
    # Role score
    mon_data = tier_data.get(pokemon)
    if mon_data and "Movesets" in mon_data and mon_data["Movesets"]:
        role = mon_data["Movesets"][0].get("role")
        if role in role_counts:
            score += 5 * calculate_role_multiplier(role_counts[role])
    
    return score

def calculate_candidate_score(candidate, problem_types, needed_role, tier_data):
    """Calculate how good a replacement a candidate would be"""
    score = 0
    pokemon_data = tier_data.get(candidate['name'])
    if not pokemon_data:
        return 0
        
    # Base tier score
    tier_score = TIER_RANKINGS.get(pokemon_data.get("tier_usage", "B"), 0)
    score += tier_score * 3
    
    # Type resistance scoring
    resisted_types = 0
    candidate_types = pokemon_data.get("typing", [])
    _, _, resistances, immunities = type_effectiveness()
    
    for prob_type in problem_types:
        for type in candidate_types:
            if (prob_type in resistances.get(type, {}) or 
                prob_type in immunities.get(type, {})):
                resisted_types += 1
                break
    
    # Bonus for resisting multiple types
    if resisted_types > 0:
        type_score = resisted_types * 5
        type_score *= (1 + (resisted_types - 1) * 0.5)
        score += type_score
    
    # Role score
    if needed_role and "Movesets" in pokemon_data and pokemon_data["Movesets"]:
        if pokemon_data["Movesets"][0].get("role") != needed_role:
            score += 4
    
    return score

def get_replacement_threshold(scores):
    max_score = max(scores.values())
    if max_score >= 8.0:  # Highly problematic team
        return 6.0  # Will catch Pokemon with significant issues
    elif max_score >= 5.0:  # Moderately problematic
        return 4.0
    else:  # Minor issues
        return 2.0

def find_best_replacements(problem_pokemon, tier_data, pokemon_data, role_totals, team_weaknesses):
    """Find the best replacements for a problematic Pokemon"""
    candidates = []
    
    # Get current Pokemon's role and weaknesses
    current_role = None
    mon_data = tier_data.get(problem_pokemon)
    if mon_data and "Movesets" in mon_data and mon_data["Movesets"]:
        current_role = mon_data["Movesets"][0].get("role")
    
    # Only consider role a problem if we have >2 of that role
    role_is_problem = current_role and role_totals.get(current_role, 0) > 2
    
    # Get problem types this Pokemon is weak to
    problem_types = []
    weaknesses = get_weaknesses(problem_pokemon, pokemon_data)
    if isinstance(weaknesses, dict):
        for type, weak_mons in team_weaknesses.items():
            if len(weak_mons) > 2 and problem_pokemon in weak_mons:
                problem_types.append(type)
    
    # Score each potential replacement
    for pokemon_name, mon_data in tier_data.items():
        if pokemon_name == problem_pokemon:
            continue
            
        score = 0
        
        # Base score from tier
        tier = mon_data.get("tier_usage", "Unknown")
        score += TIER_RANKINGS.get(tier, 0) * 3
        
        # Check type improvements
        weaknesses = get_weaknesses(pokemon_name, pokemon_data)
        if isinstance(weaknesses, dict):
            # Bonus for not sharing problem weaknesses
            shares_weaknesses = False
            for type in problem_types:
                if type in weaknesses['4x'] or type in weaknesses['2x']:
                    shares_weaknesses = True
                    score -= 10
                    break
            if not shares_weaknesses:
                score += 15
        
        # Check role improvement
        if "Movesets" in mon_data and mon_data["Movesets"]:
            role = mon_data["Movesets"][0].get("role")
            if role_is_problem and role == current_role:
                score -= 10
            elif role in ["Physical Wall", "Special Wall", "Physical Attacker", "Special Attacker"] and role_totals.get(role, 0) == 0:
                score += 10
        
        candidates.append((pokemon_name, score, mon_data))
    
    # Get top 3 suggestions that actually improve the situation
    candidates.sort(key=lambda x: x[1], reverse=True)
    return [c for c in candidates[:3] if c[1] > 0]  # Only return if score > 0

def analyze_team_with_addition(names, addition, tier_data, pokemon_data):
    """Analyze team composition including the suggested addition"""
    new_team = names + [addition]
    
    # Analyze roles
    role_counts = defaultdict(int)
    for pokemon in new_team:
        mon_data = tier_data.get(pokemon)
        if mon_data and "Movesets" in mon_data and mon_data["Movesets"]:
            role = mon_data["Movesets"][0].get("role")
            if role:
                role_counts[role] += 1
    
    # Analyze type coverage
    type_weaknesses = defaultdict(list)
    for name in new_team:
        weaknesses = get_weaknesses(name, pokemon_data)
        if isinstance(weaknesses, dict):
            for type in ALL_TYPES:
                if type in weaknesses['4x']:
                    type_weaknesses[type].extend([name] * 2)
                elif type in weaknesses['2x']:
                    type_weaknesses[type].append(name)
    
    return role_counts, type_weaknesses

def analyzer(totals, role_totals, names, tier, pokemon_data, tier_data):
    # Convert names to lowercase for data lookup but keep original for display
    names_lower = [name.lower().strip() for name in names]
    names_display = [capitalize_name(name) for name in names]
    
    # First identify all problem types
    problem_types = {}
    pokemon_scores = defaultdict(int)
    pokemon_weaknesses = defaultdict(list)  # Track weaknesses for each Pokemon
    
    for atk_type in ALL_TYPES:
        fourx_weak = []
        twox_weak = []
        
        for name in names_lower:
            weaknesses = get_weaknesses(name, pokemon_data)
            if isinstance(weaknesses, dict):
                if atk_type in weaknesses['4x']:
                    fourx_weak.append(capitalize_name(name))
                    pokemon_scores[name] += 3
                    pokemon_weaknesses[name].append(atk_type)  # Add to Pokemon's weaknesses
                elif atk_type in weaknesses['2x']:
                    twox_weak.append(capitalize_name(name))
                    pokemon_scores[name] += 1
                    pokemon_weaknesses[name].append(atk_type)  # Add to Pokemon's weaknesses
        
        total_weak = len(fourx_weak) + len(twox_weak)
        if total_weak > 1:
            problem_types[atk_type] = {
                "fourx": fourx_weak,
                "twox": twox_weak,
                "total": total_weak
            }

    # Find replacements for problematic Pokemon
    pokemon_problem_count = defaultdict(lambda: {"problem_types": [], "role": None, "replacements": [], "score": 0})
    
    for name in names_lower:
        name_display = capitalize_name(name)
        
        # Add the collected problem types for this Pokemon
        pokemon_problem_count[name_display]["problem_types"] = pokemon_weaknesses[name]
        
        mon_data = tier_data.get(name)
        if mon_data and "Movesets" in mon_data and mon_data["Movesets"]:
            current_role = mon_data["Movesets"][0].get("role")
            pokemon_problem_count[name_display]["role"] = current_role
            pokemon_problem_count[name_display]["score"] = pokemon_scores[name]
            
            if pokemon_scores[name] > 0:
                # Get all Pokemon in the tier
                tier_pokemon = [name for name in tier_data.keys()]
                
                # Find replacements that resist the problem types
                replacements = []
                problem_types_list = pokemon_problem_count[name_display]["problem_types"]
                
                for candidate in tier_pokemon:
                    if candidate == name:
                        continue
                    
                    candidate_weaknesses = get_weaknesses(candidate, pokemon_data)
                    if isinstance(candidate_weaknesses, str):
                        continue
                    
                    # Check if candidate resists the problem types
                    resists_count = 0
                    for prob_type in problem_types_list:
                        if (prob_type in candidate_weaknesses["0x"] or 
                            prob_type in candidate_weaknesses["0.5x"]):
                            resists_count += 1
                    
                    if resists_count > 0:
                        cand_data = tier_data[candidate]
                        cand_role = "Unknown"
                        if "Movesets" in cand_data and cand_data["Movesets"]:
                            cand_role = cand_data["Movesets"][0].get("role", "Unknown")
                        
                        replacements.append({
                            "name": capitalize_name(candidate),  # Capitalize replacement name
                            "role": cand_role,
                            "resists": resists_count,
                            "tier_usage": cand_data.get("tier_usage", "Unknown")
                        })
                
                replacements.sort(key=lambda x: x["resists"], reverse=True)
                pokemon_problem_count[name_display]["replacements"] = replacements[:3]

    return {
        'role_totals': dict(role_totals),
        'problem_types': problem_types,
        'pokemon_problems': pokemon_problem_count
    }

def find_replacements(pokemon, weakness_types, current_role, tier_data, replacement_candidates):
    """Find replacement Pokemon that address both type and role issues"""
    replacements = []
    _, _, resistances, immunities = type_effectiveness()
    
    print(f"\nFinding replacements for {pokemon}:")
    print(f"Must resist: {', '.join(weakness_types)}")
    if current_role:
        print(f"Must not have role: {current_role}")
    
    for candidate in replacement_candidates:
        pokemon_data = tier_data.get(candidate['name'])
        if not pokemon_data or candidate['name'] == pokemon:
            continue
        
        # Check type resistances
        resists_all = True
        candidate_types = pokemon_data.get("typing", [])
        
        for weakness_type in weakness_types:
            resists_this_type = False
            for type in candidate_types:
                if (weakness_type in resistances.get(type, {}) or 
                    weakness_type in immunities.get(type, {})):
                    resists_this_type = True
                    break
            if not resists_this_type:
                resists_all = False
                break
        
        # Check role
        valid_role = True
        if current_role and "Movesets" in pokemon_data and pokemon_data["Movesets"]:
            if pokemon_data["Movesets"][0].get("role") == current_role:
                valid_role = False
        
        if resists_all and valid_role:
            tier = pokemon_data.get("tier_usage", "Unknown")
            replacements.append(f"{candidate['name']} ({tier})")
            if len(replacements) >= 3:
                break
    
    return replacements

