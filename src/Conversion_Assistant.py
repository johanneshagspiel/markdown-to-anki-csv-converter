import glob
import json
import os.path
import shutil
from pathlib import Path


class Conversion_Assistant:

    def __init__(self):

        self.path_to_anki_collection_folder = r"C:\Users\Johannes\AppData\Roaming\Anki2\User 1\collection.media"
        if len(self.path_to_anki_collection_folder) == 0:
            raise Exception("Please add the path to the collection.media folder of your Anki installation")

        root_path = Path(__file__).parents[1]
        self.resources_folder_path = root_path.joinpath("resources", "linkedin-skill-assessments-quizzes")
        self.json_folder = root_path.joinpath("resources", "json")

    def convert_markdown_to_markdown(self):

        sub_folders = [f.path for f in os.scandir(self.resources_folder_path) if f.is_dir()]

        symbols = ["[", "**"]
        prefixes = ["reas", "ref", "expl", "not", "exam", "simple", "tutorial"]

        check_list = []

        for symbol in symbols:
            for prefix in prefixes:
                temp = symbol + prefix
                check_list.append(temp)
                temp2 = symbol + prefix.capitalize()
                check_list.append(temp2)

        reasoning_tuple = tuple(check_list)

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
                    line_list = [line for line in markdown_file.readlines()]
                markdown_file.close()

                question_list = []
                frontText = ""
                backText = ""

                answer_found = False

                reasoning_found = False

                for line_index, line in enumerate(line_list):

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
                                    for file_ending in ["jpg", "png", "jpeg"]:

                                        final_image_name = f"{image_name}.{file_ending}"
                                        total_path_to_image = f"{folder_path}\\images\\{final_image_name}"

                                        if os.path.isfile(total_path_to_image):
                                            file_found = True
                                            store_image_name = f"{file_name}_{final_image_name}"
                                            anki_path = f"{self.path_to_anki_collection_folder}\\{store_image_name}"

                                            try:
                                                shutil.copy(total_path_to_image, anki_path)
                                                new_image_path_line = f"""<img src="{store_image_name}">"""
                                                line = before_part_cleaned + new_image_path_line + after_part_cleaned
                                            except Exception as e:
                                                print(f"{file_name}: Image copy error: {e} at line {line_index}")
                                            break
                                    if not file_found:
                                        print(f"{file_name}: No file ending found for line {line}")

                    if line.startswith("## "):
                        pass

                    elif line.startswith("####"):

                        answer_found = False
                        reasoning_found = False

                        if len(frontText) > 0:
                            question = {"front": f"{frontText[:-1]}", "back": f"{backText[:-1]}"}
                            question_list.append(question)

                            frontText = ""
                            backText = ""

                        # try:
                        #     question_line = line.split("#### Q")[1]
                        # except Exception as e1:
                        #     try:
                        #         question_line = line.split("#### ")[1]
                        #     except Exception as e2:
                        #         print(f"{file_name}: Question search error: {e2} in line {line}")
                        # question = re.split("[0-9]+.", question_line, maxsplit=1)[1].strip() + "\n"

                        try:
                            question = line.split("#### ")[1]
                        except Exception as e:
                            print(f"{file_name}: Question search error: {e} in line {line}")

                        frontText += "<b>" + question[:-1] + "</b>\n"

                    elif (line.startswith("- [ ] ")):
                        answer_found = False
                        reasoning_found = False

                        line = line.replace("- [ ] ","- ")

                        frontText += line

                    elif (line.startswith("- [x] ")):
                        answer_found = True
                        reasoning_found = False

                        line = line.replace("- [x] ","- ")
                        frontText += line

                        line = line[2:]
                        backText += line

                    elif (line.startswith(reasoning_tuple)):
                        reasoning_found = True
                        backText += "\n"
                        backText += line

                    else:
                        if line != "\n":

                            if reasoning_found:
                                backText += line
                            else:
                                frontText += line
                                if answer_found:
                                    backText += line

                if len(frontText) > 0:
                    question = {"front": f"{frontText[:-1]}", "back": f"{backText[:-1]}"}
                    question_list.append(question)

                json_file_name = file_name + ".json"
                json_file_path = str(self.json_folder) + "//" + json_file_name
                with open(json_file_path, "w") as json_file:
                    json_file.write(json.dumps(question_list, indent=4))
