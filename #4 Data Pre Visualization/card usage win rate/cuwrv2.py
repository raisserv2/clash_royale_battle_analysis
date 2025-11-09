import csv
from collections import defaultdict
import ast
import json
import pandas as pd
import pickle

# Initialize counters
card_usage_counter = defaultdict(int)  # Unique player-deck combinations
card_win_counter = defaultdict(int)    # Cards in winning decks
card_total_plays_counter = defaultdict(int)  # Total times card was played (for win percentage)

# Track unique player-deck combinations to avoid duplicates for usage counter
player_deck_combinations = set()

print("Processing Clash Royale battle data...")

# Read the CSV file
with open('../../#2 Data Storage/Processed Data/fullbatch.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        # Get player identifiers and winner status
        player0_hashtag = row['players_0_hashtag']
        player1_hashtag = row['players_1_hashtag']
        player0_winner = int(row['players_0_winner'])
        player1_winner = int(row['players_1_winner'])
        
        # Process player 0's deck
        player0_spells = row['players_0_spells']
        
        # Process player 1's deck  
        player1_spells = row['players_1_spells']
        
        # Parse the spells strings into actual lists
        try:
            player0_cards_list = ast.literal_eval(player0_spells)
            player1_cards_list = ast.literal_eval(player1_spells)
        except:
            print(f"Error parsing spells for row: {row.get('replayTag', 'Unknown')}")
            continue
        
        # Create unique identifiers for player-deck combinations
        player0_deck_id = (player0_hashtag, tuple(sorted([card[0] for card in player0_cards_list if isinstance(card, tuple) and len(card) > 0])))
        player1_deck_id = (player1_hashtag, tuple(sorted([card[0] for card in player1_cards_list if isinstance(card, tuple) and len(card) > 0])))
        
        # Extract unique cards from both players' decks
        player0_unique_cards = set()
        for card_tuple in player0_cards_list:
            if isinstance(card_tuple, tuple) and len(card_tuple) > 0:
                card_name = card_tuple[0]
                player0_unique_cards.add(card_name)
        
        player1_unique_cards = set()
        for card_tuple in player1_cards_list:
            if isinstance(card_tuple, tuple) and len(card_tuple) > 0:
                card_name = card_tuple[0]
                player1_unique_cards.add(card_name)
        
        # Process player 0 for USAGE counter - only count if we haven't seen this player with this deck before
        if player0_deck_id not in player_deck_combinations:
            player_deck_combinations.add(player0_deck_id)
            
            # Add to usage counter
            for card in player0_unique_cards:
                card_usage_counter[card] += 1
        
        # Process player 1 for USAGE counter - only count if we haven't seen this player with this deck before
        if player1_deck_id not in player_deck_combinations:
            player_deck_combinations.add(player1_deck_id)
            
            # Add to usage counter
            for card in player1_unique_cards:
                card_usage_counter[card] += 1
        
        # Process player 0 for TOTAL PLAYS counter and WIN counter
        for card in player0_unique_cards:
            card_total_plays_counter[card] += 1
            
            if player0_winner == 1:  # Player 0 won
                card_win_counter[card] += 1
        
        # Process player 1 for TOTAL PLAYS counter and WIN counter
        for card in player1_unique_cards:
            card_total_plays_counter[card] += 1
            
            if player1_winner == 1:  # Player 1 won
                card_win_counter[card] += 1

# Convert to regular dictionaries for easier handling
card_usage_dict = dict(card_usage_counter)
card_win_dict = dict(card_win_counter)
card_total_plays_dict = dict(card_total_plays_counter)

# Calculate win percentages
card_win_percentage_dict = {}
for card in card_total_plays_dict:
    if card_total_plays_dict[card] > 0:
        win_percentage = (card_win_dict.get(card, 0) / card_total_plays_dict[card]) * 100
        card_win_percentage_dict[card] = round(win_percentage, 2)

print("Processing complete! Saving data to files...")

# Save data to JSON files for easy access
with open('card_usage_data.json', 'w') as f:
    json.dump(card_usage_dict, f, indent=2)

with open('card_win_data.json', 'w') as f:
    json.dump(card_win_dict, f, indent=2)

with open('card_total_plays_data.json', 'w') as f:
    json.dump(card_total_plays_dict, f, indent=2)

with open('card_win_percentage_data.json', 'w') as f:
    json.dump(card_win_percentage_dict, f, indent=2)

# Save as pickle for Python object preservation
with open('clash_royale_data.pkl', 'wb') as f:
    pickle.dump({
        'usage': card_usage_dict,
        'wins': card_win_dict,
        'total_plays': card_total_plays_dict,
        'win_percentage': card_win_percentage_dict,
        'unique_decks': len(player_deck_combinations)
    }, f)

# Create a comprehensive DataFrame for visualization
card_data = []
for card in set(card_usage_dict.keys()) | set(card_win_percentage_dict.keys()):
    card_data.append({
        'card': card,
        'usage_count': card_usage_dict.get(card, 0),
        'win_count': card_win_dict.get(card, 0),
        'total_plays': card_total_plays_dict.get(card, 0),
        'win_percentage': card_win_percentage_dict.get(card, 0)
    })

df = pd.DataFrame(card_data)
df.to_csv('clash_royale_card_stats.csv', index=False)
df.to_pickle('clash_royale_card_stats.pkl')

# Print summary statistics
print("\n" + "="*50)
print("DATA PROCESSING SUMMARY")
print("="*50)
print(f"Total unique cards: {len(card_usage_dict)}")
print(f"Total card appearances in unique decks: {sum(card_usage_dict.values())}")
print(f"Unique player-deck combinations: {len(player_deck_combinations)}")
print(f"Total card plays: {sum(card_total_plays_dict.values())}")
print(f"Total winning card appearances: {sum(card_win_dict.values())}")

print("\n" + "="*50)
print("TOP CARDS SUMMARY")
print("="*50)

print("\nTop 10 Most Used Cards (Unique per Player-Deck):")
sorted_usage = sorted(card_usage_dict.items(), key=lambda x: x[1], reverse=True)
for i, (card, count) in enumerate(sorted_usage[:10], 1):
    print(f"{i}. {card}: {count}")

print("\nTop 10 Highest Win Rate Cards (min 100 plays):")
filtered_win_rates = {card: rate for card, rate in card_win_percentage_dict.items() 
                     if card_total_plays_dict.get(card, 0) >= 100}
sorted_win_rates = sorted(filtered_win_rates.items(), key=lambda x: x[1], reverse=True)
for i, (card, rate) in enumerate(sorted_win_rates[:10], 1):
    plays = card_total_plays_dict.get(card, 0)
    wins = card_win_dict.get(card, 0)
    print(f"{i}. {card}: {rate}% ({wins}/{plays} plays)")

print("\n" + "="*50)
print("FILES SAVED:")
print("="*50)
print("1. card_usage_data.json - Card usage counts")
print("2. card_win_data.json - Card win counts") 
print("3. card_total_plays_data.json - Total plays per card")
print("4. card_win_percentage_data.json - Win percentages")
print("5. clash_royale_data.pkl - All data as Python object")
print("6. clash_royale_card_stats.csv - Comprehensive DataFrame")
print("7. clash_royale_card_stats.pkl - DataFrame as pickle")

print("\nData is now ready for visualization!")