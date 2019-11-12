from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions = data_manager.get_questions()
    return render_template("index.html", questions=questions)


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
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    return render_template('question.html', question=question, answers=answers)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_post(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'POST':
        saved_answer = request.form['answer']
        data_manager.save_answers_to_question(saved_answer, question_id)
        return redirect(f"/question/{question_id}")
    return render_template('answer.html', question=question)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=7000,
        debug=True,
    )
