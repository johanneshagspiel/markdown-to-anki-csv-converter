
class Question():

    def __init__(self, question, information, answer_option_list, answers, explanation):
        self.question = question
        self.information = information
        self.answer_option_list = answer_option_list

        self.answers = answers
        self.explanation = explanation

    def to_string(self):
        return f"""{self.question}
        {self.information}
        {[answer_option for answer_option in self.answer_option_list]}
        {[answer for answer in self.answers]}
        {self.explanation}
        """

    def to_csv_format(self):

        answer_option_text = "<ul>"
        for answer_option in self.answer_option_list:
            answer_option_text += f"<li>{answer_option}</li>"
        answer_option_text += "</ul>"

        if len(self.information) > 0:
            question_test = f"<b>{self.question}</b><br><br>{self.information}<br>{answer_option_text}"
        else:
            question_test = f"<b>{self.question}</b><br>{answer_option_text}"


        if len(self.answers) == 1:
            answer_text = self.answers[0]
        else:
            answer_text = "<ul>"
            for answer in self.answers:
                answer_text += f"<li>{answer}</li>"
            answer_text += "</ul>"

        if len(self.explanation) > 0:
            answer_text = f"{answer_text}<br><br>{self.explanation}"
        else:
            answer_text = f"{answer_text}"


        return {"question" : question_test, "answer" : answer_text}