import csv
import glob
import re
from pathlib import Path

from question import Question

if __name__ == '__main__':
    _root = Path(__file__).parents[1]
    _resources_path = _root.joinpath("linkedin-skill-assessments-quizzes")

    folder_path = _resources_path.joinpath("git")
    markdown_search_string = str(folder_path) + "\\*.md"
    markdown_file = glob.glob(markdown_search_string)[0]

    file_name = Path(markdown_file).stem

    with open(markdown_file) as markdown_file:
        line_list = [line.strip() for line in markdown_file.readlines() if line != "\n"]
    markdown_file.close()

    questions = []

    question = ""
    information = ""
    answer_option_list = []
    answers = []
    explanation = ""

    first_time = True

    for line in line_list:

        if line.startswith("####"):

            if first_time:
                first_time = False
            else:
                new_question = Question(question = question, information=information,
                                        answer_option_list=answer_option_list, answers=answers, explanation =explanation)
                questions.append(new_question)

                question = ""
                information = ""
                answer_option_list = []
                answers = []
                explanation = ""

            question_line = line.split("### Q")[1]
            question = re.split("[0-9]+. ", question_line)[1]

        elif line.startswith("- [ ] "):
            answer_option = line.split("- [ ] ")[1]
            answer_option_list.append(answer_option)

        elif line.startswith("- [x] "):
            answer_option = line.split("- [x] ")[1]
            answer_option_list.append(answer_option)
            answers.append(answer_option)
        else:
            if len(line) > 0:
                if len(answers) > 0:
                    explanation += line
                    explanation += "<br>"
                else:
                    information += line
                    information += "<br>"

    csv_file_name = file_name + ".csv"
    file_path = str(folder_path) + "//" + csv_file_name
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["question", "answer"])
        writer.writeheader()
        for question in questions:
            writer.writerow(question.to_csv_format())
