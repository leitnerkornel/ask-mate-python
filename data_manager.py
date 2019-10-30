import datetime
import os
import connection
PATH = os.path.dirname(os.path.abspath(__file__))


def get_answers():
    ANSWER = f"{PATH}/sample_data/answer.csv"
    answers = connection.get_csv_data(ANSWER)
    return answers


def get_questions():
    QUESTION = f"{PATH}/sample_data/question.csv"
    questions = connection.get_csv_data(QUESTION)
    return questions

def convert_epoch_time(time):
    print(
        datetime.datetime.fromtimestamp(
            int(time)
        ).strftime('%Y-%m-%d %H:%M:%S')
    )
