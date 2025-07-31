# So we need to generalize the code
#Game start logs in erro log.txt OnMatchmakingMatchFound
#Game end logs in erro log.txt RemoteGame|SendRequestObject|RequestType=CubeGame.AckGameResultRequest
import os
import json
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

list_of_cards = []
cardsLeftInDeck = list_of_cards.copy()
def GetCardsInDeck():
    with open(collectionLogs, 'r', encoding='utf-8-sig') as file:
        collection_data = json.load(file)
    with open(playStateLogs, 'r', encoding='utf-8-sig') as file:
        play_state_data = json.load(file)

    deckId = play_state_data['SelectedDeckId']['Value']

    for deck in collection_data['ServerState']['Decks']:
        if deck['Id'] == deckId:
            for card in deck['Cards']:
                if 'CardDefId' in card:
                    list_of_cards.append(card['CardDefId'])
                else:
                    print(f"Card without CardDefId found: {card}")
    
    return list_of_cards
#
collectionLogs = r"C:\Users\ojeda\AppData\LocalLow\Second Dinner\SNAP\Standalone\States\nvprod\CollectionState.json"
playStateLogs = r"C:\Users\ojeda\AppData\LocalLow\Second Dinner\SNAP\Standalone\States\nvprod\PlayState.json"
liveLogs = r"C:\Users\ojeda\AppData\LocalLow\Second Dinner\SNAP\ErrorLog.txt"

TRIGGER_KEYWORD = "OnMatchmakingMatchFound"
END_KEYWORD = "GameResultsEntry"
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
       
        if TRIGGER_KEYWORD in line:
            clear_screen()
            print(GetCardsInDeck())
            cardsLeftInDeck = list_of_cards.copy()
            print("✅ Match started! Found line:", line.strip()) #Start rendering the deck
            canContinue = True

        for card in list_of_cards:
            if canContinue and card in line:
                if card in cardsLeftInDeck:
                    cardsLeftInDeck.remove(card)
                    print("Current deck:", cardsLeftInDeck)


        if END_KEYWORD in line:
            print("✅ Match ended! Found line:", line.strip()) #Stop rendering the deck



list_of_cards = []

cards = game_state['RemoteGame']['GameState']['ClientResultMessage']['GameResultAccountItems'][0]['Deck']['Cards']

for card in cards:
    list_of_cards.append(card['CardDefId'])




while True:
    clear_screen()
    print(list_of_cards)

#print(game_state['RemoteGame']['GameState']['ClientResultMessage']['GameResultAccountItems'][0]['Deck']['Cards'])