def page_title_from_question_title(question, max_word):
    return " ".join(question['title'].split()[:max_word])
