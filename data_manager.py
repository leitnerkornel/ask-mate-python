import connection
import os
from datetime import datetime

PATH = os.path.dirname(os.path.abspath(__file__))


@connection.connection_handler
def get_answers_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s;
                   """,
                   {'question_id': question_id})
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
                   """,
                   {'question_id': question_id})
    question = cursor.fetchall()
    return question


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                        SELECT * FROM question;
                       """)
    questions = cursor.fetchall()
    return questions


def convert_epoch_time(time):
    return datetime.fromtimestamp(
        int(time)
    ).strftime('%Y-%m-%d %H:%M:%S')


def generate_next_id(list_of_q_or_a):
    return str(int(list_of_q_or_a[-1]['id']) + 1)


def convert_linebreaks_to_br(original_str):
    return '<br>'.join(original_str.split('\n'))
