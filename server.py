from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions = data_manager.get_questions()
    return render_template("index.html", questions=questions)


@app.route('/list')
def answer_and_message():
    saved_answer = {}
    saved_message = {}
    answer_text = None
    message_text = None
    if 'answer' in saved_answer:
        answer_text = saved_answer['answer']
    if 'message' in saved_message:
        message_text = saved_message['message']
    return render_template("index.html", answer=answer_text, message=message_text)


@app.route('/post-answer', methods=['GET', 'POST'])
def route_post():
    saved_answer = {}
    saved_titles = {}
    if request.method == 'POST':
        saved_titles['title'] = request.form['title']
        saved_answer['answer'] = request.form['answer']
        return redirect('/list')
    answer_text = None
    answer_title = None
    if 'answer' in saved_answer:
        answer_text = saved_answer['answer']
    if 'title' in saved_titles:
        answer_title = saved_titles['title']
    return render_template('answer.html', answer=answer_text, title=answer_title)


@app.route('/add-question', methods=['GET', 'POST'])
def route_add():
    saved_message = {}
    saved_titles = {}
    if request.method == "POST":
        saved_message['note'] = request.form['note']
        saved_message['title'] = request.form['title']
        return redirect('/list')
    message_text = None
    title_text = None
    if 'note' in saved_message:
        message_text = saved_message['note']
    if 'title' in saved_titles:
        title_text = saved_titles['title']
    return render_template('message.html', note=message_text, title=title_text)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id):
    answers_list = []
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    return render_template('question.html', question=question, answers=answers)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=7000,
        debug=True,
    )
