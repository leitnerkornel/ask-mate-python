from flask import Flask, render_template, request, redirect, session

import data_manager
import util

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# This will come from session.
logged_user_id = 5

logged_user = "kornel"


def login_by_hand(user):
    session['username'] = user
    return "You are successfully logged."


def current_user():
    return session.get('username', "Anonymous")


@app.route('/login_test/<user>')
def login_test(user):
    session['username'] = user
    print(session['username'])
    return "You are successfully logged."


@app.route('/')
def index_last_numbered_question():
    question_limit = 5
    numbered_question = data_manager.get_numbered_question(question_limit)
    return render_template("index.html", questions=numbered_question, question_limit=question_limit)


@app.route('/list')
def all_question():
    order_by = request.args.get('order')
    questions = data_manager.get_questions(order_by)

    return render_template("all_question.html", questions=questions)


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == "GET":
        return render_template('message.html')

    question_title = request.form['title']
    question_message = request.form['note']
    username = data_manager.get_username_by_id(logged_user_id)  # This will come from session.
    data_manager.add_question(question_title, question_message,
                              username['username'], logged_user_id)
    return redirect('/')


@app.route('/question/<question_id>/update-question', methods=['POST', 'GET'])
def route_update_question(question_id):
    if request.method == "POST":
        question_title = request.form['title']
        question_message = request.form['message']
        data_manager.update_question(question_id, question_title, question_message)
        return redirect(f'/question/{question_id}')

    question = data_manager.get_question_by_id(question_id)
    return render_template('update.html', question=question)


@app.route('/answer/<answer_id>/update-answer', methods=['POST', 'GET'])
def route_update_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    if request.method == "POST":
        answer_message = request.form['message']
        data_manager.update_answer(answer_id, answer_message)
        return redirect('/list')
    return render_template('update-answer.html', answer=answer, answer_id=answer_id)


@app.route('/question/<question_id>', methods=['GET'])
def route_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    comment = data_manager.get_comments_by_q_id(question_id)
    question_title = util.page_title_from_question_title(question, max_word=4)
    return render_template('question.html', question=question, answers=answers, comment=comment,
                           question_title=question_title)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_answer(question_id)
    data_manager.delete_question(question_id)
    return redirect('/')


@app.route('/question/<question_id>/<answer_id>/delete-answer')
def delete_answer_alone(answer_id, question_id):
    data_manager.delete_answer(answer_id, question_id)
    return redirect(f"/question/{question_id}")


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_post_answer(question_id):
    if request.method == 'GET':
        question = data_manager.get_question_by_id(question_id)
        return render_template('answer.html', question=question)

    saved_answer = request.form['answer']
    username = data_manager.get_username_by_id(logged_user_id)  # This will come from session.
    data_manager.save_answers_to_question(saved_answer, question_id,
                                          username['username'], logged_user_id)
    return redirect(f"/question/{question_id}")


@app.route('/search')
def list_search_result():
    search_phrase = request.args.get('q')
    if search_phrase:
        questions = data_manager.search_in_questions(search_phrase)
        answers = data_manager.search_in_answers(search_phrase)
    else:
        questions = ""
        answers = ""
        search_phrase = "Sorry, it was an empty search"
    return render_template('search_result.html', search_phrase=search_phrase, questions=questions, answers=answers)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def route_comment_to_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'POST':
        saved_comment = request.form['com']
        data_manager.add_comment_to_question(saved_comment, question_id)
        return redirect(f"/question/{question_id}")
    return render_template('comment.html', question=question)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def route_comment_to_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    comment = data_manager.get_comments_by_a_id(answer_id)
    if request.method == 'POST':
        saved_comment = request.form['com']
        data_manager.add_comment_to_answer(saved_comment, answer_id)
        return redirect('/list')
    return render_template('comment_ans.html', answer=answer, comment=comment)


@app.route('/registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        username = request.form['username']
        password = util.hash_password(request.form['pwd1'])
        registered_users = data_manager.get_usernames_by_username(username)
        if util.is_username_free(username, registered_users):
            success = f"The registration was successful. You can log in with {username}."
            data_manager.register_user(username, password)
            return render_template('login.html', message=success)
        else:
            error = f"The username: {username} is already taken. Try again."
            return render_template('registration.html', message=error)
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        stored_password = data_manager.get_data_linked_to_username(username)
        password_input = request.form['pwd']
        valid_password = util.verify_password(password_input, stored_password)
        if valid_password:
            logged_user_id = data_manager.get_data_linked_to_username(username)
            return redirect('/')
        else:
            print('Itt te nem jutsz át!')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=7000,
        debug=True,
    )
