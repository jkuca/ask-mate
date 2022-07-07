from flask import Flask, request, render_template, jsonify, redirect, url_for
from sample_data import data_manager

app = Flask(__name__)

# ADD displaying 5 latest questions

###################################################
############### Landing Page ######################
###################################################


@app.route("/")
def home():
    latest_questions = data_manager.get_latest_questions(5)
    return render_template('home.html', questions=latest_questions)

###################################################
########## List of Question #######################
###################################################


@app.route("/list")
def get_all_questions_sorted_by_submission_time():
    questions = data_manager.get_sorted_questions('id', 'ASC')  # edit
    print(questions)
    return render_template('list.html', questions=questions)


##############b#####################################
########## Qestion by ID ##########################
###################################################

@app.route("/question/<string:question_id>")
def get_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answer_by_id(question_id)
    data_manager.count_visits(question_id, question['view_number'])
    comments = data_manager.get_sorted_comments(
        parameter='question_id', id=question_id)
    # , comments=comments)
    return render_template('display_question.html', data=question, answers=answers)

########### Question Options #######################


###### Add Question #############
@app.route("/add_question", methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        id = data_manager.add_new_question(title, message)
        return redirect(url_for('get_question', question_id=id['id']))
    else:
        return render_template('ask_question.html')


######## Edit Question #############
@app.route("/question/<string:id_post>/edit", methods=["POST", "GET"])
def edit_question(id_post):
    if request.method == "POST":
        message = request.form.get("message")
        title = request.form.get('title')

        data_manager.get_edit_question_message(id_post, message)
        if len(title) > 0:
            data_manager.get_edit_question_title(id_post, title)
        return redirect(url_for('get_question', question_id=id_post))
    else:
        data_of_question = data_manager.get_question_by_id(id_post)

    return render_template("edit.html", data=data_of_question)


########### Delete Question ############
@app.route("/question/<string:id_post>/delete")
def delete_question(id_post):
    data_manager.delete_question_by_id(id_post)
    return redirect('/list')


########## Add Comment to Question ###############
@app.route("/question/<string:id_question>/new-comment", methods=['POST', 'GET'])
def add_new_comment_question(id_question):
    if request.method == 'POST':
        message = request.form.get('comment')
        data_manager.add_new_comment(message, id_question=id_question)
        return redirect(url_for('get_question', question_id=id_question))
    else:
        question = data_manager.get_question_by_id("2")
        return render_template('comment.html', data=question)


#############################
#### Question Votes #########
#############################


######### Vote Up ########
@app.route("/question/<string:question_id>/vote-up")
def vote_question_up(question_id):
    question = data_manager.get_question_by_id(question_id)
    data_manager.count_votes_up(question_id, question['vote_number'])
    blink_url = "/question/" + str(question_id)
    return redirect(blink_url, 302)

###### Vote Down ########


@app.route("/question/<string:question_id>/vote-down")
def vote_question_down(question_id):
    question = data_manager.get_question_by_id(question_id)
    data_manager.count_votes_down(question_id, question['vote_number'])
    blink_url = "/question/" + str(question_id)
    return redirect(blink_url, 302)

#############################################################
############ Answer Options #################################
#############################################################

######## Add answer to Question ################


@app.route("/question/<string:id_post>/new-answer", methods=['POST', 'GET'])
def add_answer(id_post):
    if request.method == 'POST':
        message = request.form.get('message')
        data_manager.add_new_answer(id_post, message)
        return redirect(url_for('get_question', question_id=id_post))
    return render_template('add_answer.html', data=id_post)


# template edit_answer - redirect from the answer page

############# Edit Answer ####################
@app.route('/answer/<string:answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == "GET":
        answer = data_manager.get_answer_by_id(answer_id)
        return render_template('edit_answer.html', answer=answer)

    question = data_manager.get_question_by_id(answer['question_id'])
    edited_answer_data = {
        'message': request.form.get('message'),
        # 'image': request.form.get('image')
    }
    updated_answer = data_manager.edit_answer(answer_id, edited_answer_data)
    return redirect('/display_question/question["id"]', data=question, answers=updated_answer)

################ Delete Answer #################


@app.route("/answer/<string:id_answer>/delete")
def delete_answer(id_answer):
    data_manager.delete_row(id_answer, 'answer.csv')
    return redirect('/list')


###############################################
################ Vote answers #################
###############################################

############## Answer Vote Up ################
@app.route("/answer/<answer_id>/vote-up")
def vote_answer_up():
    pass

############## Answer Vote Down ################


@app.route("/answer/<answer_id>/vote-down")
def vote_answer_down():
    pass


############## Answer Add Comment ################
@app.route("/answer/<string:id_answer>/new-comment", methods=['POST', 'GET'])
def add_new_comment_answer(id_answer):
    if request.method == 'POST':
        message = request.form.get('comment')
        data_manager.add_new_comment(message, id_answer=id_answer)
        return redirect(url_for('get_question', question_id=id_answer))
    else:
        question = data_manager.get_question_by_id("2")
        return render_template('comment.html', data=question)


###########################################
########### Serch Bar #####################
###########################################

@app.route('/search')
def search_result():
    search_phrase = request.args.get('search_phrase')
    search_phrase = "How"
    questions = data_manager.search_questions(search_phrase)
    print(questions)
    return render_template('search.html', search_phrase=search_phrase, questions=questions)


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
