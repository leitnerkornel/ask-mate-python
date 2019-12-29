import bcrypt
import data_manager


def page_title_from_question_title(question, max_word):
    return " ".join(question['title'].split()[:max_word])


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def is_username_free(username, registered_users):
    if registered_users is None:
        return True
    else:
        return False
