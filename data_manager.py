import connection
from psycopg2 import sql
from datetime import datetime
import bcrypt


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
def add_question(cursor, question_title, question_message, submission_time, name, user_id):
    cursor.execute("""  
                        ALTER TABLE question ADD COLUMN IF NOT EXISTS username text;
                        ALTER TABLE question ADD COLUMN IF NOT EXISTS user_id integer;
                        INSERT INTO question (title, message, submission_time, username, user_id)
                        VALUES (%(question_title)s, %(question_message)s, %(submission_time)s, %(name)s, %(user_id)s);
                       """,
                   {'question_title': question_title, 'question_message': question_message,
                    'submission_time': submission_time, 'name': name, 'user_id': user_id})


@connection.connection_handler
def update_question(cursor, question_id, question_title, question_message, submission_time):
    cursor.execute("""
                    UPDATE question
                    SET title = %(question_title)s, message = %(question_message)s,
                    submission_time = %(submission_time)s
                    WHERE id = %(question_id)s;
    """,
                   {'question_title': question_title, 'question_message': question_message, 'question_id': question_id,
                    'submission_time': submission_time})


@connection.connection_handler
def save_answers_to_question(cursor, answer_text, question_id, submission_time, name, user_id):
    cursor.execute("""
                        ALTER TABLE answer ADD COLUMN IF NOT EXISTS username text;
                        ALTER TABLE answer ADD COLUMN IF NOT EXISTS user_id integer;
                        INSERT INTO answer(message, question_id, submission_time, username, user_id)
                        VALUES (%(answer_text)s, %(question_id)s, %(submission_time)s, %(name)s, %(user_id)s);
                    """,
                   {'answer_text': answer_text, 'question_id': question_id, 'submission_time': submission_time,
                    'name': name, 'user_id': user_id})


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
def delete_answer(cursor, answer_id, question_id):
    cursor.execute("""
                        DELETE FROM answer
                        WHERE id = %(answer_id)s AND
                        question_id = %(question_id)s;
                    """,
                   {'answer_id': answer_id, 'question_id': question_id})


@connection.connection_handler
def search_in_questions(cursor, search_phrase):
    cursor.execute("""
                       SELECT * FROM question
                       WHERE lower(message) LIKE lower(%(search_phrase)s) OR lower(title) LIKE lower(%(search_phrase)s);
                       """,
                   {'search_phrase': "%" + search_phrase + "%"})
    questions = cursor.fetchall()
    return questions

@connection.connection_handler
def search_in_answers(cursor, search_phrase):
    cursor.execute("""
                       SELECT a.message, q.id, q.title FROM answer AS a JOIN question AS q ON a.question_id = q.id
                       WHERE lower(a.message) LIKE lower(%(search_phrase)s);
                       """,
                   {'search_phrase': "%" + search_phrase + "%"})
    answers = cursor.fetchall()
    return answers


def convert_linebreaks_to_br(original_str):
    return '<br/>'.join(original_str.split('\n'))


@connection.connection_handler
def new_comment(cursor, com, question_id, submission_time):
    cursor.execute("""
                    INSERT INTO comment
                    (message, question_id, submission_time)
                    VALUES (%(com)s, %(question_id)s, %(submission_time)s)
    """,
                   {'com': com, 'question_id': question_id, 'submission_time': submission_time})


@connection.connection_handler
def get_comments_by_q_id(cursor, question_id):
    cursor.execute("""
                        SELECT submission_time, message FROM comment
                        WHERE question_id = %(question_id)s;
                       """,
                   {'question_id': question_id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def register_user(cursor, username, password, reg_date):
    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS public.users ( 
                        id serial constraint users_pk primary key,
                        username text,
                        password text,
                        reg_date timestamp without time zone,
                        reputation int);
                        INSERT INTO users(username, password, reg_date)
                        VALUES (%(username)s, %(password)s, %(reg_date)s)
                    """,
                   {'username': username, 'password': password, 'reg_date': reg_date})


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@connection.connection_handler
def get_username_by_id(cursor, user_id):
    cursor.execute("""
                    SELECT username FROM users
                    WHERE id = %(user_id)s;
                   """,
                   {'user_id': user_id})
    question = cursor.fetchone()
    return question


@connection.connection_handler
def get_user_id_by_username(cursor, username):
    cursor.execute("""
                    SELECT username FROM users
                    WHERE username = %(username)s;
                   """,
                   {'username': username})
    question = cursor.fetchone()
    return question

