import csv
import glob
import json
import os.path
import re
import shutil
import sys
from pathlib import Path
from question import Question
from src.Anki_Web_Helper import Anki_Web_Helper


class Conversion_Assistant:

    def __init__(self):
        # In window,s this path is typically found at "C:\Users\@Username\AppData\Roaming\Anki2\@Username\collection.media"
        self.path_to_anki_collection_folder = r"C:\Users\Johannes\AppData\Roaming\Anki2\User 1\collection.media"

        if len(self.path_to_anki_collection_folder) == 0:
            raise Exception("Please add the path to the collection.media folder of your Anki installation")

        root_path = Path(__file__).parents[1]
        self.resources_folder_path = root_path.joinpath("resources", "linkedin-skill-assessments-quizzes")
        self.json_folder = root_path.joinpath("resources", "json")
        self.csv_folder = root_path.joinpath("resources", "csv_files")
        self.old_csv_folder = root_path.joinpath("resources", "old_csv_files")

    def convert_markdown_to_csv(self):

        sub_folders = [f.path for f in os.scandir(self.resources_folder_path) if f.is_dir()]

        for folder_path in sub_folders:
            markdown_search_string = str(folder_path) + "\\*.md"
            search_results = glob.glob(markdown_search_string)

            search_result = None
            if len(search_results) == 1:
                search_result = search_results[0]
            elif len(search_results) > 1:
                file_tuple = [(markdown_path, os.path.basename(markdown_path).split(".md")[0].split("-quiz")[-1]) for
                              markdown_path in search_results]
                search_result = [path for (path, file_name) in file_tuple if len(file_name) == 0][0]

            if search_result:
                markdown_file = search_result
                file_name = Path(markdown_file).stem
                print(f"Converting file \"{file_name}\"")

                with open(markdown_file, encoding='utf8') as markdown_file:
                    line_list = [line.strip() for line in markdown_file.readlines() if line != "\n"]
                markdown_file.close()

                questions = []

                question = ""
                information = ""
                answer_option_list = []
                answer_list = []
                explanation = ""
                multi_line_answer_mode = False
                multi_line_option_mode = False
                multi_line = ""

                first_time = True

                for line in line_list:

                    if "(images/" in line:
                        split_line = line.split("(images/")

                        if len(split_line) == 2:
                            before_part_dirty = split_line[0]
                            after_part_dirty = split_line[1]

                            before_part_split = before_part_dirty.split("!")
                            if len(before_part_split) == 2:
                                before_part_cleaned = before_part_split[0]

                                after_part_split = after_part_dirty.split(")")
                                if len(after_part_split) == 2:
                                    after_part_cleaned = after_part_split[1]

                                    image_name = after_part_split[0].split("?raw=")[0].split(".")[0]
                                    file_found = False
                                    for file_ending in [".jpg", ".png", ".jpeg"]:
                                        total_path_to_image = str(folder_path) + "\\images\\" + image_name + file_ending

                                        if os.path.isfile(total_path_to_image):
                                            file_found = True
                                            new_image_name = str(file_name) + "_" + str(image_name)
                                            anki_path = self.path_to_anki_collection_folder + "\\" + new_image_name + file_ending

                                            try:
                                                shutil.copy(total_path_to_image, anki_path)
                                                new_image_path_line = f"""<img src="{new_image_name}">"""
                                                line = before_part_cleaned + new_image_path_line + after_part_cleaned
                                            except Exception as e:
                                                None
                                    if not file_found:
                                        print("hi")

                    if line.startswith("####"):

                        if first_time:
                            first_time = False
                        else:

                            if multi_line_answer_mode and multi_line_option_mode:
                                answer_list.append(multi_line)
                                answer_option_list.append(multi_line)
                            elif multi_line_answer_mode:
                                answer_list.append(multi_line)
                            elif multi_line_option_mode:
                                answer_option_list.append(multi_line)

                            new_question = Question(question=question, information=information,
                                                    answer_option_list=answer_option_list, answers=answer_list,
                                                    explanation=explanation)
                            questions.append(new_question)

                            question = ""
                            information = ""
                            answer_option_list = []
                            answer_list = []
                            explanation = ""
                            multi_line_answer_mode = False
                            multi_line_option_mode = False
                            multi_line = ""

                        try:
                            question_line = line.split("#### Q")[1]
                        except Exception:
                            try:
                                question_line = line.split("#### ")[1]
                            except Exception as e:
                                print(e)

                        try:
                            question = re.split("[0-9]+.", question_line)[1]
                        except Exception as e:
                            print(line)
                            print(question_line)
                            print(e)
                            sys.exit()


                    elif line.startswith("- [ ] "):
                        if multi_line_answer_mode and multi_line_option_mode:
                            answer_list.append(multi_line)
                            answer_option_list.append(multi_line)
                            multi_line = ""
                            multi_line_answer_mode = False
                            multi_line_option_mode = False
                        elif multi_line_answer_mode:
                            answer_list.append(multi_line)
                            multi_line = ""
                            multi_line_answer_mode = False
                        elif multi_line_option_mode:
                            answer_option_list.append(multi_line)
                            multi_line = ""
                            multi_line_option_mode = False

                        answer_option = line.split("- [ ] ")[1]

                        multi_line_option_mode = True
                        multi_line += answer_option

                    elif line.startswith("- [x] "):
                        if multi_line_answer_mode and multi_line_option_mode:
                            answer_list.append(multi_line)
                            answer_option_list.append(multi_line)
                            multi_line = ""
                            multi_line_answer_mode = False
                            multi_line_option_mode = False
                        elif multi_line_answer_mode:
                            answer_list.append(multi_line)
                            multi_line = ""
                            multi_line_answer_mode = False
                        elif multi_line_option_mode:
                            answer_option_list.append(multi_line)
                            multi_line = ""
                            multi_line_option_mode = False

                        answer_option = line.split("- [x] ")[1]

                        multi_line_answer_mode = True
                        multi_line_option_mode = True
                        multi_line += answer_option

                    else:
                        if len(line) > 0:

                            if not first_time:

                                if line.startswith("**") or re.match("\[.*?\]\(.*?\)", line):
                                    if multi_line_answer_mode and multi_line_option_mode:
                                        answer_list.append(multi_line)
                                        answer_option_list.append(multi_line)
                                        multi_line = ""
                                        multi_line_answer_mode = False
                                        multi_line_option_mode = False
                                    elif multi_line_answer_mode:
                                        answer_list.append(multi_line)
                                        multi_line = ""
                                        multi_line_answer_mode = False
                                    elif multi_line_option_mode:
                                        answer_option_list.append(multi_line)
                                        multi_line = ""
                                        multi_line_option_mode = False

                                if multi_line_answer_mode or multi_line_option_mode:
                                    multi_line += line
                                    multi_line += "<br>"
                                elif len(answer_list) > 0:
                                    explanation += line
                                    explanation += "<br>"
                                else:
                                    information += line
                                    information += "<br>"

                csv_file_name = file_name + ".csv"
                csv_file_path = str(self.csv_folder) + "//" + csv_file_name
                with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=["question", "answer"])
                    for question in questions:
                        writer.writerow(question.to_csv_format())

                storage_str = [question.to_csv_format() for question in questions]
                json_file_name = file_name + ".json"
                json_file_path = str(self.json_folder) + "//" + json_file_name
                with open(json_file_path, "w") as json_file:
                    json_file.write(json.dumps(storage_str, indent=4))

    def compare_new_to_old_csv(self, file_name, current_deck_name):

        print(f"Loading Cards {file_name} / {current_deck_name}")

        awh = Anki_Web_Helper()

        new_json_path = str(self.json_folder) + "//" + file_name + ".json"

        new_json_list = []
        with open(new_json_path, "r") as new_json_file:
            new_json_list = json.loads(new_json_file.read())

        card_id_list = awh.getAllCardsFromDeck(current_deck_name)

        if len(card_id_list) == 0:
            awh.createDeck(deckName=current_deck_name)
            res = []
        else:
            res = awh.getInfoForCards(card_id_list)

        existing_card_dic = {entry["fields"]["Front"]["value"]: (entry["note"], entry["fields"]["Back"]["value"])  for entry in res}

        to_add_list = []
        to_delete_id_list = []
        to_delete_list = []
        for card_dic in new_json_list:
            newQuestion = card_dic["question"]
            newAnswer = card_dic["answer"]

            if newQuestion not in existing_card_dic:
                to_add_list.append((newQuestion, newAnswer))
            else:
                cardId, answer = existing_card_dic[newQuestion]

                if answer != newAnswer:
                    to_delete_list.append((newQuestion, newAnswer, cardId))
                    to_delete_id_list.append(cardId)

        for index, (question, answer, cardId) in enumerate(to_delete_list):
            print(f"Updating {index + 1} / {len(to_delete_list)}")

            noteDic = {
                "id" : cardId,
                "fields" : {
                    "Front" : question,
                    "Back" : answer
                }
            }
            awh.updateNote(noteDic=noteDic)

        for index, (question, answer) in enumerate(to_add_list):
            print(f"Adding {index + 1} / {len(to_add_list)}")

            noteDic = {
                "deckName" : current_deck_name,
                "modelName" : "Basic",
                "fields" : {
                    "Front" : question,
                    "Back" : answer
                }
            }

            try:
                awh.addNode(noteDic=noteDic)
            except Exception as e:
                print("Duplicate Note")
                print(json.dumps(noteDic, indent=4))
                print(" ")
