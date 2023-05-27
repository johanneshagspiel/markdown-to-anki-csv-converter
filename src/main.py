import json

from src.Anki_Deck_Manipulator import Anki_Deck_Manipulator
from src.Anki_Web_Helper import Anki_Web_Helper
from src.Conversion_Assistant import Conversion_Assistant

if __name__ == '__main__':

    ca = Conversion_Assistant()
    ca.convert_markdown_to_markdown()

    deck_list = [("agile-methodologies-quiz", "Agile_Methodology_Quiz"),
                 ("git-quiz", "Git_Quiz"),
                 ("java-quiz", "Java_Quiz"),
                 ("mysql-quiz", "Mysql_Quiz"),
                 ("python-quiz", "Python_Quiz"),
                 ("reactjs-quiz", "React_Quiz"),
                 ("rest-api-quiz", "REST_Quiz"),
                 ("scala-quiz", "Scala_Quiz"),
                 ("spring-framework-quiz", "Spring_Quiz")]

    adm = Anki_Deck_Manipulator()
    for file_name, deck_name in deck_list:
        adm.add_new_json_to_deck(file_name=file_name, current_deck_name=deck_name)
