import json
from pathlib import Path

from src.Anki_Web_Helper import Anki_Web_Helper


class Anki_Deck_Manipulator:

    def __init__(self):
        self.path_to_anki_collection_folder = r"C:\Users\Johannes\AppData\Roaming\Anki2\User 1\collection.media"

        if len(self.path_to_anki_collection_folder) == 0:
            raise Exception("Please add the path to the collection.media folder of your Anki installation")

        root_path = Path(__file__).parents[1]
        self.resources_folder_path = root_path.joinpath("resources", "linkedin-skill-assessments-quizzes")
        self.json_folder = root_path.joinpath("resources", "json")

        self.awh = Anki_Web_Helper()
    def add_new_json_to_deck(self, file_name, current_deck_name):

        print(f"Loading Cards {file_name} / {current_deck_name}")

        new_json_path = str(self.json_folder) + "//" + file_name + ".json"

        new_json_list = []
        with open(new_json_path, "r") as new_json_file:
            new_json_list = json.loads(new_json_file.read())

        card_id_list = self.awh.getAllCardsFromDeck(current_deck_name)

        if len(card_id_list) == 0:
            self.awh.createDeck(deckName=current_deck_name)
            res = []
        else:
            res = self.awh.getInfoForCards(card_id_list)

        existing_card_dic = {entry["fields"]["Front"]["value"]: (entry["note"], entry["fields"]["Back"]["value"])  for entry in res}

        to_add_list = []
        to_delete_id_list = []
        to_delete_list = []
        for card_dic in new_json_list:
            newFront = card_dic["front"]
            newBack = card_dic["back"]

            if newFront not in existing_card_dic:
                to_add_list.append((newFront, newBack))
            else:
                cardId, back = existing_card_dic[newFront]

                if back != newBack:
                    to_delete_list.append((newFront, newBack, cardId))
                    to_delete_id_list.append(cardId)

        for index, (front, back, cardId) in enumerate(to_delete_list):
            print(f"Updating {index + 1} / {len(to_delete_list)}")

            noteDic = {
                "id" : cardId,
                "fields" : {
                    "Front" : front,
                    "Back" : back
                }
            }
            self.awh.updateNote(noteDic=noteDic)

        for index, (front, back) in enumerate(to_add_list):
            print(f"Adding {index + 1} / {len(to_add_list)}")

            noteDic = {
                "deckName" : current_deck_name,
                "modelName" : "KaTeX and Markdown Basic",
                "fields" : {
                    "Front" : front,
                    "Back" : back
                }
            }

            try:
                self.awh.addNode(noteDic=noteDic)
            except Exception as e:
                print("Duplicate Note")
                print(json.dumps(noteDic, indent=4))
                print(" ")
