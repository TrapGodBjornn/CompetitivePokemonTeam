ALL_TYPES = ['Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 'Poison', 
             'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 
             'Steel', 'Fairy']

def all_combos(team, tier_data):
    TYPE_CHART = {
        'Normal': {'Rock': 0.5, 'Steel': 0.5, 'Ghost': 0},
        'Fire': {'Fire': 0.5, 'Water': 0.5, 'Rock': 0.5, 'Dragon': 0.5, 'Grass': 2, 'Ice': 2, 'Bug': 2, 'Steel': 2},
        'Water': {'Water': 0.5, 'Grass': 0.5, 'Dragon': 0.5, 'Fire': 2, 'Ground': 2, 'Rock': 2},
        'Electric': {'Electric': 0.5, 'Grass': 0.5, 'Dragon': 0.5, 'Ground': 0, 'Water': 2, 'Flying': 2},
        'Grass': {'Fire': 0.5, 'Grass': 0.5, 'Poison': 0.5, 'Flying': 0.5, 'Bug': 0.5, 'Dragon': 0.5, 'Steel': 0.5, 'Water': 2, 'Ground': 2, 'Rock': 2},
        'Ice': {'Fire': 0.5, 'Water': 0.5, 'Ice': 0.5, 'Steel': 0.5, 'Grass': 2, 'Ground': 2, 'Flying': 2, 'Dragon': 2},
        'Fighting': {'Poison': 0.5, 'Flying': 0.5, 'Psychic': 0.5, 'Bug': 0.5, 'Fairy': 0.5, 'Ghost': 0, 'Normal': 2, 'Ice': 2, 'Rock': 2, 'Dark': 2, 'Steel': 2},
        'Poison': {'Poison': 0.5, 'Ground': 0.5, 'Rock': 0.5, 'Ghost': 0.5, 'Steel': 0, 'Grass': 2, 'Fairy': 2},
        'Ground': {'Grass': 0.5, 'Bug': 0.5, 'Flying': 0, 'Poison': 2, 'Rock': 2, 'Steel': 2, 'Fire': 2, 'Electric': 2},
        'Flying': {'Electric': 0.5, 'Rock': 0.5, 'Steel': 0.5, 'Grass': 2, 'Fighting': 2, 'Bug': 2},
        'Psychic': {'Psychic': 0.5, 'Steel': 0.5, 'Dark': 0, 'Fighting': 2, 'Poison': 2},
        'Bug': {'Fire': 0.5, 'Fighting': 0.5, 'Poison': 0.5, 'Flying': 0.5, 'Ghost': 0.5, 'Steel': 0.5, 'Fairy': 0.5, 'Grass': 2, 'Psychic': 2, 'Dark': 2},
        'Rock': {'Fighting': 0.5, 'Ground': 0.5, 'Steel': 0.5, 'Fire': 2, 'Ice': 2, 'Flying': 2, 'Bug': 2},
        'Ghost': {'Dark': 0.5, 'Normal': 0, 'Psychic': 2, 'Ghost': 2},
        'Dragon': {'Steel': 0.5, 'Fairy': 0, 'Dragon': 2},
        'Dark': {'Fighting': 0.5, 'Dark': 0.5, 'Fairy': 0.5, 'Psychic': 2, 'Ghost': 2},
        'Steel': {'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5, 'Steel': 0.5, 'Ice': 2, 'Rock': 2, 'Fairy': 2},
        'Fairy': {'Fire': 0.5, 'Poison': 0.5, 'Steel': 0.5, 'Fighting': 2, 'Dragon': 2, 'Dark': 2}
    }

    combos = []
    for pokemon in team:
        typing = tier_data[pokemon.lower()]['typing']
        combo = {
            '4x': set(),
            '2x': set(),
            '1x': set(),
            '0.5x': set(),
            '0.25x': set(),
            '0x': set()
        }
        
        # Calculate effectiveness for each attacking type
        for attack_type in ALL_TYPES:
            multiplier = 1.0
            for defend_type in typing:
                if defend_type in TYPE_CHART[attack_type]:
                    multiplier *= TYPE_CHART[attack_type][defend_type]
            
            # Add to appropriate category
            if multiplier == 4:
                combo['4x'].add(attack_type)
            elif multiplier == 2:
                combo['2x'].add(attack_type)
            elif multiplier == 1:
                combo['1x'].add(attack_type)
            elif multiplier == 0.5:
                combo['0.5x'].add(attack_type)
            elif multiplier == 0.25:
                combo['0.25x'].add(attack_type)
            elif multiplier == 0:
                combo['0x'].add(attack_type)
        
        combos.append(combo)
    return combos

def analyze_team(team, display_names, tier_data):
    # Get all type combinations for the team
    type_combos = all_combos(team, tier_data)
    
    # First identify team-wide problems (any type that 2+ Pokemon are weak to)
    problem_types = {}
    for type_name in ALL_TYPES:
        total_weak = 0
        fourx = []
        twox = []
        
        for i, pokemon in enumerate(team):
            combo = type_combos[i]
            if type_name in combo['4x'] or type_name in combo['2x']:  # Count both 4x and 2x as weaknesses
                total_weak += 1
                if type_name in combo['4x']:
                    fourx.append(display_names[i])
                else:
                    twox.append(display_names[i])
        
        if total_weak >= 2:  # If 2 or more Pokemon are weak to this type
            problem_types[type_name] = {
                'total': total_weak,
                'fourx': fourx,
                'twox': twox
            }

    # Calculate role coverage
    role_totals = aggregate_roles(team, tier_data)
    
    # Generate Pokemon-specific problems and recommendations
    pokemon_problems = {}
    used_replacements = set()  # Track which replacements have been used
    
    # First pass to get all problems and initial recommendations
    for i, pokemon in enumerate(team):
        combo = type_combos[i]
        problem_list = list(combo['4x']) + list(combo['2x'])
        filtered_problems = [t for t in problem_list if t in problem_types]
        
        # Get all possible replacements first
        all_replacements = generate_replacements(pokemon, filtered_problems, tier_data) if filtered_problems else []
        
        # For second+ problematic Pokemon, skip any already-used replacements
        if used_replacements and all_replacements:
            all_replacements = [r for r in all_replacements if r['name'] not in used_replacements]
        
        # Take the best remaining replacement
        final_replacements = all_replacements[:3]  # Keep up to 3 recommendations
        if final_replacements:
            used_replacements.add(final_replacements[0]['name'])
        
        pokemon_problems[display_names[i]] = {
            'problem_types': filtered_problems,
            'score': len(filtered_problems) * 2,
            'role': get_role(pokemon, tier_data),
            'replacements': final_replacements
        }

    return {
        'role_totals': role_totals,
        'problem_types': problem_types,
        'pokemon_problems': pokemon_problems
    }

def generate_replacements(pokemon, problem_types, tier_data):
    replacements = []
    
    # Skip if no problems to solve
    if not problem_types:
        return replacements
        
    # Look through all Pokemon in the tier
    for candidate, data in tier_data.items():
        if candidate.lower() == pokemon.lower():
            continue  # Skip the original Pokemon
            
        resists = 0
        typing = data.get('typing', [])
        
        # Calculate how many problem types this candidate resists
        for type_name in problem_types:
            effectiveness = calculate_effectiveness(type_name, typing)
            if effectiveness < 1:  # Resists this type
                resists += 1
                
        # If it resists at least one problem type, consider it
        if resists > 0:
            # Get the first moveset's role or 'Unknown'
            role = data.get('Movesets', [{}])[0].get('role', 'Unknown')
            tier_usage = data.get('tier_usage', 'Unknown')
            
            replacements.append({
                'name': candidate,
                'role': role,
                'resists': resists,
                'tier_usage': tier_usage
            })
    
    # Sort by number of resistances (descending) and tier usage
    replacements.sort(key=lambda x: (-x['resists'], x['tier_usage']))
    
    # Return top 3 recommendations
    return replacements[:3]

def calculate_effectiveness(attack_type, defend_types):
    # Add type effectiveness calculation here
    # This should return the multiplier (0.5 for resistance, 2 for weakness, etc.)
    # We can implement this if needed
    pass 

def aggregate_roles(team, tier_data):
    role_totals = {}
    for pokemon in team:
        role = get_role(pokemon, tier_data)
        if role:
            role_totals[role] = role_totals.get(role, 0) + 1
    return role_totals

def get_role(pokemon, tier_data):
    movesets = tier_data.get(pokemon.lower(), {}).get('Movesets', [])
    return movesets[0].get('role') if movesets else None 