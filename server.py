from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route('/')
def last_numbered_question():
    numbered_question = data_manager.get_numbered_question(numb_limit=5)
    return render_template("index.html", questions=numbered_question)


@app.route('/list')
def all_question():
    allowed_order_options = ["title", "submission_time", "message"]
    order_by = request.args.get('order')
    if order_by in allowed_order_options:
        questions = data_manager.get_questions(order_by)
    else:
        questions = data_manager.get_questions(2)

    return render_template("list_questions.html", questions=questions)


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == "POST":
        question_title = request.form['title']
        question_message = request.form['note']
        data_manager.add_question(question_title, question_message)
        return redirect('/')
    return render_template('message.html')


@app.route('/question/<question_id>/update-question', methods=['POST', 'GET'])
def route_update_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == "POST":
        question_title = request.form['title']
        question_message = request.form['message']
        data_manager.update_question(question_id, question_title, question_message)
        return redirect(f'/question/{question_id}')
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
    return render_template('question.html', question=question, answers=answers, comment=comment)


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
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'POST':
        saved_answer = request.form['answer']
        data_manager.save_answers_to_question(saved_answer, question_id)
        return redirect(f"/question/{question_id}")
    return render_template('answer.html', question=question)


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
    return render_template('comment_ans.html', answer=answer, answer_id=answer_id, comment=comment)


@app.route('/registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        username = request.form['username']
        password = data_manager.hash_password(request.form['pwd1'])
        data_manager.register_user(username, password)

    return render_template('registration.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=7000,
        debug=True,
    )
