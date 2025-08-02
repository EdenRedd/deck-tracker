# So we need to generalize the code
#Game start logs in erro log.txt OnMatchmakingMatchFound
#Game end logs in erro log.txt RemoteGame|SendRequestObject|RequestType=CubeGame.AckGameResultRequest
import os
import json
import time

#Have to replace these hardcoded paths with a way to work for any user
collectionLogs = r"C:\Users\ojeda\AppData\LocalLow\Second Dinner\SNAP\Standalone\States\nvprod\CollectionState.json"
playStateLogs = r"C:\Users\ojeda\AppData\LocalLow\Second Dinner\SNAP\Standalone\States\nvprod\PlayState.json"
liveLogs = r"C:\Users\ojeda\AppData\LocalLow\Second Dinner\SNAP\ErrorLog.txt"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def GetCardsInDeck():
    deck_cards = []
    with open(collectionLogs, 'r', encoding='utf-8-sig') as file:
        collection_data = json.load(file)
    with open(playStateLogs, 'r', encoding='utf-8-sig') as file:
        play_state_data = json.load(file)

    deckId = play_state_data['SelectedDeckId']['Value']

    for deck in collection_data['ServerState']['Decks']:
        if deck['Id'] == deckId:
            for card in deck['Cards']:
                if 'CardDefId' in card:
                    deck_cards.append(card['CardDefId'])
                else:
                    print(f"Card without CardDefId found: {card}")
    
    return deck_cards

list_of_cards = []
cardsLeftInDeck = []

START_GAME_KEYWORD = "OnMatchmakingMatchFound"
END_GAME_KEYWORD = "GameManager|OnLeaveGameScene"
canContinue = False

while not os.path.exists(liveLogs):
    print("Waiting for log file...")
    time.sleep(1)

with open(liveLogs, 'r', encoding= 'utf-8-sig') as file:
    file.seek(0, os.SEEK_END)
    print("Watching log for trigger...")
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
       
        if START_GAME_KEYWORD in line:
            list_of_cards = GetCardsInDeck()
            clear_screen()
            print(GetCardsInDeck())
            cardsLeftInDeck = list_of_cards.copy()
            print("✅ Match started! Found line:", line.strip()) #Start rendering the deck
            canContinue = True

        if canContinue and any((card + (".asset|DrawCard")) in line for card in list_of_cards):
            for card in list_of_cards:
                if card in line and card in cardsLeftInDeck:
                    cardsLeftInDeck.remove(card)
                    print("Current deck:", cardsLeftInDeck)


        if END_GAME_KEYWORD in line:
            list_of_cards.clear()
            cardsLeftInDeck.clear()
            canContinue = False
            print("✅ Match ended! Found line:", line.strip()) #Stop rendering the deck
