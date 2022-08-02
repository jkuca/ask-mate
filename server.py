from flask import Flask, request, render_template, redirect, url_for, session
from sample_data import data_manager
import re

app = Flask(__name__)
app.secret_key = '>xG(<-FS]0i{3&)h@oEE#vkC$Qm3=/@6nUu]vE#-agp*j+G!]Fs+Qw#{:gSZ&YS'
# ADD displaying 5 latest questions

###################################################
############### Landing Page ######################
###################################################


@app.route("/", methods=['POST', 'GET'])
def home():
    latest_questions = data_manager.get_latest_questions(5)
    return render_template('home.html', questions=latest_questions)

###################################################
########## List of Question #######################
###################################################


@app.route("/list", methods=['POST', 'GET'])
def get_all_questions_sorted_by_submission_time():
    order = request.args.get('filter_question')
    direction = request.args.get('direction')
    if order and direction:
        questions = data_manager.get_sorted_questions(
            order, direction)
    else:
        questions = data_manager.get_sorted_questions('id', "DESC")
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
    comments_answer = []
    for i in answers:
        asa = data_manager.get_sorted_comments(
            parameter='answer_id', id=str(i['id']))
        comments_answer.append(asa)
    return render_template('display_question.html', data=question, answers=answers, comments=comments, comments_answer=comments_answer)

########### Question Options #######################


###### Add Question #############
@ app.route("/add_question", methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        id = data_manager.add_new_question(title, message)
        return redirect(url_for('get_question', question_id=id['id']))
    else:
        return render_template('ask_question.html')


######## Edit Question #############
@ app.route("/question/<string:id_post>/edit", methods=["POST", "GET"])
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

    return render_template("edit.html", data=data_of_question, direction='question')


########### Delete Question ############
@ app.route("/question/<string:question_id>/delete")
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect('/list')


#############################
#### Question Votes #########
#############################


######### Vote Up ########
@ app.route("/question/<string:question_id>/vote-up")
def vote_question_up(question_id):
    question = data_manager.get_question_by_id(question_id)
    data_manager.count_votes_up(question_id, question['vote_number'])
    blink_url = "/question/" + str(question_id)
    return redirect(blink_url, 302)

###### Vote Down ########


@ app.route("/question/<string:question_id>/vote-down")
def vote_question_down(question_id):
    question = data_manager.get_question_by_id(question_id)
    data_manager.count_votes_down(question_id, question['vote_number'])
    blink_url = "/question/" + str(question_id)
    return redirect(blink_url, 302)

#############################################################
############ Answer Options #################################
#############################################################

######## Add answer to Question ################


@ app.route("/question/<string:id_post>/new-answer", methods=['POST', 'GET'])
def add_answer(id_post):
    if request.method == 'POST':
        message = request.form.get('message')
        data_manager.add_new_answer(message, id_post)
        return redirect(url_for('get_question', question_id=id_post))
    return render_template('add_answer.html', data=id_post)


# template edit_answer - redirect from the answer page

############# Edit Answer ####################
@ app.route('/answer/<string:answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = data_manager.get_one_answer_by_id(answer_id)
    if request.method == "POST":
        message = request.form.get("message")
        data_manager.edit_answer(answer_id,  message)
        return redirect(url_for('get_question', question_id=answer['question_id']))
    return render_template('edit_answer.html', answer=answer)


################ Delete Answer ################
@ app.route("/answer/<string:id_answer>/delete")
def delete_answer(id_answer):
    answer = data_manager.get_one_answer_by_id(id_answer)
    data_manager.delete_answer(id_answer)
    blink_url = "/question/" + str(answer['question_id'])
    return redirect(blink_url, 302)

###############################################
################ Vote answers #################
###############################################

############## Answer Vote Up ################


@ app.route("/answer/<string:answer_id>/vote-up")
def vote_answer_up(answer_id):
    answer = data_manager.get_one_answer_by_id(answer_id)
    data_manager.count_votes_answer_up(answer_id, answer['vote_number'])
    blink_url = "/question/" + str(answer['question_id'])
    return redirect(blink_url, 302)

############## Answer Vote Down ################


@ app.route("/answer/<string:answer_id>/vote-down")
def vote_answer_down(answer_id):
    answer = data_manager.get_one_answer_by_id(answer_id)
    data_manager.count_votes_answer_down(answer_id, answer['vote_number'])
    blink_url = "/question/" + str(answer['question_id'])
    return redirect(blink_url, 302)


#############################
########## COMMENTS #########
#############################

########## Add Comment to Question ###############
@ app.route("/question/<string:id_question>/new-comment", methods=['POST', 'GET'])
def add_new_comment_question(id_question):
    question = data_manager.get_question_by_id(id_question)
    if request.method == 'POST':
        message = request.form.get('comment')
        data_manager.add_new_comment(message, id_question=id_question)
        return redirect(url_for('get_question', question_id=question['id']))
    return render_template('comment.html', data=question['id'])


########### Add Comment to Answer ################
@ app.route("/answer/<string:id_answer>/new-comment", methods=['POST', 'GET'])
def add_new_comment_answer(id_answer):
    answer = data_manager.get_one_answer_by_id(id_answer)
    if request.method == 'POST':
        message = request.form.get('comment')
        data_manager.add_new_comment(message, id_answer=id_answer)
        return redirect(url_for('get_question', question_id=answer['question_id']))
    return render_template('comment-answer.html', data=answer)


########## DELETE COMMENT ################
@ app.route('/comment/<string:comment_id>/delete')
def delete_comment(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    if comment['question_id']:
        blink_url = "/question/" + str(comment['question_id'])
    else:
        answer = data_manager.get_one_answer_by_id(comment['answer_id'])
        blink_url = "/question/" + str(answer['question_id'])
    data_manager.delete_comment(comment_id)
    return redirect(blink_url, 302)

########## EDIT COMMENT ################


@ app.route("/comment/<string:id_comment>/edit", methods=['POST', 'GET'])
def edit_comment(id_comment):
    if request.method == 'POST':
        message = request.form.get('message')
        data_manager.edit_comment(message, id_comment)
        comment = data_manager.get_comment_by_id(id_comment)
        if comment['question_id']:
            return redirect(url_for('get_question', question_id=comment['question_id']))
        else:
            answer = data_manager.get_one_answer_by_id(
                comment['answer_id'])
            return redirect(url_for('get_question', question_id=answer['question_id']))
    comment = data_manager.get_comment_by_id(id_comment)
    return render_template('edit.html', data=comment, direction='comment')

###########################################
########### Serch Bar #####################
###########################################


@ app.route('/search', methods=['POST', 'GET'])
def search_result():
    search_phrase = request.form['title']
    questions = data_manager.search_questions(search_phrase)
    return render_template('search.html', search_phrase=search_phrase, questions=questions)


############### LOGIN/REGISTER/SESSION ###########################


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = data_manager.getUser(username, password)
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        account = data_manager.getUserByUsername(username)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:

            data_manager.addUser(username, password, email)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)

#### USERS ####


@app.route('/users', methods=['GET', 'POST'])
def users():
    table = data_manager.getUsersInfo()
    return render_template('users.html', table=table)


@app.route('/profile')
def profile():
    user_info = data_manager.getUserById(str(session['id']))
    return render_template('profile.html', user_info=user_info)


@app.route('/user/<string:user_id>')
def user_profile(user_id):
    user_info = data_manager.getUserById(user_id)
    return render_template('userprofile.html', user_info=user_info)


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
