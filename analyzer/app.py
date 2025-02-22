print("\n\n=== STARTING PROGRAM ===\n\n")  # Add this as the very first line

from flask import Flask, render_template, request, jsonify
import json
import os
import sys

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

app = Flask(__name__)

print("Starting imports...")  # Debug print

try:
    from Competitive_Team_Analyzer import get_weaknesses, all_combos, aggregate_roles, analyzer, load_pokemon_data
    print("Successfully imported Competitive_Team_Analyzer")  # Debug print
except Exception as e:
    print(f"Failed to import Competitive_Team_Analyzer: {str(e)}")  # Debug print
    raise

def load_data():
    # Look for data files in the data directory
    base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    if not os.path.exists(base_path):
        # Fallback to project root if data directory doesn't exist
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return load_pokemon_data(base_path)

# Load data at startup
pokemon_data, uber_data, ou_data, uu_data = load_data()

@app.route('/')
def home():
    print("Accessing home route")  # Debug print
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering template: {str(e)}")  # Debug print
        raise

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debug print
        team = data.get('team', [])
        display_names = data.get('displayNames', [])
        tier = data.get('tier', '').lower()
        
        print("Processing team:", team)  # Debug print
        print("Display names:", display_names)  # Debug print
        
        if not team or len(team) != 6:
            return jsonify({'error': 'Please provide exactly 6 Pokemon'})
        
        # Get the appropriate tier data
        tier_data = {
            'uber': uber_data,
            'ou': ou_data,
            'uu': uu_data
        }.get(tier)
        
        if not tier_data:
            return jsonify({'error': 'Invalid tier selected'})

        # Run analysis with normalized names but keep display names
        totals, names = all_combos(pokemon_data, team)
        role_totals = aggregate_roles(tier_data, team)
        results = analyzer(totals, role_totals, team, tier, pokemon_data, tier_data)
        
        # Add display names to results
        results['display_names'] = dict(zip(team, display_names))
        results['tier_data'] = tier_data
        
        return jsonify(results)
    except Exception as e:
        print(f"Analysis error: {str(e)}")  # Debug print
        print(f"Full error details: {e.__class__.__name__}")  # Print error type
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if os.environ.get('RENDER'):
        # Production on Render
        port = int(os.environ.get('PORT', 10000))
        app.run(host='0.0.0.0', port=port)
    else:
        # Local development
        print("Starting The Battle Lab...")
        app.run(port=8080, debug=True) 