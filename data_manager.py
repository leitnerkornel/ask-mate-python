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
    question = cursor.fetchone()
    return question


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                        SELECT * FROM question
                        ORDER BY submission_time DESC;
                   """)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_last_five_question(cursor):
    cursor.execute("""
                   SELECT * FROM question
                   ORDER BY submission_time DESC
                   LIMIT 5;
                   """)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def add_question(cursor, question_title, question_message):
    cursor.execute("""
                        INSERT INTO question 
                        (title, message)
                        VALUES (%(question_title)s, %(question_message)s) ;
                       """,
                   {'question_title': question_title, 'question_message': question_message})


@connection.connection_handler
def save_answers_to_question(cursor, answer_text, question_id):
    cursor.execute("""
                        INSERT INTO answer(message, question_id)
                        VALUES (%(answer_text)s, %(question_id)s)
                    """,
                   {'answer_text': answer_text, 'question_id': question_id})


@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                        DELETE FROM question
                        WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})


def convert_epoch_time(time):
    return datetime.fromtimestamp(
        int(time)
    ).strftime('%Y-%m-%d %H:%M:%S')


def convert_linebreaks_to_br(original_str):
    return '<br>'.join(original_str.split('\n'))
