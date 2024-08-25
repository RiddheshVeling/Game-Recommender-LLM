from google_play_scraper import search
import csv
import json

# Searched for Free, Best, Grossing and Paid
results = search(
    "Best games of 2023-2024",
    lang="en",
    country="us",
    n_hits=30  # max limit
)

def extract_game_info(game):
    return {
        'name': game.get('title', ''),
        'package_name': game.get('appId', ''),
        'description': game.get('description', ''),
        'icon_url': game.get('icon', ''),
        'genre': game.get('genre', ''),
        'rating': game.get('score', ''),
        # 'ratings': game.get('installs', '') wont work since documentation says it is outdated
    }

extracted_info = [extract_game_info(game) for game in results]

file = 'best_games.csv'
headers = ['name', 'package_name', 'description', 'icon_url', 'genre', 'rating', 'ratings']

with open(file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(extracted_info)

print("Successfully stored data into csv!")