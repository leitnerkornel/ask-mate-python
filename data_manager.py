import datetime
import os
import connection

PATH = os.path.dirname(os.path.abspath(__file__))


def get_answers():
    ANSWER = f"{PATH}/sample_data/answer.csv"
    answers = connection.get_csv_data(ANSWER)
    for answer in answers:
        answer['message'] = convert_linebreaks_to_br(answer['message'])
    for answer in answers:
        answer['submission_time'] = convert_epoch_time(answer['submission_time'])
    return answers


def get_questions():
    QUESTIONPATH = f"{PATH}/sample_data/question.csv"
    questions = connection.get_csv_data(QUESTIONPATH)
    for question in questions:
        question['message'] = convert_linebreaks_to_br(question['message'])
    for question in questions:
        question['submission_time'] = convert_epoch_time(question['submission_time'])
    return questions


def convert_epoch_time(time):
    return datetime.datetime.fromtimestamp(
            int(time)
        ).strftime('%Y-%m-%d %H:%M:%S')


def generate_next_id(list_of_q_or_a):
    return str(int(list_of_q_or_a[-1]['id']) + 1)

def convert_linebreaks_to_br(original_str):
    return '<br>'.join(original_str.split('\n'))




