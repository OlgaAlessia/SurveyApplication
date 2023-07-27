from flask import Flask, request, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret40"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
SURVEY_LEN = len(survey.questions)

@app.route('/')
def get_user_survey():
    """Show list of survey"""
    return render_template("select-survey.html", survey=survey)

@app.route('/questions/<int:number>')
def get_question(number):
    """Show the question"""
    
    if (len(responses) == SURVEY_LEN):
        # The user answered all the questions!
        return redirect("/complete")
    
    if number != len(responses):
        flash(f"Try to access an invalid question {number}.")
        return redirect(f'/questions/{len(responses)}')
    
    question = survey.questions[number]
    return render_template("questions.html", qid=number, question=question)

@app.route('/answer', methods=["POST"])
def get_answer():
    """Get the answer of the question"""
    answer = request.form['choice']
    responses.append(answer)
    
    if (len(responses) == SURVEY_LEN):
        # The user answered all the questions!
        return redirect("/complete")
    
    return redirect(f'/questions/{len(responses)}')

@app.route('/complete')
def show_thanks():
    """Survey Complited. Show a Thank you Page"""
    return render_template('complete.html')
