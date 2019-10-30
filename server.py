from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)

saved_answer = {}
saved_message = {}
saved_titles = {}


@app.route('/')
@app.route('/list')
def route_list():
    questions = data_manager.get_questions()
    return render_template("index.html", questions=questions)


@app.route('/list')
def answer_and_message():
    answer_text = None
    message_text = None
    if 'answer' in saved_answer:
        answer_text = saved_answer['answer']
    if 'message' in saved_message:
        message_text = saved_message['message']
    return render_template("index.html", answer=answer_text, message=message_text)


@app.route('/post-answer', methods=['GET', 'POST'])
def route_post():
    if request.method == 'POST':
        saved_titles['title'] = request.form['title']
        saved_answer['answer'] = request.form['answer']
        return redirect('/list')
    answer_text = None
    if 'answer' in saved_answer:
        answer_text = saved_answer['answer']
    return render_template('answer.html', answer=answer_text)


@app.route('/add-question', methods=['GET', 'POST'])
def route_add():
    if request.method == "POST":
        saved_message['message'] = request.form['message']
        return redirect('/list')
    message_text = None
    title_text = None
    if 'message' in saved_message:
        message_text = saved_message['message']
    if 'title' in saved_titles:
        title_text = saved_titles['title']
    return render_template('message.html', message=message_text, title=title_text)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id):
    answers_list = []
    questions = data_manager.get_questions()
    answers = data_manager.get_answers()
    for item in questions:
        if item['id'] == question_id:
            asked_question = item
    for item in answers:
        if item['question_id'] == question_id:
            answers_list.append(item)
    return render_template('question.html', asked_question=asked_question, answers_list=answers_list)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=7000,
        debug=True,
    )
