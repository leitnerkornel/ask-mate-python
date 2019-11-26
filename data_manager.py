import connection
from datetime import datetime


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
def get_questions(cursor, order_by):
    cursor.execute(f"""
                        SELECT * FROM question
                        ORDER BY {order_by};
                        """)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_numbered_question(cursor, numb_limit):
    cursor.execute("""
                   SELECT * FROM question
                   ORDER BY submission_time DESC
                   LIMIT %(numb_limit)s;
                   """,
                   {'numb_limit': numb_limit})
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def add_question(cursor, question_title, question_message, submission_time):
    cursor.execute("""
                        INSERT INTO question 
                        (title, message, submission_time)
                        VALUES (%(question_title)s, %(question_message)s, %(submission_time)s) ;
                       """,
                   {'question_title': question_title, 'question_message': question_message,
                    'submission_time': submission_time})


@connection.connection_handler
def save_answers_to_question(cursor, answer_text, question_id, submission_time):
    cursor.execute("""
                        INSERT INTO answer(message, question_id, submission_time)
                        VALUES (%(answer_text)s, %(question_id)s, %(submission_time)s)
                    """,
                   {'answer_text': answer_text, 'question_id': question_id, 'submission_time': submission_time})


@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                        DELETE FROM question
                        WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})


def get_time():
    now = datetime.utcnow()
    return now.strftime('%Y-%m-%d %H:%M:%S')


@connection.connection_handler
def delete_answer(cursor, question_id):
    cursor.execute("""
                        DELETE FROM answer
                        WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})


def convert_linebreaks_to_br(original_str):
    return '<br/>'.join(original_str.split('\n'))
