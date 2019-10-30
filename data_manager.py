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
    return datetime.datetime.fromtimestamp(
            int(time)
        ).strftime('%Y-%m-%d %H:%M:%S')


def generate_next_id(list_of_q_or_a):
    return str(int(list_of_q_or_a[-1]['id']) + 1)




