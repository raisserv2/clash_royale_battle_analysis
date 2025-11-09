import requests
import json
from typing import Dict, List, Any
import time

def fetch_arena_mapping() -> Dict[str, Any]:
    """Fetch and parse arena data from game data JSON"""
    game_data_url = "https://cdn.statsroyale.com/gamedata-v4.json"
    
    try:
        print("🎮 Fetching game data...")
        headers = {
            'referer': 'https://statsroyale.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
        }
        response = requests.get(game_data_url, headers=headers)
        response.raise_for_status()
        game_data = response.json()
        
        arenas = game_data['items']['arenas']
        print(f"✅ Loaded data for {len(arenas)} arenas")
        
        return arenas
        
    except Exception as e:
        print(f"❌ Failed to fetch game data: {e}")
        return []

def analyze_arenas(arenas: List[Dict]) -> Dict[str, Any]:
    """Analyze and organize arena data"""
    # Filter main progression arenas
    main_arenas = [
        arena for arena in arenas 
        if arena.get('trophyRoad') == 'Default' 
        and arena.get('arena') is not None
        and arena.get('trophyLimit', 0) > 0
    ]
    
    # Remove duplicates by arena number
    seen_arenas = set()
    unique_arenas = []
    for arena in main_arenas:
        arena_num = arena['arena']
        if arena_num not in seen_arenas:
            seen_arenas.add(arena_num)
            unique_arenas.append(arena)
    
    # Sort by arena number
    sorted_arenas = sorted(unique_arenas, key=lambda x: x['arena'])
    
    # Build trophy ranges
    arena_ranges = {}
    for i, arena in enumerate(sorted_arenas):
        arena_num = arena['arena']
        trophy_limit = arena.get('trophyLimit', 0)
        arena_name = arena.get('name', 'Unknown')
        
        # Determine trophy range
        if i == 0:
            start_trophies = 0
            end_trophies = trophy_limit - 1
        else:
            prev_arena = sorted_arenas[i-1]
            start_trophies = prev_arena.get('trophyLimit', 0)
            end_trophies = trophy_limit - 1
        
        arena_ranges[arena_num] = {
            'name': arena_name,
            'id': arena['id'],
            'start_trophies': start_trophies,
            'end_trophies': end_trophies,
            'trophy_limit': trophy_limit,
            'trophy_road': arena.get('trophyRoad', 'Unknown'),
            'required_king_level': arena.get('requiredKingLevel'),
            'arena_number': arena_num
        }
    
    return {
        'all_arenas': arenas,
        'main_progression_arenas': sorted_arenas,
        'arena_ranges': arena_ranges
    }

def print_arena_mapping(analysis: Dict[str, Any]):
    """Print comprehensive arena mapping"""
    arena_ranges = analysis['arena_ranges']
    main_arenas = analysis['main_progression_arenas']
    
    print(f"\n{'='*80}")
    print(f"🏆 CLASH ROYALE ARENA MAPPING")
    print(f"{'='*80}")
    print(f"Found {len(main_arenas)} main progression arenas")
    print(f"{'='*80}")
    
    print(f"\n{'Arena':^6} {'ID':^12} {'Name':<20} {'Trophy Range':<15} {'Trophy Limit':<12} {'King Level':<10}")
    print(f"{'-----':^6} {'----------':^12} {'----':<20} {'------------':<15} {'------------':<12} {'----------':<10}")
    
    for arena_num in sorted(arena_ranges.keys()):
        arena_info = arena_ranges[arena_num]
        trophy_range = f"{arena_info['start_trophies']}-{arena_info['end_trophies']}"
        
        print(f"{arena_num:^6} {arena_info['id']:^12} {arena_info['name']:<20} "
              f"{trophy_range:<15} {arena_info['trophy_limit']:<12} "
              f"{arena_info.get('required_king_level', 'N/A'):<10}")

def print_detailed_arena_info(analysis: Dict[str, Any]):
    """Print detailed information for each arena"""
    arena_ranges = analysis['arena_ranges']
    
    print(f"\n{'='*80}")
    print(f"📋 DETAILED ARENA INFORMATION")
    print(f"{'='*80}")
    
    for arena_num in sorted(arena_ranges.keys()):
        arena_info = arena_ranges[arena_num]
        
        print(f"\n🎯 Arena {arena_num}: {arena_info['name']}")
        print(f"   ID: {arena_info['id']}")
        print(f"   Trophy Range: {arena_info['start_trophies']} - {arena_info['end_trophies']}")
        print(f"   Trophy Limit: {arena_info['trophy_limit']}")
        print(f"   Trophy Road: {arena_info['trophy_road']}")
        if arena_info.get('required_king_level'):
            print(f"   Required King Level: {arena_info['required_king_level']}")
        
        # Find original arena data for additional info
        original_arena = None
        for arena in analysis['all_arenas']:
            if arena.get('id') == arena_info['id']:
                original_arena = arena
                break
        
        if original_arena:
            if original_arena.get('demoteTrophyLimit'):
                print(f"   Demote Trophy Limit: {original_arena['demoteTrophyLimit']}")
            if original_arena.get('chestRewardMultiplier'):
                print(f"   Chest Reward Multiplier: {original_arena['chestRewardMultiplier']}")

def print_api_usage_mapping(analysis: Dict[str, Any]):
    """Print mapping for API usage in our scraper"""
    arena_ranges = analysis['arena_ranges']
    
    print(f"\n{'='*80}")
    print(f"🔧 API USAGE MAPPING")
    print(f"{'='*80}")
    print("Use these Arena IDs in deckbuilder/search API calls:")
    print(f"{'='*80}")
    
    print(f"\n{'Arena':^6} {'API Arena ID':^15} {'Name':<20} {'Trophy Range':<15}")
    print(f"{'-----':^6} {'-------------':^15} {'----':<20} {'------------':<15}")
    
    for arena_num in sorted(arena_ranges.keys()):
        arena_info = arena_ranges[arena_num]
        trophy_range = f"{arena_info['start_trophies']}-{arena_info['end_trophies']}"
        
        print(f"{arena_num:^6} {arena_info['id']:^15} {arena_info['name']:<20} {trophy_range:<15}")

def save_arena_mapping(analysis: Dict[str, Any], filename: str = "arena_mapping.json"):
    """Save arena mapping to JSON file"""
    mapping_data = {
        'metadata': {
            'total_arenas': len(analysis['main_progression_arenas']),
            'scraping_timestamp': int(time.time()),
            'description': 'Clash Royale Arena Mapping from Game Data'
        },
        'arenas': analysis['arena_ranges']
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(mapping_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Arena mapping saved to {filename}")

def main():
    import time
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape Clash Royale arena mapping from game data')
    parser.add_argument('--save', action='store_true', help='Save mapping to JSON file')
    parser.add_argument('--output', default='arena_mapping.json', help='Output JSON filename')
    parser.add_argument('--detailed', action='store_true', help='Show detailed arena information')
    
    args = parser.parse_args()
    
    # Fetch and analyze arena data
    arenas = fetch_arena_mapping()
    if not arenas:
        return
    
    analysis = analyze_arenas(arenas)
    
    # Print various mappings
    print_arena_mapping(analysis)
    print_api_usage_mapping(analysis)
    
    if args.detailed:
        print_detailed_arena_info(analysis)
    
    # Save to file if requested
    if args.save:
        save_arena_mapping(analysis, args.output)

if __name__ == "__main__":
    main()
    