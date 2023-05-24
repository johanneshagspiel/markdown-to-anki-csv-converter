import json
from src.Anki_Web_Helper import Anki_Web_Helper
from src.Conversion_Assistant import Conversion_Assistant

if __name__ == '__main__':

    deck_list = [("agile-methodologies-quiz", "Agile_Methodology_Quiz"),
                 ("git-quiz", "Git_Quiz"),
                 ("java-quiz", "Java_Quiz"),
                 ("mysql-quiz", "Mysql_Quiz"),
                 ("python-quiz", "Python_Quiz"),
                 ("reactjs-quiz", "React_Quiz"),
                 ("rest-api-quiz", "REST_Quiz"),
                 ("scala-quiz", "Scala_Quiz"),
                 ("spring-framework-quiz", "Spring_Quiz")]

    ca = Conversion_Assistant()
    ca.convert_markdown_to_csv()

    for file_name, deck_name in deck_list:
        ca.compare_new_to_old_csv(file_name=file_name, current_deck_name=deck_name)
