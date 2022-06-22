import csv
import glob
import os.path
import re
import shutil
from pathlib import Path

from question import Question

if __name__ == '__main__':

    # In window,s this path is typically found at "C:\Users\@Username\AppData\Roaming\Anki2\@Username\collection.media"
    path_to_anki_collection_folder = r""

    if len(path_to_anki_collection_folder) == 0:
        raise Exception("Please add the path to the collection.media folder of your Anki installation")

    root_path = Path(__file__).parents[1]
    resources_folder_path = root_path.joinpath("resources", "linkedin-skill-assessments-quizzes")
    storage_folder = root_path.joinpath("resources", "csv_files")

    sub_folders = [f.path for f in os.scandir(resources_folder_path) if f.is_dir()]

    for folder_path in sub_folders:
        markdown_search_string = str(folder_path) + "\\*.md"
        search_results = glob.glob(markdown_search_string)

        if len(search_results) == 1:
            markdown_file = search_results[0]
            file_name = Path(markdown_file).stem

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

                                image_name = after_part_split[0]
                                total_path_to_image = str(folder_path) + "//images//" + image_name

                                if os.path.isfile(total_path_to_image):
                                    anki_path = path_to_anki_collection_folder + "//" + str(image_name)

                                    try:
                                        shutil.copy(total_path_to_image, anki_path)
                                        new_image_path_line = f"""<img src="{image_name}">"""
                                        line = before_part_cleaned + new_image_path_line + after_part_cleaned
                                    except Exception as e:
                                        None

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

                        new_question = Question(question = question, information=information,
                                                answer_option_list=answer_option_list, answers=answer_list, explanation =explanation)
                        questions.append(new_question)

                        question = ""
                        information = ""
                        answer_option_list = []
                        answer_list = []
                        explanation = ""
                        multi_line_answer_mode = False
                        multi_line_option_mode = False
                        multi_line = ""

                    question_line = line.split("### Q")[1]
                    question = re.split("[0-9]+.", question_line)[1]

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
            file_path = str(storage_folder) + "//" + csv_file_name
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["question", "answer"])
                for question in questions:
                    writer.writerow(question.to_csv_format())
