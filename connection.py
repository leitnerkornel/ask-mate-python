import csv
import os
PATH = os.path.dirname(os.path.abspath(__file__))
ANSWERS = f"{PATH}/sample_data/answer.csv"
QUESTIONS = f"{PATH}/sample_data/question.csv"


def get_answers():
    answers = []
    with open(ANSWERS) as csv_file:
        reader = csv.DictReader(csv_file)
        for item in reader:
            answers.append(dict(item))
    return answers


def get_questions():
    questions = []
    with open(QUESTIONS) as csv_file:
        reader = csv.DictReader(csv_file)
        for item in reader:
            questions.append(dict(item))
    return questions
