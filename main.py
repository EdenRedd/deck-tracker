#Access the game state log file
import os
import json

file_path = r"C:\Users\ojeda\AppData\LocalLow\Second Dinner\SNAP\Standalone\States\nvprod\GameState.json"

with open(file_path, 'r', encoding= 'utf-8-sig') as file:
    game_state = json.load(file)

list_of_cards = []

cards = game_state['RemoteGame']['GameState']['ClientResultMessage']['GameResultAccountItems'][0]['Deck']['Cards']

for card in cards:
    list_of_cards.append(card['CardDefId'])

print(list_of_cards)

#print(game_state['RemoteGame']['GameState']['ClientResultMessage']['GameResultAccountItems'][0]['Deck']['Cards'])