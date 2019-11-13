from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route('/')
def last_five_question():
    five_question = data_manager.get_last_five_question()
    return render_template("index.html", questions=five_question)


@app.route('/list')
def all_question():
    questions = data_manager.get_questions()
    return render_template("list_questions.html", questions=questions)


@app.route('/add-question', methods=['GET', 'POST'])
def route_add():
    if request.method == "POST":
        question_title = request.form['title']
        question_message = request.form['note']
        submission_time = data_manager.get_time()
        data_manager.add_question(question_title, question_message, submission_time)
        return redirect('/')
    return render_template('message.html')


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    return render_template('question.html', question=question, answers=answers)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect('/')


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
